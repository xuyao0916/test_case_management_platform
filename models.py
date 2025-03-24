import psycopg2
import logging

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def create_connection():
    try:
        conn = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password='211211',
            host='localhost',
            port='5432'
        )
        return conn
    except Exception as ex:
        logging.error(f"数据库连接失败: {str(ex)}")
        return None

def create_table():
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS test_cases (
                    id SERIAL PRIMARY KEY,
                    test_title TEXT NOT NULL,
                    test_description TEXT NOT NULL,
                    test_steps TEXT NOT NULL,
                    expected_result TEXT NOT NULL,
                    priority TEXT NOT NULL
                )
            ''')
            conn.commit()
        except Exception as ex:
            logging.error(f"创建或更新表失败: {str(ex)}")
        finally:
            cursor.close()
            conn.close()

def insert_test_case(test_case):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO test_cases (test_title, test_description, test_steps, expected_result, priority) VALUES (%s, %s, %s, %s, %s)",
                (test_case['title'], test_case['description'], "\n".join(test_case['steps']), "\n".join(test_case['results']), test_case['priority'])
            )
            conn.commit()
        except Exception as e:
            logging.error(f"数据库插入操作失败: {str(e)}")
        finally:
            cursor.close()
            conn.close()

def insert_test_cases(test_cases):
    for test_case in test_cases:
        insert_test_case(test_case)

def get_all_test_cases():
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM test_cases")
            rows = cursor.fetchall()
            print("Fetched rows:", rows)  # 添加调试打印

            if not rows:
                logging.info("没有获取到任何测试用例数据")
            else:
                logging.info(f"获取到 {len(rows)} 条测试用例数据")

            return rows
        except Exception as e:
            logging.error(f"获取测试用例失败: {str(e)}")
            return []
        finally:
            cursor.close()
            conn.close()
    return []

