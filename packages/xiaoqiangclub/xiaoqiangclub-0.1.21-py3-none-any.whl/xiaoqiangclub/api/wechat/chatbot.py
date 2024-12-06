# _*_ coding : UTF-8 _*_
# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2024/10/23 12:25
# 文件名称： chatbot.py
# 项目描述： 微信对话开发平台API
# 开发工具： PyCharm
import os
import time
import json
import uuid
import hashlib
from xiaoqiangclub.config.log_config import log
from typing import (Optional, Union, Dict, List)
from xiaoqiangclub.config.constants import SYSTEM_TEMP_DIR
from xiaoqiangclub.data.token_manager import TokenManagerAsync
from xiaoqiangclub.utils.network_utils import get_response_async


class WeChatBotAPI:
    def __init__(self, app_id: str, token: str, encoding_aes_key: str, user_id: str):
        """
        微信对话开发平台API
        接入之前，需要先在对话平台官网创建机器人，并在应用绑定中申请开放 API 的接入参数。文档：
        https://developers.weixin.qq.com/doc/aispeech/confapi/dialog/token.html

        :param app_id: 微信对话开放平台：管理 > 应用绑定 > 开放API 获取
        :param token:
        :param encoding_aes_key:
        :param user_id: 微信对话开放平台：管理 > 基础设置 > 成员权限 > 用户ID 获取
        """
        self.app_id = app_id
        self.token = token
        self.aes_key = encoding_aes_key
        self.user_id = user_id
        self.nonce = 'XiaoqiangClub'
        # 获取access_token
        self.token_manager = TokenManagerAsync(self._get_access_token, storage_path=self.__access_token_file)
        # 获取只能对话需要用到的 signature 参数
        self.query_signature_manager = TokenManagerAsync(self.__get_query_signature,
                                                         storage_path=self.__query_signature_file)

    @property
    def __access_token_file(self):
        """保存access_token的文件"""
        return os.path.join(SYSTEM_TEMP_DIR, f'wechatbot_access_token_{self.app_id}.txt')

    @property
    def __query_signature_file(self):
        """保存access_token的文件"""
        return os.path.join(SYSTEM_TEMP_DIR, f'wechatbot_query_signature_{self.app_id}.txt')

    async def __get_query_signature(self) -> Optional[dict]:
        """
        获取调用机器人智能对话功能的参数 signature

        https://developers.weixin.qq.com/doc/aispeech/confapi/INTERFACEDOCUMENT.html
        :return: 签名和过期时间
        """
        try:
            # 构建请求参数
            data = {
                'userid': self.user_id
            }
            url = f'https://chatbot.weixin.qq.com/openapi/sign/{self.token}'
            response = await get_response_async(url, data=data)

            if response.status_code == 200:
                json_data = response.json()
                signature = json_data.get('signature')
                log.debug(f'获取 signature: {signature}')
                return {
                    'token': signature,
                    'expires_at': int(json_data.get('expiresIn')) + int(time.time()) - 60  # 过期时间
                }

        except Exception as e:
            log.error(f"获取 signature 失败：{e}")
            return None

    def __generate_signature(self, unix_timestamp: str, body: Optional[str] = "") -> str:
        """
        生成请求签名的函数。

        :param unix_timestamp: Unix 时间戳。
        :param body: 请求的 Body 内容，GET 请求时可以为空字符串。
        :return: 生成的签名字符串。
        """

        s = self.token + str(unix_timestamp) + self.nonce + hashlib.md5(body.encode()).hexdigest()
        sign = hashlib.md5(s.encode()).hexdigest()
        log.debug(f"生成签名：{sign}")
        return sign

    async def __get_headers(self, body, get_access_token: bool = False) -> dict:
        """
        生成请求头
        :param body: 请求内容，get请求需要设置为空：""
        :param get_access_token: 是否用于换取access_token
        :return:
        """
        timestamp = str(int(time.time()))
        if get_access_token:
            headers = {
                'X-APPID': self.app_id,
                'content-type': 'application/json',
                'request_id': str(uuid.uuid4()),
                'timestamp': timestamp,
                'nonce': self.nonce,
                'sign': self.__generate_signature(timestamp, json.dumps(body))
            }
        else:
            # 设置请求头
            headers = {
                'X-OPENAI-TOKEN': await self.token_manager.get_token_async(),
                'content-type': 'application/json',
                'request_id': str(uuid.uuid4()),
                'timestamp': timestamp,
                'nonce': self.nonce,
                'sign': self.__generate_signature(timestamp, json.dumps(body))
            }

        return headers

    async def _get_response(self, url: str, body: dict = None, get_access_token: bool = False,
                            return_json: bool = True, post: bool = False) -> Optional[Union[Dict, str]]:
        """
        获取响应
        :param url:
        :param body: 请求数据
        :param get_access_token: 是否用于换取access_token
        :param return_json: 是否返回json格式数据
        :return:
        """
        try:
            headers = await self.__get_headers(body, get_access_token)
            if body or post:
                response = await get_response_async(url, headers=headers, json=body)
            else:
                response = await get_response_async(url, headers=headers)

            if response.status_code == 200:
                return response.json() if return_json else response.text

            log.error(f"请求失败，状态码：{response.status_code}，响应内容：{response.text}")
            return None

        except Exception as e:
            log.error(f"网络请求发生错误: {e}")
            return None

    @staticmethod
    async def _get_data(get_key: str, json_data: dict, return_raw_data: bool = False) -> Optional[Union[str, int]]:
        """
        从响应中获取数据

        :param get_key: 数据在字典中的key
        :param json_data: 响应的json数据
        :param return_raw_data: 是否返回原始数据
        :return:
        """
        if return_raw_data:
            return json_data

        if not json_data:
            log.error(f"获取 {get_key} 失败：{json_data}")
            return None

        value = json_data.get('data', {}).get(get_key)
        if value:
            log.debug(f"获取到{get_key}：{value}")
            return value
        else:
            log.error(f"获取 {get_key} 失败：{json_data.get('msg')}")
            return None

    async def _get_access_token(self) -> Optional[dict]:
        """获取access_token"""
        body = {
            "account": self.user_id
        }

        json_data = await self._get_response('https://openaiapi.weixin.qq.com/v2/token', body, True)
        if not json_data:
            log.error(f"获取access_token失败：{json_data}")
            return None

        access_token = await self._get_data('access_token', json_data)
        expires_at = int(time.time()) + 100 * 60  # 过期时间100分钟
        return {'token': access_token, 'expires_at': expires_at}

    async def add_question(self, question: str, answers: Union[str, List[str]], question_class: str = '关键字',
                           similar_questions: List[str] = None, disable: bool = False, mode: int = 0,
                           threshold: str = '0.9', return_raw_data: bool = False) -> Optional[str]:
        """
        插入知识问答，对应页面：配置 > 知识问答 > 问题分类
        https://developers.weixin.qq.com/doc/aispeech/confapi/dialog/bot/import.html

        :param question:  问题：意图名称（标准问法），技能的主要问题
        :param answers: 回答列表，针对意图名称的回答
        :param question_class: 问题分类：技能名称，分类，默认为'关键字'分类
        :param similar_questions: 相似度问题列表，用户可能提出的变体问题
        :param disable: 是否禁用该意图，默认为False
        :param mode: 导入模式，0表示导入并覆盖已存在的，1表示覆盖（先删除原来所有，再导入），2表示如果存在就跳过
        :param threshold: 相似度阈值，默认为0.9
        :param return_raw_data: 是否返回原始数据，默认为False
        :return: API响应内容，返回JSON格式的响应字符串，字典的"code": 0表示添加成功
        """
        # 判断关键词是否存在
        exist = await self.keywords_exists(question)
        if exist and mode == 2:
            log.info(f"关键词 {question} 已存在，跳过")
            return None

        if not exist and mode == 2:  # 不存在就直接插入
            mode = 0

        data = {
            "mode": mode,
            "data": [
                {
                    "skill": question_class,
                    "intent": question,
                    "threshold": threshold,  # 相似度阈值，默认为0.9
                    "disable": disable,
                    "questions": similar_questions,
                    "answers": [answers] if isinstance(answers, str) else answers
                }
            ]
        }
        json_data = await self._get_response('https://openaiapi.weixin.qq.com/v2/bot/import/json', data)

        return await self._get_data('task_id', json_data, return_raw_data)

    async def publish_bot(self, return_raw_data: bool = False) -> Optional[str]:
        """
        调用发布API
        :param return_raw_data: 是否返回原始数据，默认为False
        :return: API响应内容解析后的字典
        """
        json_data = await self._get_response("https://openaiapi.weixin.qq.com/v2/bot/publish", body={}, post=True)
        task_id = await self._get_data('task_id', json_data, return_raw_data)
        if task_id:
            log.info(f"发布成功，任务ID：{task_id}")
        else:
            log.error(f"发布失败，{json_data}")

        return task_id

    async def get_task_info(self, task_id: str) -> Optional[dict]:
        """
        查询异步请求详情
        https://developers.weixin.qq.com/doc/aispeech/confapi/dialog/bot/fetch.html
        :param task_id: 任务ID，一般在请求结果中
        :return:
        """
        data = {
            'task_id': task_id
        }
        return await self._get_response('https://openaiapi.weixin.qq.com/v2/async/fetch', data)

    async def get_publish_progress(self, return_raw_data: bool = False) -> Optional[Union[dict, int]]:
        """
        获取机器人发布进度
        :param return_raw_data: 是否返回原始数据，默认为False
        :return: 发布进度，百分数，省略%
        """
        data = {
            "env": "online"
        }
        json_data = await self._get_response("https://openaiapi.weixin.qq.com/v2/bot/effective_progress", data)

        return await self._get_data('progress', json_data, return_raw_data)

    async def get_answer(self, query: str, return_node_name: bool = False,
                         return_raw_data: bool = False) -> Optional[Union[dict, tuple, str]]:
        """
        获取机器人智能对话结果
        :param query: 提问内容
        :param return_node_name: 是否返回节点名称，也就是知识问答中的知识分类，默认为False
        :param return_raw_data: 是否返回原始数据，默认为False
        :return:
        """
        try:
            # 获取签名
            signature = await self.query_signature_manager.get_token_async()

            if not signature:
                return None

            # 构建请求参数
            data = {
                'signature': signature,
                'query': query,
            }
            # 发送 POST 请求
            url = f'https://chatbot.weixin.qq.com/openapi/aibot/{self.token}'
            response = await get_response_async(url, data=data)
            if response.status_code == 200:
                json_data = response.json()
                if return_raw_data:
                    return json_data

                answer = json_data.get('answer')
                ans_node_name = json_data.get('ans_node_name')

                if return_node_name:
                    return ans_node_name, answer
                else:
                    return answer
        except Exception as e:
            log.error(f'获取答案失败：{e}')
            return None

    async def keywords_exists(self, keywords: str) -> bool:
        """
        判断关键词是否已经存在
        :param keywords: 关键词
        :return:
        """
        reply = await self.get_answer(keywords)
        if reply != '请问你是想了解以下问题吗？' and reply:  # 说明不存在
            return True

        return False

    async def chat_with_chatbot(self) -> None:
        """微信对话开发平台连续对话"""
        print('已开启对话模式，请输入对话内容，输入 exit 退出对话')

        while True:
            query = input('我：')
            query = query.strip()
            if query.lower() == 'exit':
                print('bye')
                break

            answer = await self.get_answer(query)
            if not answer:
                print('ChatBot：换个问题试试吧~')
            print(f'ChatBot：{answer}')
