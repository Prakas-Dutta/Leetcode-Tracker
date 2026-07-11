from fastapi import FastAPI
from database import conn
from model import Problem, completedProblem

app = FastAPI()

@app.get('/{id}')
def get_problem_info(id: int):
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM problem_list WHERE id = %s', (id,))
    problem = cursor.fetchone()
    if problem is None:
        return "Enter valid LeetCode ID!!!"
    return problem

@app.post('/')
def add_problem(problem_info: completedProblem):
    problem = problem_info.model_dump()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM problem_list WHERE id = %d'%(problem['leetcode_id']))
    db_problem = cursor.fetchone()
    if db_problem == None:
        cursor.close()
        return "Wrong information!!!"
    else:
        cursor.execute('INSERT INTO completed_list VALUES(%s, %s, %s, %s)', (problem['leetcode_id'], problem['title'], problem['difficulty'], problem['approach']))
        conn.commit()
        cursor.close()
        return "Successfully added!!!"

@app.get('/no_of_problem/')
def no_of_problem():
    cursor = conn.cursor(buffered=True)
    cursor.execute('SELECT COUNT(*) FROM problem_list')
    number = cursor.fetchone()
    cursor.close()
    return number[0]

@app.get('/list_problem_approach/')
def list_problem_approach():
    cursor = conn.cursor(buffered=True, dictionary=True)
    cursor.execute('SELECT DISTINCT approach, COUNT(*) FROM completed_list GROUP BY approach')
    result = cursor.fetchall()
    cursor.close()
    return result


