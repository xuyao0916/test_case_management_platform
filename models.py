import sqlite3


def create_connection():
    conn = sqlite3.connect('test_cases.db')
    return conn


def create_table():
    conn = create_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS test_cases
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 test_project TEXT NOT NULL,
                 test_steps TEXT NOT NULL,
                 expected_result TEXT NOT NULL)''')
    conn.commit()
    conn.close()


def insert_test_case(test_project, test_steps, expected_result):
    conn = create_connection()
    cursor = conn.cursor()
    # 修正列名以匹配表结构
    cursor.execute("INSERT INTO test_cases (test_project, test_steps, expected_result) VALUES (?,?,?)",
                   (test_project, test_steps, expected_result))
    conn.commit()
    conn.close()


def get_all_test_cases():
    conn = create_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM test_cases")
    rows = c.fetchall()
    conn.close()
    return rows