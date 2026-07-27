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

