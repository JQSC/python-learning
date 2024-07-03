import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())


# 获取环境变量
api_key = os.environ["OPENAI_API_KEY_LOCAL"]
base_url = os.environ["OPENAI_BASE_URL"]

client = OpenAI(api_key=api_key, base_url=base_url)


def get_completion_from_messages(
    messages, model="gpt-3.5-turbo", temperature=0, max_tokens=500
):
    """
    封装一个支持更多参数的自定义访问 OpenAI GPT3.5 的函数

    参数:
    messages: 这是一个消息列表，每个消息都是一个字典，包含 role(角色）和 content(内容)。角色可以是'system'、'user' 或 'assistant’，内容是角色的消息。
    model: 调用的模型，默认为 gpt-3.5-turbo(ChatGPT)，有内测资格的用户可以选择 gpt-4
    temperature: 这决定模型输出的随机程度，默认为0，表示输出将非常确定。增加温度会使输出更随机。
    max_tokens: 这决定模型输出的最大的 token 数。
    """
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,  # 这决定模型输出的随机程度
        max_tokens=max_tokens,  # 这决定模型输出的最大的 token 数
    )
    return response.choices[0].message.content
