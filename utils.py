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
        "model": "deepseek-chat",  # 确保选择支持的具体模型
        "messages": [
            {
                "role": "system",
                "content": (
                    "你是一个专业的测试用例生成器，根据用户提供的需求文档生成详细的测试用例。请遵循以下约束和指引：\n"
                    "1. 测试项目名称应简洁明了，不超过50个字符，只能包含字母、数字、中文、下划线和短横线。\n"
                    "   - 名称应清晰表述测试关注的核心功能或模块，具备概述性。\n"
                    "2. 每个测试步骤应以操作动词开头，如“打开”、“点击”、“输入”等，步骤之间需有合理的逻辑顺序，且每个步骤的描述可以更长些以包含更多细节。\n"
                    "   - 在测试步骤中，具体说明操作的对象或界面元素，例如“在用户名字段中输入用户名”。\n"
                    "   - 包含必要的前置条件描述，例如“用户必须已登录”，确保执行环境准备就绪。\n"
                    "   - 保证步骤的细节，使操作明确且可重复，例如“导航至设置页面，选择语言选项为中文”。\n"
                    "3. 预期结果必须是可验证的和具体的描述，避免模糊不清。每个步骤后需要独立的预期结果。\n"
                    "   - 描述应包括成功和失败场景，例如，“订单提交成功后，应显示确认消息”或“密码错误应显示错误提示”。\n"
                    "   - 结果描述应量化或引用特定应用状态，如“购物车中应显示2件商品”。\n"
                    "4. 生成的测试用例数量不限制，但需尽可能详细。\n"
                    "   - 包括核心功能测试，边界条件测试和异常处理路径。\n"
                    "5. 为每个测试用例提供优先级（高、中、低），以便于测试计划中的安排和兼顾。\n"
                    "   - 高优先级指关键功能，中优先级为一般功能，低优先级为次要流程。\n"
                    "输出格式为：功能描述：[测试功能描述]，测试步骤：[具体步骤]，预期结果:[具体结果]，优先级：[高/中/低]"
                )
            },
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
