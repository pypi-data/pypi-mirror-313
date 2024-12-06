import os
from xiaoqiangclub import VERSION
from setuptools import setup, find_packages


def get_long_description():
    """获取详细描述"""
    try:
        if os.path.exists('README.md'):
            with open('README.md', 'r', encoding='utf-8') as f:
                return f.read()
        return 'XiaoqiangClub 自用工具包'
    except Exception as e:
        print(f"读取 README.md 失败: {e}")
        return 'XiaoqiangClub 自用工具包'


setup(
    name='xiaoqiangclub',
    version=VERSION,  # 示例版本号
    author='xiaoqiang',
    author_email='xiaoqiangclub@hotmail.com',
    description='XiaoqiangClub 自用工具包',
    long_description=get_long_description(),  # 项目详细描述
    long_description_content_type='text/markdown',
    url='https://gitee.com/xiaoqiangclub/xiaoqiangclub',
    install_requires=[  # 依赖包
        'aiofiles==24.1.0',
        'aiosqlite==0.20.0',
        'apscheduler==3.10.4',
        'bencodepy==0.9.5',
        'fake_useragent==1.5.1',
        'fastapi==0.115.5',
        'httpx[socks]==0.27.2',
        'openai==1.53.0',
        'pandas==2.2.3',
        'parsel==1.9.1',
        'playwright==1.49.0',
        'pycryptodome==3.21.0',
        'PyYAML==6.0.1',
        'pyzipper==0.3.6',
        'redis==5.2.0',
        'slowapi==0.1.9',
        'sqlitedict==2.1.0',
        'tinydb==4.8.2',
        'websocket==0.2.1',  # 星火大模型
        'wechatpy==1.8.18',
        'zhipuai==2.1.5.20230904'
    ],
    extras_require={
        # Windows 平台特定依赖
        'windows': ['pywin32==308',
                    'opencv-python==4.10.0.84',
                    'pillow==11.0.0',
                    'PyAutoGUI==0.9.54',
                    'pynput==1.7.7'],
    },
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    license='Apache 2.0',  # 指明使用的许可证
    python_requires='>=3.9',
    zip_safe=False,
    entry_points={  # 命令行入口
        'console_scripts': [
            'xiaoqiangclub = xiaoqiangclub.cmd.xiaoqiangclub_cli:main',
        ],
    },
)
