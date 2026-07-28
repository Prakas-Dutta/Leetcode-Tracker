from fastapi import FastAPI, HTTPException
from database import conn
from model import CompletedProblem, UpdatedInfo

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get('/{id}')
def get_problem_info(id: int):
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM problem_list WHERE id = %s', (id,))
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
        return "Successfully added!!!"

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
        return 'Deleted successfully!!!'
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
        return 'Updated successfully!!!'
    else:
        cursor.close()
        raise HTTPException(status_code=404, detail='The value of ID or approach is wrong')

import httpx, json, get_recent_leetcode_solutions

def build_prompt(pattern_stats, recent, contest_rating=1470):
    return f'''You are a DSA coach. Given a user's solved-problem pattern breakdown, 
    suggest what to practice next. Return ONLY valid JSON, no markdown, no code fences.

    Pattern counts: {pattern_stats}
    Recently solved (last 10): {recent}
    Contest rating: {contest_rating}

    Return JSON in exactly this format:
    {{
    "weak_patterns": ["pattern1", "pattern2"],
    "reasoning": "1-2 sentences",
    "suggested_focus": "pattern name",
    "suggested_problems": [{{ "name": "Problem name 1", "url": "https://leetcode.com/problems/problem-1/" }}, {{ "name": "Problem name 2", "url": "https://leetcode.com/problems/problem-2/" }}, {{ "name": "Problem name 3", "url": "https://leetcode.com/problems/problem-3/" }}]
    }}'''

from dotenv import load_dotenv
import os
import json
import httpx

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent"


def extract_json(raw_text: str) -> dict:
    """Strip markdown code fences if present, then parse JSON safely."""
    text = raw_text.strip()
    if text.startswith("```"):
        # remove leading ```json or ``` and trailing ```
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
        text = text.strip()
    return json.loads(text)


@app.get('/chatbot_suggestions/')
async def get_suggestions():
    leetcode_username = "Prakas26"  # your actual LeetCode handle

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