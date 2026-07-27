import mysql.connector
from leetcode_all_problems import fetch_all_problems

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
        CREATE TABLE completed_list
        (leetcode_id INT, approach VARCHAR(200),
        FOREIGN KEY (leetcode_id) REFERENCES problem_list(leetcode_id),
        PRIMARY KEY(leetcode_id, approach));
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
        host = 'localhost',
        user = 'root',
        password = 'Prakas09@123',
        database = 'leetcode'
    )
except Exception:
    conn = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'Prakas09@123',
    )
    cursor = conn.cursor()
    cursor.execute('create database leetcode;')
    database_setup()
    cursor.close()
    conn.close()
    conn = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'Prakas09@123',
        database = 'leetcode'
    )

database_setup(conn)
