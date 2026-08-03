import mysql.connector
from server.leetcode_all_problems import fetch_all_problems
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")


def database_setup(conn):
    cursor = conn.cursor(buffered = True)

    cursor.execute("SHOW TABLES")
    table_exists = cursor.fetchone() is not None

    if not table_exists:
        cursor.execute('''
            CREATE TABLE problem_list (
                leetcode_id INT PRIMARY KEY,
                title VARCHAR(150),
                difficulty VARCHAR(6)
            )
        ''')
        cursor.execute('''
            CREATE TABLE user_info (
                user_id INT PRIMARY KEY AUTO_INCREMENT,
                username VARCHAR(200),
                leetcode_username VARCHAR(200),
                password VARCHAR(60)
            )
        ''')
        cursor.execute('''
        CREATE TABLE completed_list
        (leetcode_id INT, user_id INT, approach VARCHAR(200),
        FOREIGN KEY (leetcode_id) REFERENCES problem_list(leetcode_id), 
        FOREIGN KEY (user_id) REFERENCES user_info(user_id),
        PRIMARY KEY(leetcode_id, user_id, approach));
        ''')

        data = fetch_all_problems()
        cursor.executemany(
            "INSERT INTO problem_list VALUES (%s, %s, %s)",
            data
        )
    else:
        data = fetch_all_problems()
        api_length = len(data)

        cursor.execute("SELECT COUNT(*) FROM problem_list")
        database_length = cursor.fetchone()[0]

        if api_length != database_length:
            cursor.executemany(
                "INSERT INTO problem_list VALUES (%s, %s, %s)",
                data[database_length:]
            )

    conn.commit()
    cursor.close()
try:
    conn = mysql.connector.connect(
        host = DB_HOST,
        user = DB_USER,
        password = DB_PASSWORD,
        database = DB_NAME
    )
except Exception:
    conn = mysql.connector.connect(
        host = DB_HOST,
        user = DB_USER,
        password = DB_PASSWORD,
    )
    cursor = conn.cursor()
    cursor.execute(f'create database {DB_NAME}')
    cursor.close()
    conn.close()
    conn = mysql.connector.connect(
        host = DB_HOST,
        user = DB_USER,
        password = DB_PASSWORD,
        database = DB_NAME
    )

database_setup(conn)
