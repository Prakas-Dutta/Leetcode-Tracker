from fastapi import FastAPI, HTTPException
from database import conn
from model import CompletedProblem, UpdatedInfo, UserInfo
import httpx
from ai_support import build_prompt, extract_json
from dotenv import load_dotenv
import get_recent_leetcode_solutions
import json
import os


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
def add_problem(problem_info: CompletedProblem):
    print(problem_info)
    problem = problem_info.model_dump()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM completed_list WHERE leetcode_id = %s and approach = %s', (problem['leetcode_id'], problem['approach']))
    db_problem = cursor.fetchone()
    if db_problem:
        cursor.close()
        raise HTTPException(status_code=409, detail='This problem already exists with this approach')
    else:
        cursor.execute('INSERT INTO completed_list VALUES(%s, %s)', (problem['leetcode_id'], problem['approach']))
        conn.commit()
        cursor.close()
        raise HTTPException(status_code=201, detail='Added successfully!!!')

@app.get('/problem_list/')
def no_of_problem():
    cursor = conn.cursor(buffered=True)
    cursor.execute('SELECT COUNT(*) FROM completed_list')
    number = cursor.fetchone()
    cursor.close()
    return number[0]

@app.get('/completed_list/')
def list_problem_approach():
    cursor = conn.cursor(buffered=True, dictionary=True)
    cursor.execute('SELECT DISTINCT approach, COUNT(*) as no_of_problems FROM completed_list GROUP BY approach')
    result = cursor.fetchall()
    cursor.close()
    return result


@app.delete('/completed_list/')
def delete_completed_problem(problem:CompletedProblem):
    id, approach = problem.leetcode_id, problem.approach
    cursor = conn.cursor(buffered=True)
    cursor.execute('SELECT * FROM completed_list WHERE leetcode_id=%s and approach=%s', (id, approach, ))
    row = cursor.fetchone()
    if row:
        cursor.execute('DELETE FROM completed_list WHERE leetcode_id=%s and approach=%s', (id, approach, ))
        conn.commit()
        cursor.close()
        raise HTTPException(status_code=204, detail='Deleted successfully!!!')
    else:
        cursor.close()
        raise HTTPException(status_code=404, detail='The value of ID or approach is wrong')


@app.patch('/completed_list/')
def update_approach(problem_info:UpdatedInfo):
    problem = problem_info.model_dump()
    cursor = conn.cursor(buffered=True)
    cursor.execute('SELECT * FROM completed_list WHERE leetcode_id=%s and approach=%s', (problem['leetcode_id'], problem['approach'], ))
    row = cursor.fetchone()
    if row:
        cursor.execute('UPDATE completed_list SET approach=%s WHERE leetcode_id=%s and approach=%s', (problem['updated_approach'], problem['leetcode_id'], problem['approach'], ))
        conn.commit()
        cursor.close()
        raise HTTPException(status_code=200, detail='Updated successfully!!!')
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
    raise HTTPException(status_code=200, detail='Login successful')

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
    raise HTTPException(status_code=201, detail='User created successfully')


@app.get('/suggestions/')
async def get_suggestions():
    leetcode_username = LEETCODE_USERNAME

    pattern_stats = list_problem_approach()
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