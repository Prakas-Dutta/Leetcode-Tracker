from fastapi import FastAPI
from database import conn
from model import Problem

app = FastAPI()

@app.get('/{id}')
def get_database_info(id:int):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM problem_list WHERE id = %d'%(id))
    problem = cursor.fetchone()
    if problem == None:
        return 'Enter valid leetcode ID!!!'
    return problem

@app.post('/')
def add_problem(problem_info: Problem):
    problem = problem_info.model_dump()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM problem_list WHERE id = %d'%(problem['leetcode_id']))
    db_problem = cursor.fetchone()
    if db_problem != None:
        cursor.close()
        return "Wrong information!!!"
    else:
        cursor.execute('INSERT INTO completed_list VALUES(%s, %s, %s, %s)'%(problem['leetcode_id'], problem['title'], problem['difficulty'], problem['approach']))
        conn.commit()
        cursor.close()
