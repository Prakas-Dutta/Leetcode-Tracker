from fastapi import FastAPI, HTTPException
from backend.database import conn
from backend.model import CompletedProblem, UpdatedInfo

app = FastAPI()

@app.get('/{id}')
def get_problem_info(id: int):
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM problem_list WHERE id = %s', (id,))
    problem = cursor.fetchone()
    cursor.close()
    if problem is None:
        raise HTTPException(status_code=404, detail='ID is not valid')
    return problem

@app.post('/')
def add_problem(problem_info: CompletedProblem):
    problem = problem_info.model_dump()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM problem_list WHERE id = %s', (problem['leetcode_id'],))
    db_problem = cursor.fetchone()
    if db_problem == None:
        cursor.close()
        raise HTTPException(status_code=404, detail='Wrong information')
    else:
        cursor.execute('INSERT INTO completed_list(leetcode_id, title, difficulty, approach) VALUES(%s, %s, %s, %s)', (problem['leetcode_id'], problem['title'], problem['difficulty'], problem['approach'],))
        conn.commit()
        cursor.close()
        return "Successfully added!!!"

@app.get('/problem_list/')
def no_of_problem():
    cursor = conn.cursor(buffered=True)
    cursor.execute('SELECT COUNT(*) FROM problem_list')
    number = cursor.fetchone()
    cursor.close()
    return number[0]

@app.get('/completed_list/')
def list_problem_approach():
    cursor = conn.cursor(buffered=True, dictionary=True)
    cursor.execute('SELECT DISTINCT approach, COUNT(*) FROM completed_list GROUP BY approach')
    result = cursor.fetchall()
    cursor.close()
    return result

@app.delete('/completed_list/{id}/{approach}')
def delete_completed_problem(id:int, approach:str):
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
    cursor.execute('SELECT * FROM completed_list WHERE leetcode_id=%s and approach=%s', (problem['id'], problem['approach'], ))
    row = cursor.fetchone()
    if row:
        cursor.execute('UPDATE completed_list SET approach=%s WHERE leetcode_id=%s and approach=%s', (problem['updated_approach'], problem['id'], problem['approach'], ))
        conn.commit()
        cursor.close()
        return 'Updated successfully!!!'
    else:
        cursor.close()
        raise HTTPException(status_code=404, detail='The value of ID or approach is wrong')

