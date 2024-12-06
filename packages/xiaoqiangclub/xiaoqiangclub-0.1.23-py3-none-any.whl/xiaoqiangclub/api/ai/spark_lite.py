# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2024/11/10 11:25
# 文件名称： spark_lite.py
# 项目描述： 科大讯飞星火大模型接口 Spark Lite：https://www.xfyun.cn/doc/spark/Web.html
# 开发工具： PyCharm
import ssl
import hmac
import json
import base64
import hashlib
import datetime
import websocket
from time import mktime
from typing import Optional
from threading import Thread, Event
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time
from xiaoqiangclub.config.log_config import log
from xiaoqiangclub.data.file import read_file, write_file


class SparkLiteAPI:
    def __init__(self, app_id: str, api_key: str, api_secret: str, model: str = "lite",
                 persona: str = None, context: bool = True, save_context_file: str = None):
        """
        初始化科大讯飞星火大模型接口
        https://console.xfyun.cn/services/cbm

        :param app_id: 申请的应用ID
        :param api_key: API密钥
        :param api_secret: API密钥的密钥
        :param model: 使用的模型名称，默认为 "lite"，支持 'lite(Pro版本)', 'generalv3.5(Max版本)', '4.0Ultra(4.0Ultra版本)', 'generalv3(Pro版本)'
        :param persona: 人物设定（可选），用于设定模型角色
        :param context: 是否启用上下文对话（默认启用）
        :param save_context_file: 上下文对话保存的json文件路径，如果设置了该参数，context参数将无效，会默认开启上下文保存。
        """
        self.app_id = app_id
        self.api_key = api_key
        self.api_secret = api_secret
        self.model = model
        self.host = "spark-api.xf-yun.com"
        self.path, self.spark_url = self._get_model_params()
        self.done_event = Event()
        self.result = []
        self.stream = False
        self.context = context
        self.persona = persona
        self.save_context_file = save_context_file
        self.history = []  # 保存对话历史

        # 如果启用了上下文并且提供了保存文件路径，则加载保存的对话历史
        if self.context or self.save_context_file:
            if self.save_context_file:
                self._load_context_from_file()
            if self.persona:
                self.history.append({"role": "system", "content": self.persona})

    def _get_model_params(self) -> tuple:
        """根据模型选择正确的 path 和 spark_url"""
        if self.model.lower() == "generalv3.5":
            return "/v3.5/chat", "wss://spark-api.xf-yun.com/v3.5/chat"  # Max版本
        elif self.model.lower() == "4.0ultra":
            return "/v4.0/chat", "wss://spark-api.xf-yun.com/v4.0/chat"  # 4.0Ultra版本
        elif self.model.lower() == "generalv3":
            return "/v3.1/chat", "wss://spark-api.xf-yun.com/v3.1/chat"  # Pro版本
        elif self.model.lower() == "lite":
            return "/v1.1/chat", "wss://spark-api.xf-yun.com/v1.1/chat"  # Lite版本
        else:
            raise ValueError(f"未知的模型: {self.model}")

    def _create_url(self) -> str:
        """生成 WebSocket 连接的 URL"""
        now = datetime.datetime.now()
        date = format_date_time(mktime(now.timetuple()))
        signature_origin = f"host: {self.host}\n"
        signature_origin += f"date: {date}\n"
        signature_origin += f"GET {self.path} HTTP/1.1"
        signature_sha = hmac.new(self.api_secret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha_base64 = base64.b64encode(signature_sha).decode('utf-8')
        authorization_origin = f'api_key="{self.api_key}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha_base64}"'
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode('utf-8')
        params = {
            "authorization": authorization,
            "date": date,
            "host": self.host
        }
        return self.spark_url + '?' + urlencode(params)

    @staticmethod
    def _on_error(ws, error: str):
        """处理 WebSocket 连接中的错误"""
        log.error(f"发生错误: {error}")

    @staticmethod
    def _on_close(ws, status_code: int, status_msg: str):
        """处理 WebSocket 连接关闭"""
        log.debug(f"关闭连接，code: {status_code}, message: {status_msg}")
        ws.api_instance.done_event.set()  # 设置事件标志

    def _on_open(self, ws):
        """WebSocket 连接成功时的回调"""
        data = json.dumps(self._generate_params(ws.query))
        ws.send(data)

    def _on_message(self, ws, message: str):
        """WebSocket 接收到消息时的回调"""
        data = json.loads(message)
        code = data['header']['code']
        if code != 0:
            log.error(f'请求错误: {code}, {data}')
            ws.close()
        else:
            choices = data["payload"]["choices"]
            status = choices["status"]
            content = choices["text"][0]["content"]
            self.result.append(content)
            if self.stream:
                print(content, end='', flush=True)
            if status == 2:
                ws.close()
                self.done_event.set()  # 设置事件标志

    def _generate_params(self, query: str) -> dict:
        """生成请求参数"""
        # 如果启用了上下文，更新对话历史
        if self.context:
            self.history.append({"role": "user", "content": query})

            # 检查历史记录长度，确保总长度不超过8000字符
            total_length = sum(len(item["content"]) for item in self.history)
            while total_length > 8000:
                self.history.pop(0)  # 删除最早的记录
                total_length = sum(len(item["content"]) for item in self.history)

        return {
            "header": {
                "app_id": self.app_id,
                "uid": "1234",  # 可以用真实的用户 ID 替代
            },
            "parameter": {
                "chat": {
                    "domain": self.model,
                    "temperature": 0.5,
                    "max_tokens": 4096,
                    "auditing": "default",
                }
            },
            "payload": {
                "message": {"text": self.history}
            }
        }

    def _save_context_to_file(self):
        """保存对话历史到文件"""
        if self.save_context_file:
            log.debug(f"保存上下文对话到文件: {self.save_context_file}")
            try:
                write_file(self.save_context_file, self.history, ensure_ascii=False)
            except Exception as e:
                log.error(f"保存上下文文件时发生错误: {e}")

    def _load_context_from_file(self):
        """从文件加载保存的对话历史"""
        try:
            file_content = read_file(self.save_context_file, log_errors=False)
            if file_content:
                self.history.extend(file_content)
        except Exception as e:
            log.error(f"加载上下文文件时发生错误: {e}")

    def _run_websocket(self, query: str):
        """运行 WebSocket 并处理消息"""
        ws_url = self._create_url()
        ws = websocket.WebSocketApp(ws_url, on_message=self._on_message, on_error=self._on_error,
                                    on_close=self._on_close, on_open=self._on_open)
        ws.query = query
        ws.api_instance = self  # 将当前实例传递给 WebSocket
        ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

    def get_answer(self, question: str, stream: bool = False) -> Optional[str]:
        """
        获取模型的回答

        :param question: 提问
        :param stream: 是否启用流式传输
        :return: 返回生成的回答内容
        """
        self.stream = stream
        self.result.clear()  # 清空之前的结果
        self.done_event.clear()  # 清除之前的事件
        thread = Thread(target=self._run_websocket, args=(question,))
        thread.start()
        self.done_event.wait()

        # 保存上下文到文件（如果设置了保存路径）
        self._save_context_to_file()

        return ''.join(self.result)

    def chat_with_spark_lite(self):
        """实现连续对话功能"""
        print(f"开始与 {self.model} 进行连续对话，输入 'exit' 或 '退出' 结束对话。")
        while True:
            user_input = input("\n我: ").strip()
            if not user_input:
                print("输入为空，请重新输入...")
                continue
            if user_input.lower() in ["exit", "退出"]:
                print("对话结束，感谢您的使用！")
                break
            answer = self.get_answer(user_input, stream=False)
            print(f"{self.model}:", answer)
            # 更新对话历史
            self.history.append({"role": "assistant", "content": answer})
            # 保存上下文到文件（如果设置了保存路径）
            self._save_context_to_file()
