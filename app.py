import logging
from flask import Flask, render_template, request, jsonify
from models import create_table, insert_test_cases, get_all_test_cases
from utils import generate_test_cases_from_requirements

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

# 创建数据库表
create_table()

def parse_test_cases(test_cases_text):
    test_cases = []
    lines = test_cases_text.split('\n')
    current_case = {"title": "", "description": "", "steps": [], "results": [], "priority": ""}
    current_section = None

    for line in lines:
        line = line.strip()
        if line:
            if line.startswith("功能描述："):
                if current_case["description"]:
                    test_cases.append(current_case)
                    current_case = {"title": "", "description": "", "steps": [], "results": [], "priority": ""}
                description = line.replace("功能描述：", "").strip()
                current_case["description"] = description
                current_case["title"] = description.split('，')[0]
            elif line.startswith("测试步骤："):
                current_section = "steps"
            elif line.startswith("预期结果："):
                current_section = "results"
            elif line.startswith("优先级："):
                current_case["priority"] = line.replace("优先级：", "").strip()
            else:
                if current_section == "steps":
                    current_case["steps"].append(line)
                elif current_section == "results":
                    current_case["results"].append(line)

    if current_case["description"]:
        test_cases.append(current_case)

    return test_cases

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        requirements = request.form.get('requirements')
        if not requirements:
            logging.warning("用户输入的需求为空")
            return "请输入有效的测试需求"

        logging.info(f"收到的需求为: {requirements}")

        try:
            logging.info(f"开始生成测试用例，输入的需求: {requirements}")
            test_cases_text = generate_test_cases_from_requirements(requirements)

            if test_cases_text:
                test_cases = parse_test_cases(test_cases_text)

                try:
                    insert_test_cases(test_cases)
                    logging.info("所有测试用例已成功保存到数据库。")
                except Exception as db_e:
                    logging.error(f"保存测试用例到数据库时发生错误: {str(db_e)}")
                    return f"保存测试用例到数据库时发生错误: {str(db_e)}"

                return render_template('test_cases.html', test_cases=test_cases)
            else:
                logging.warning("生成测试用例失败，未获取到测试用例文本")
                return "生成测试用例失败，请稍后重试。"
        except Exception as e:
            logging.error(f"生成测试用例时发生错误: {str(e)}")
            return f"生成测试用例时发生错误: {str(e)}"
    return render_template('index.html')

@app.route('/test_cases')
def test_cases():
    try:
        cases = get_all_test_cases()
        return render_template('test_cases.html', cases=cases)
    except Exception as e:
        logging.error(f"获取测试用例列表时发生错误: {str(e)}")
        return "获取测试用例列表失败，请稍后重试。"

@app.route('/generate', methods=['POST'])
def generate():
    if 'file' in request.files:
        file = request.files['file']
        requirements = file.read().decode('utf-8')
    elif 'requirements' in request.form:
        requirements = request.form['requirements']
    else:
        logging.warning("未提供有效的文件或需求文本")
        return "请输入有效的文件或测试需求"

    try:
        logging.info(f"开始生成测试用例，输入的需求: {requirements}")
        test_cases_text = generate_test_cases_from_requirements(requirements)

        if test_cases_text:
            test_cases = parse_test_cases(test_cases_text)

            try:
                insert_test_cases(test_cases)
                logging.info("所有测试用例已成功保存到数据库。")
            except Exception as db_e:
                logging.error(f"保存测试用例到数据库时发生错误: {str(db_e)}")
                return f"保存测试用例到数据库时发生错误: {str(db_e)}"

            return render_template('test_cases.html', test_cases=test_cases)
        else:
            logging.warning("生成测试用例失败，未获取到测试用例文本")
            return "生成测试用例失败，请稍后重试。"
    except Exception as e:
        logging.error(f"生成测试用例时发生错误: {str(e)}")
        return f"生成测试用例时发生错误: {str(e)}"


@app.route('/test_cases')
def display_test_cases():
    try:
        # 这里的get_all_test_cases()需要返回一个满足上述数据结构的数据
        cases = get_all_test_cases()

        # 将数据库返回的数据转换成所需的格式
        formatted_cases = []
        for row in cases:
            formatted_cases.append({
                'title': row[1],
                'description': row[2],
                'steps': row[3].split('\n'),  # 拆分步骤字符串为列表
                'results': row[4].split('\n'),  # 拆分结果字符串为列表
                'priority': row[5]
            })

        return render_template('test_cases.html', test_cases=formatted_cases)
    except Exception as e:
        return f"Error retrieving test cases: {e}"


@app.route('/manage')
def manage_test_cases():
    try:
        cases = get_all_test_cases()

        formatted_cases = []
        for row in cases:
            # Assuming row is structured as (id, title, description, steps, expected_result, priority)
            formatted_cases.append({
                'title': row[1],
                'description': row[2],
                'steps': row[3].split('\n'),  # 拆分步骤字符串为列表
                'results': row[4].split('\n'),  # 拆分结果字符串为列表
                'priority': row[5]
            })

        return render_template('index.html', test_cases=formatted_cases)
    except Exception as e:
        logging.error(f"获取测试用例列表时发生错误: {str(e)}")
        return "获取测试用例列表失败，请稍后重试。"


@app.route('/api/test_cases')
def get_test_cases():
    try:
        cases = get_all_test_cases()
        formatted_cases = []

        for row in cases:
            formatted_cases.append({
                'title': row[1],
                'description': row[2],
                'steps': row[3].split('\n'),
                'results': row[4].split('\n'),
                'priority': row[5]
            })

        return jsonify(formatted_cases)
    except Exception as e:
        logging.error(f"获取测试用例列表时发生错误: {str(e)}")
        return jsonify({"error": "获取测试用例列表失败，请稍后重试。"}), 500


if __name__ == '__main__':
    app.run(debug=True)
