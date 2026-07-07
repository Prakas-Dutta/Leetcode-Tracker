import mysql.connector
from leetcode_all_problems import fetch_all_problems

def database_setup():
    cursor = conn.cursor()
    if cursor.execute('show tables;'):
        cursor.execute("create table problem_list('id' int, 'title' varchar(100), 'difficulty' varchar(6));")
        cursor.execute("create table completed_list('id' int, 'title' varchar(100), 'difficulty' varchar(6), 'approach':varchar(100));")
        data = fetch_all_problems()
        cursor.executemany(
            "INSERT INTO problem_list (id, title, difficulty) VALUES (%s, %s, %s)",
            data
        )
        cursor.close()
    else:
        data = fetch_all_problems()
        cursor.executemany(
            "INSERT INTO problem_list (id, title, difficulty) VALUES (%s, %s, %s)",
            data
        )
try:
    conn = mysql.connector.connect(
        host = 'localhost',
        user = 'prakas',
        password = 'Prakas09',
        database = 'leetcode'
    )
except Exception:
    conn = mysql.connector.connect(
        host = 'localhost',
        user = 'prakas',
        password = 'Prakas09',
    )
    cursor = conn.cursor()
    cursor.execute('create database leetcode;')
    database_setup()
    cursor.close()
    conn.close()
    conn = mysql.connector.connect(
        host = 'localhost',
        user = 'prakas',
        password = 'Prakas09',
        database = 'leetcode'
    )

database_setup()
