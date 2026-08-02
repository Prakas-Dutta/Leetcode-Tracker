from fastapi import FastAPI, HTTPException, Header, Depends
from database import conn
from model import CompletedProblem, UpdatedInfo, UserInfo
import httpx
from ai_support import build_prompt, extract_json
from dotenv import load_dotenv
import get_recent_leetcode_solutions
import json
import os
from jose import jwt
from datetime import timedelta, datetime, timezone


def create_access_token(userinfo: dict):
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    cursor = conn.cursor(buffered=True, dictionary=True)
    cursor.execute('SELECT user_id FROM user_info WHERE username=%s AND password=%s', (userinfo['username'], userinfo['password']))
    user_id = cursor.fetchone()
    userinfo = {'user_id': user_id['user_id'], "exp": expire}
    return jwt.encode(userinfo, SECRET_KEY, algorithm="HS256")

def verify_access_token(token: str = Header(...)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
LEETCODE_USERNAME = os.getenv("LEETCODE_USERNAME")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent"
SECRET_KEY = os.getenv("SECRET_KEY")

@app.get('/{id}')
def get_problem_info(id: int):
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM problem_list WHERE leetcode_id = %s', (id,))
    problem = cursor.fetchone()
    cursor.close()
    if problem is None:
        raise HTTPException(status_code=404, detail='ID is not valid')
    return problem

@app.post('/completed_list/')
def add_problem(problem_info: CompletedProblem, token: dict = Depends(verify_access_token)):
    problem = problem_info.model_dump()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM completed_list WHERE leetcode_id = %s and user_id = %s and approach = %s', (problem['leetcode_id'], token['user_id'], problem['approach']))
    db_problem = cursor.fetchone()
    if db_problem:
        cursor.close()
        raise HTTPException(status_code=409, detail='This problem already exists with this approach')
    else:
        cursor.execute('INSERT INTO completed_list VALUES(%s, %s, %s)', (problem['leetcode_id'], token['user_id'], problem['approach']))
        conn.commit()
        cursor.close()
        return 'Added successfully!!!'

@app.get('/problem_list/')
def no_of_problem(user_info: dict = Depends(verify_access_token)):
    cursor = conn.cursor(buffered=True)
    cursor.execute('SELECT COUNT(*) FROM completed_list WHERE user_id = %s', (user_info['user_id'],))
    number = cursor.fetchone()
    cursor.close()
    return number[0]

@app.get('/completed_list/')
def list_problem_approach(user_info: dict = Depends(verify_access_token)):
    cursor = conn.cursor(buffered=True, dictionary=True)
    cursor.execute('SELECT DISTINCT approach, COUNT(*) as no_of_problems FROM completed_list WHERE user_id = %s GROUP BY approach', (user_info['user_id'],))
    result = cursor.fetchall()
    cursor.close()
    return result


@app.delete('/completed_list/')
def delete_completed_problem(problem:CompletedProblem, user_info: dict = Depends(verify_access_token)):
    id, approach = problem.leetcode_id, problem.approach
    cursor = conn.cursor(buffered=True)
    cursor.execute('SELECT * FROM completed_list WHERE leetcode_id=%s and approach=%s and user_id=%s', (id, approach, user_info['user_id']))
    row = cursor.fetchone()
    if row:
        cursor.execute('DELETE FROM completed_list WHERE leetcode_id=%s and approach=%s and user_id=%s', (id, approach, user_info['user_id']))
        conn.commit()
        cursor.close()
        return'Deleted successfully!!!'
    else:
        cursor.close()
        raise HTTPException(status_code=404, detail='The value of ID or approach is wrong')


@app.patch('/completed_list/')
def update_approach(problem_info:UpdatedInfo, user_info: dict = Depends(verify_access_token)):
    problem = problem_info.model_dump()
    cursor = conn.cursor(buffered=True)
    cursor.execute('SELECT * FROM completed_list WHERE leetcode_id=%s and approach=%s and user_id=%s', (problem['leetcode_id'], problem['approach'], user_info['user_id']))
    row = cursor.fetchone()
    if row:
        cursor.execute('UPDATE completed_list SET approach=%s WHERE leetcode_id=%s and user_id=%s and approach=%s', (problem['updated_approach'], problem['leetcode_id'], user_info['user_id'], problem['approach']))
        conn.commit()
        cursor.close()
        return 'Updated successfully!!!'
    else:
        cursor.close()
        raise HTTPException(status_code=404, detail='The value of ID or approach is wrong')

@app.post('/login/')
def login_user(userinfo: UserInfo):
    cursor = conn.cursor(buffered=True, dictionary=True)
    cursor.execute('SELECT * FROM user_info WHERE username=%s AND password=%s', (userinfo.username, userinfo.password))
    result = cursor.fetchone()
    if result is None:
        cursor.close()
        raise HTTPException(status_code=404, detail='Invalid credentials')
    cursor.close()
    return {"message": "Login successful", "token": create_access_token(userinfo.model_dump())}

@app.post('/signup/')
def signup_user(userinfo: UserInfo):
    cursor = conn.cursor(buffered=True)
    cursor.execute('SELECT * FROM user_info WHERE username=%s', (userinfo.username,))
    result = cursor.fetchone()
    if result is not None:
        cursor.close()
        raise HTTPException(status_code=409, detail='Username already exists')
    cursor.execute('INSERT INTO user_info (username, password) VALUES (%s, %s)', (userinfo.username, userinfo.password))
    conn.commit()
    cursor.close()
    return 'User created successfully'

@app.get('/valid_approaches/{id}/')
def get_valid_approaches(id: int, user_info: dict = Depends(verify_access_token)):
    cursor = conn.cursor(buffered=True, dictionary=True)
    cursor.execute('SELECT approach FROM completed_list WHERE leetcode_id=%s and user_id=%s', (id, user_info['user_id']))
    result = cursor.fetchall()
    cursor.close()
    return [row['approach'] for row in result]

@app.get('/suggestions/')
async def get_suggestions(pattern_stats: list[dict] = Depends(list_problem_approach)):
    leetcode_username = LEETCODE_USERNAME

    recent = await get_recent_leetcode_solutions.get_recent_leetcode_solutions(
        leetcode_username=leetcode_username, limit=10
    )

    prompt = build_prompt(pattern_stats, recent)

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                GEMINI_URL,
                headers={
                    "x-goog-api-key": GEMINI_API_KEY,
                    "Content-Type": "application/json"
                },
                json={"contents": [{"parts": [{"text": prompt}]}]}
            )
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Could not reach Gemini API: {e}")

    data = resp.json()

    if "candidates" not in data:
        print("GEMINI ERROR RESPONSE:", data)
        raise HTTPException(status_code=502, detail=str(data))

    raw_text = data["candidates"][0]["content"]["parts"][0]["text"]

    try:
        return extract_json(raw_text)
    except json.JSONDecodeError:
        print("FAILED TO PARSE GEMINI OUTPUT:", raw_text)
        raise HTTPException(status_code=502, detail="Gemini returned non-JSON output")




