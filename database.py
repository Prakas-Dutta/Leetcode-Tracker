import mysql.connector

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
    cursor.close()
    conn.close()
    conn = mysql.connector.connect(
        host = 'localhost',
        user = 'prakas',
        password = 'Prakas09',
        database = 'leetcode'
    )
