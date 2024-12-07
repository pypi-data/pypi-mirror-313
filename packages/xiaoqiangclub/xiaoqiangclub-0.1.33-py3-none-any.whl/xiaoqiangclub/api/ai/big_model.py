# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2024/11/9 22:07
# 文件名称： big_model.py
# 项目描述： 智谱AI GLM-4-Flash：https://open.bigmodel.cn/dev/api/libraries
# 开发工具： PyCharm
import copy
import os
from typing import Optional
from zhipuai import ZhipuAI
from xiaoqiangclub.config.log_config import log
from xiaoqiangclub.data.file import read_file, write_file


class ZhiPuAIAPI:
    def __init__(self, api_key: str, model: str = "glm-4-flash", persona: str = None,
                 context: bool = True, save_context_file: str = None, **kwargs):
        """
        初始化智谱AI GLM-4-Flash模型接口封装

        :param api_key: 用户的API Key
        :param model: 使用的模型名称，默认为 "glm-4-flash"
        :param persona: 人物设定（可选）
        :param context: 是否使用上下文对话，默认为True
        :param save_context_file: 上下文对话保存的json文件路径，如果设置了该参数，context参数将无效，会默认开启上下文保存。
        :param kwargs: 其他参数，会传递给ZhipuAI的初始化函数
        """
        self.client = ZhipuAI(api_key=api_key, **kwargs)
        self.model = model
        self.persona = persona
        self.save_context_file = save_context_file
        self.context = context
        self.history: list = []  # 保存上下文对话

        # 如果设置了上下文文件，进行文件类型检查并读取内容
        if save_context_file:
            self._ensure_json_extension()
            self._load_context_from_file()

        # 如果设置了人物设定，加入消息列表
        if persona and (self.context or self.save_context_file):
            self.history.append({"role": "system", "content": self.persona})

    def _ensure_json_extension(self):
        """确保保存的文件是 JSON 格式，如果不是，则自动转换为 JSON 格式并记录警告"""
        if self.save_context_file and not self.save_context_file.endswith('.json'):
            log.warning(f"文件 {self.save_context_file} 不是 JSON 格式，自动转换为 JSON 格式。")
            self.save_context_file = os.path.splitext(self.save_context_file)[0] + '.json'

    def _load_context_from_file(self):
        """从文件加载上下文对话"""
        try:
            file_content = read_file(self.save_context_file, log_errors=False)
            if file_content:
                self.history.extend(file_content)
        except Exception as e:
            log.error(f"加载上下文文件时发生错误: {e}")

    def get_answer(self, question: str, stream: bool = False, print_replier: bool = False) -> Optional[str]:
        """
        获取回答

        :param question: 用户提问
        :param stream: 是否启用流式输出（默认False）
        :param print_replier: 是否打印模型名称（默认False）
        :return: 返回模型的回答内容（流模式下返回None）
        """
        if not self.context and not self.save_context_file:
            self.history = []
            if self.persona:
                self.history.append({"role": "system", "content": self.persona})

        self.history.append({"role": "user", "content": question})

        try:
            # 调用智谱AI接口获取响应
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.history,
                stream=stream,
            )
        except Exception as e:
            log.error(f"调用智谱AI接口时发生错误: {e}")
            return None

        if stream:
            # 处理流式响应
            reply = self._handle_stream_response(response, print_replier)
        else:
            # 处理非流式响应
            reply = response.choices[0].message.content

        # 将响应添加到上下文
        if self.context or self.save_context_file:
            self.history.append({"role": "assistant", "content": reply})

        # 保存上下文到文件（如果设置了保存路径）
        self._save_context_to_file()

        return reply

    def _handle_stream_response(self, response, chat_with_zhipuai: bool) -> Optional[str]:
        """处理流式响应"""
        reply = ""
        try:
            if chat_with_zhipuai:
                print("智谱AI：", end="", flush=True)  # 打印智谱AI的回复
            # 流式输出处理
            for chunk in response:
                chunk_content = chunk.choices[0].delta.content
                reply += chunk_content
                print(chunk_content, end='', flush=True)
            print("\n")
        except Exception as e:
            log.error(f"流式输出处理时发生错误: {e}")
            if chat_with_zhipuai:
                print(f"{self.model} 未返回有效的回答，请稍后重试...")
        return reply

    def _save_context_to_file(self):
        """保存上下文对话到文件"""
        if self.save_context_file:
            log.debug(f'保存上下文对话到文件: {self.save_context_file}')
            try:
                write_file(self.save_context_file, self.history, ensure_ascii=False)
            except Exception as e:
                log.error(f"保存上下文文件时发生错误: {e}")

    def chat_with_zhipuai(self):
        """
        实现连续对话功能
        """
        print(f"开始与 {self.model} 进行连续对话，输入 'exit' 或 '退出' 结束对话。")
        original_context_status = copy.deepcopy(self.context)  # 深拷贝保存当前上下文
        self.context = True  # 启用上下文对话
        try:
            while True:
                question = input("你：")  # 获取用户输入
                if question.lower() in ["exit", "退出"]:
                    print("对话结束，感谢您的使用！")
                    break

                self.get_answer(question, stream=True, print_replier=True)
        finally:
            self.context = original_context_status  # 恢复上下文对话状态
