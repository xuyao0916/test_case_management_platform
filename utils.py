import requests
import json

# 替换为你自己的 DeepSeek API Key
DEEPSEEK_API_KEY = "sk-9b2493b9ffe1400ebe5a1813da608e6a"
# 根据实际情况修改 API 端点
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

def generate_test_cases_from_requirements(requirements):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }
    data = {
        "model": "deepseek-chat",  # 根据实际支持的模型选择
        "messages": [
            {"role": "system", "content": "你是一个专业的测试用例生成器，根据用户提供的需求文档生成详细的测试用例。请遵循以下约束：\n"
                                        "1. 测试项目名称应简洁明了，不超过50个字符，只能包含字母、数字、中文、下划线和短横线。\n"
                                        "2. 每个测试步骤应以明确的动词开头，如“打开”、“点击”、“输入”等，步骤之间需有合理的逻辑顺序，且每个步骤不超过100个字符。\n"
                                        "3. 预期结果必须是可验证的、具体的描述，避免模糊不清的表述，每个预期结果不超过150个字符。\n"
                                        "4. 生成的测试用例数量为3到5个。\n"
                                        "输出格式为：测试项目：[项目名称]，测试步骤：[具体步骤]，预期结果：[预期结果]"},
            {"role": "user", "content": requirements}
        ]
    }
    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        result = response.json()
        print("接口返回的原始数据:")
        print(result)

        if "choices" in result and len(result["choices"]) > 0:
            choice = result["choices"][0]
            if "message" in choice:
                message = choice["message"]
                # 检查 role 字段是否存在且值合理，同时检查 content 字段
                if "role" in message and "content" in message:
                    content = message["content"]
                    print("从返回数据中提取的用于生成测试用例的内容:")
                    print(content)
                    return content
                else:
                    print("返回数据中 message 缺少 role 或 content 字段")
            else:
                print("返回数据中 choice 缺少 message 字段")
        else:
            print("返回数据中缺少 choices 字段或其为空")
    except requests.RequestException as e:
        print(f"请求 DeepSeek API 时出现网络错误: {e}")
    except json.JSONDecodeError as e:
        print(f"解析 DeepSeek API 响应时出现 JSON 解析错误: {e}")
    except Exception as e:
        print(f"处理 DeepSeek API 响应时出现其他错误: {e}")
    return None