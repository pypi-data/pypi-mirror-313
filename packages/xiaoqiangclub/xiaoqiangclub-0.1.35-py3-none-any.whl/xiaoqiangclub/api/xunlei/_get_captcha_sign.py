# _*_ coding : UTF-8 _*_
# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2024/10/10 12:38
# 文件名称： _get_captcha_sign.py
# 项目描述： 获取验证码的签名
# 开发工具： PyCharm
import time
import hashlib
from xiaoqiangclub.config.log_config import log

# 配置
api_env = 'production'
xl_user_apis = {
    'development': ['https://dev-xluser-ssl.xunlei.com'],
    'beta-development': ['https://dev-xluser-ssl.xunlei.com'],
    'production': [
        'https://xluser-ssl.xunlei.com',
        'https://xluser2-ssl.xunlei.com',
        'https://xluser3-ssl.xunlei.com'
    ],
}
api_origins = xl_user_apis[api_env]

xbase_config = {
    "clientId": "Yd0uSVGrNJhCC2oE",
    "signKey": "jY41hOYPM2"
}

sso_config = {
    'packageName': 'pan.xunlei.com',
    'apiOrigins': api_origins,
    'algVersion': '1',
    'authorizePage': f"https://i.xunlei.com/center/account/personal/oauth/?client_id={xbase_config['clientId']}&ui_key=c",
    'scope': 'profile offline pan sso user',
    'signOutURI': 'https://pan.xunlei.com/yc/signout/?sso_sign_out=',
    **xbase_config
}

algorithms = [
    {"alg": "md5", "salt": "t24w3VjaHB++4RM"},
    {"alg": "md5", "salt": "pgA9zT3GQqQhXyWwL"},
    {"alg": "md5", "salt": "35Nt1aQOI67"},
    {"alg": "md5", "salt": "lKwoU/SK0AJ3y6vn+l3n"},
    {"alg": "md5", "salt": "h3OGLCTCzmbhJLmb6WTNq8ogHNuI8GnpVUJ"},
    {"alg": "md5", "salt": "v0Br3m00h2g5cXF1Zbpbt4DNh9/8tt8"},
    {"alg": "md5", "salt": "vOSCqn9uXdX02Nt4pQCoRmj0WiY7AvDh6"},
    {"alg": "md5", "salt": "oa2PBcypZ"},
    {"alg": "md5", "salt": "NeNF/rCYnaA1Yp"},
    {"alg": "md5", "salt": "yDCpWLF5b"},
    {"alg": "md5", "salt": "xK9k"},
    {"alg": "md5", "salt": "K0ACI+Yf"},
    {"alg": "md5", "salt": "XDWXowjmmnp1GF"},
    {"alg": "md5", "salt": "cX5DR4LoIKZy2hbC2xmVy"},
    {"alg": "md5", "salt": "VZVfriR9"}
]


def md5_hash(value: str) -> str:
    return hashlib.md5(value.encode('utf-8')).hexdigest()


async def get_pub_key_sign(login_device_id: str, timestamp: str = None) -> str:
    """
    从源代码中获取：webpack://src/api/get_pub_key_sign.js

    :param login_device_id: 当前登入的设备ID
    :param timestamp: 时间戳精确到毫秒
    :return:
    """
    try:
        if not timestamp:
            timestamp = str(int(round(time.time() * 1000)))

        # 初始化: captchaSign = client_id + client_version + package_name + device_id + timestamp
        captcha_sign = f"{sso_config['clientId']}2.9.0{sso_config['packageName']}{login_device_id}{timestamp}"
        for item in algorithms:
            captcha_sign = md5_hash(f"{captcha_sign}{item['salt']}")

        return f"{sso_config['algVersion']}.{captcha_sign}"
    except Exception as error:
        log.error(f"获取验证码签名失败: {error}")
