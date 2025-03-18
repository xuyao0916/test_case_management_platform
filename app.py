import logging
from flask import Flask, render_template, request
from models import create_table, insert_test_case, get_all_test_cases
from utils import generate_test_cases_from_requirements

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

# 创建数据库表
create_table()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        requirements = request.form.get('requirements')
        if not requirements:
            logging.warning("用户输入的需求为空")
            return "请输入有效的测试需求"

        try:
            logging.info(f"开始生成测试用例，输入的需求: {requirements}")
            test_cases_text = generate_test_cases_from_requirements(requirements)
            if test_cases_text:
                test_cases = []
                current_case = {
                    "project": "",
                    "steps": [],
                    "result": []
                }
                lines = test_cases_text.split('\n')
                for line in lines:
                    line = line.strip()
                    if line.startswith("测试项目："):
                        if current_case["project"]:
                            test_cases.append(current_case)
                            current_case = {
                                "project": "",
                                "steps": [],
                                "result": []
                            }
                        current_case["project"] = line.replace("测试项目：", "")
                    elif line.startswith("测试步骤："):
                        continue
                    elif line.startswith("预期结果："):
                        continue
                    elif line and current_case["project"]:
                        if not current_case["steps"]:
                            current_case["steps"].append(line)
                        else:
                            current_case["result"].append(line)
                # 添加最后一个测试用例
                if current_case["project"]:
                    test_cases.append(current_case)

                for case in test_cases:
                    try:
                        insert_test_case(case["project"], "\n".join(case["steps"]), "\n".join(case["result"]))
                        logging.info(f"成功保存测试用例: 项目={case['project']}, 步骤={case['steps']}, 预期结果={case['result']}")
                    except Exception as db_e:
                        logging.error(f"保存测试用例到数据库时发生错误: {str(db_e)}")
                        return f"保存测试用例到数据库时发生错误: {str(db_e)}"

                return render_template('test_case_display.html', test_cases=test_cases)
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

if __name__ == '__main__':
    app.run(debug=True)