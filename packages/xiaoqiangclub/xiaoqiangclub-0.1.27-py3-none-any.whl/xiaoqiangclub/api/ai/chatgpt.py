# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2024/11/3 07:36
# 文件名称： chatgpt.py
# 项目描述： GPT_API_free接口：https://github.com/chatanywhere/GPT_API_free
# 开发工具： PyCharm
# https://api.chatanywhere.tech
# https://github.com/chatanywhere/GPT_API_free/blob/main/images/jet2.png

from openai import OpenAI
from typing import (Union, Optional, List, Dict)


def chatgpt(messages: Union[str, List[Dict[str, str]]],
            api_key: str, stream: bool = False,
            model: str = "gpt-4o-mini") -> Optional[str]:
    """
    调用ChatGPT接口，获取回复

    :param messages: 完整的对话消息，包含角色和内容，可以是字符串或字典列表
    :param api_key: 用于访问API的密钥，申请链接：https://api.chatanywhere.org/v1/oauth/free/github/render
    :param stream: 是否使用流式输出
    :param model: 使用的模型代号，支持 'gpt-3.5-turbo'、'embedding'、'gpt-4o-mini'、'gpt-4'，默认为 'gpt-4o-mini'
    :return: ChatGPT的回复内容
    """
    if isinstance(messages, str):
        messages = [{"role": "user", "content": messages}]

    client = OpenAI(api_key=api_key, base_url="https://api.chatanywhere.tech/v1")

    try:
        if stream:
            answer = ""
            stream_response = client.chat.completions.create(
                model=model,
                messages=messages,
                stream=True,
            )
            for chunk in stream_response:
                if chunk.choices[0].delta.content:
                    answer_chunk = chunk.choices[0].delta.content
                    answer += answer_chunk
                    print(answer_chunk, end="", flush=True)
        else:
            completion = client.chat.completions.create(model=model, messages=messages)
            answer = completion.choices[0].message.content

        return answer
    except Exception as e:
        print(f"错误: {e}")
        return None


def chat_with_chatgpt(api_key: str, model: str = "gpt-4o-mini", stream: bool = True) -> None:
    """
    聊天循环接口，用户可以不断输入消息并获得回复

    :param api_key: 用于访问API的密钥
    :param model: 使用的模型代号，支持 'gpt-3.5-turbo'、'embedding'、'gpt-4o-mini'、'gpt-4'，默认为 'gpt-4o-mini'
    :param stream: 使用流式输出
    """
    messages = []
    print(f"开始和 {model} 连续对话，输入 'exit' 可以结束对话。")

    while True:
        user_input = input("你: ")

        if user_input.strip() == "":
            print("输入为空，请重新输入...")
            continue

        if user_input.lower() == 'exit':
            print("对话结束。")
            break
        messages.append({'role': 'user', 'content': user_input})
        bot_response = chatgpt(messages, api_key, model=model, stream=stream)

        if bot_response is not None:
            print("ChatGpt:", bot_response)
            messages.append({'role': 'assistant', 'content': bot_response})
        else:
            print("无法获取ChatGPT的回复，请重试。")
