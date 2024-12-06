# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2024/11/17 13:28
# 文件名称： create_python_project_template.py
# 项目描述： 创建Python项目模板
# 开发工具： PyCharm
import os
import argparse
from typing import Dict, Union
from xiaoqiangclub.data.file import format_path
from xiaoqiangclub.utils.time_utils import get_current_date


def file_header(filename: str, description: str, date: str) -> str:
    """
    生成文件头注释。

    :param filename: 文件名
    :param description: 项目描述
    :param date: 开发时间
    :return: 文件头注释
    """
    return f"""# 开发人员： Xiaoqiang
# 微信公众号:  XiaoqiangClub
# 开发时间： {date}
# 文件名称： {filename}
# 项目描述： {description}
# 开发工具： PyCharm\n"""


def init_py_content(project_name: str) -> str:
    """
    生成 project/__init__.py 文件内容。

    :param project_name: 项目名称
    :return: constants.py 文件内容
    """
    return f"""from .utils.constants import (VERSION, AUTHOR, DESCRIPTION, EMAIL, CURRENT_SYSTEM, DATA_PATH, LOG_PATH, LOG_FILE, log)

__title__ = "{project_name}"
__version__ = VERSION
__author__ = AUTHOR
__description__ = DESCRIPTION

__all__ = [
    "__title__", "__version__", "__author__", "__description__",
    "VERSION", "AUTHOR", "DESCRIPTION", "EMAIL",
    "CURRENT_SYSTEM", "DATA_PATH", "LOG_PATH", "LOG_FILE", "log",
]
"""


def utils_init_py_content() -> str:
    """生成 project/utils/__init__.py 文件内容"""
    return """from .constants import (VERSION, AUTHOR, DESCRIPTION, EMAIL, CURRENT_SYSTEM, DATA_PATH, LOG_PATH, LOG_FILE, log)


__all__ = [
    "VERSION", "AUTHOR", "DESCRIPTION", "EMAIL",
    "CURRENT_SYSTEM", "DATA_PATH", "LOG_PATH", "LOG_FILE", "log",
]
"""


def dockerfile_content(project_name: str) -> str:
    """生成 project/dockerfile 文件内容"""
    return f"""# 使用官方的Python镜像作为基础镜像，这里以Python 3.8为例
# 你可以根据你的项目实际需求修改Python版本
FROM python:3.9

# 设置环境变量
ENV WORK_DIR="/app/{project_name}/{project_name}" \
    RUN_FILE="start.py" \
    PORT="8000" \
    PIP_MIRROR="https://mirrors.aliyun.com/pypi/simple/"


# 设置工作目录，后续的操作都会在这个目录下。进行建议将WORKDIR设置为入口文件所在目录
WORKDIR ${{WORK_DIR}}

# 将当前目录（即包含Dockerfile的目录）下的所有文件复制到容器内的  /app 目录下
# 注意：. 表示当前目录， /app 是容器内的目标目录
COPY . /app

# 安装项目所需的依赖包
# 假设你的项目依赖都列在 requirements.txt 文件中
RUN pip install --no-cache-dir -r /app/{project_name}/requirements.txt -i ${{PIP_MIRROR}}

# 暴露容器内应用监听的端口
# 如果你的Python项目是一个Web应用，监听在8000端口，就暴露这个端口
# 你需要根据项目实际监听的端口修改这里的值
EXPOSE ${{PORT}}

# 定义容器启动时要执行的命令
# 这里假设你的Python项目启动脚本是 app.py，你需要根据实际情况修改
CMD ["python", "${{RUN_FILE}}"]

# 以下是构建镜像和创建、访问容器的命令示例，在实际使用时需要根据具体情况进行调整：

# 构建镜像命令
# docker build -t {project_name}:latest .
# -t：指定镜像的名称和标签，这里镜像名称是your_image_name，标签是latest
# . ：表示当前目录，即Dockerfile所在的目录，告诉Docker在此目录下寻找构建镜像所需的文件


# 创建并运行容器命令
# docker run -d -p 8111:8000 --name {project_name} {project_name}:latest
# docker run -d -p <主机端口>:<容器端口> --name <容器名称> <镜像名称>:<标签>
# -d：表示在后台运行容器
# -p：用于端口映射，这里将主机的8000端口映射到容器内的8000端口，假设你的Python应用在容器内监听8000端口
# --name：给容器指定一个名称，这里是my_python_container
# your_image_name:latest：指定要运行的镜像名称和标签，要与构建镜像时指定的一致


# 进入正在运行的容器（假设要执行一些容器内的操作）
# docker exec -it {project_name} /bin/bash
# docker exec -it <容器名称> /bin/bash
# -it：以交互模式分配一个伪终端
# my_python_container：要进入的容器名称，和创建容器时指定的名称一致
# /bin/bash：在容器内启动bash终端，方便执行命令
"""


def docker_compose_yaml_content(project_name: str) -> str:
    """
    生成 docker-compose.yaml 文件内容。
    :param project_name: 项目名称
    :return:
    """
    return f"""# docker-compose版本号，这里使用3.8版本的语法规则
version: '3.8'

services:
  # 定义名为my_fastapi_service的服务，代表我们的FastAPI应用服务
  {project_name}:
    # env_file:
    #   - ./.env
    build:
      # 构建镜像的上下文目录，通过.env文件中的变量指定，这里是项目在主机上的目录
      context: .
      # 指定构建镜像所使用的Dockerfile，这里是当前目录下的Dockerfile
      dockerfile: Dockerfile
    # 容器名称
    container_name: {project_name}
    
    ports:
      # 将主机端口（由.env文件中的HOST_PORT变量指定）和容器端口（由.env文件中的CONTAINER_PORT变量指定）进行映射，使得可以从主机访问容器内的应用
      - "8111:8000"

    environment:
      # 设置FastAPI应用的环境变量，值由.env文件中的FASTAPI_APP_ENV变量指定，用于配置应用运行环境
      - WORK_DIR=/app/{project_name}/{project_name}
      - RUN_FILE=start.py
      - PORT=8000
      - PIP_MIRROR=https://mirrors.aliyun.com/pypi/simple/
      
    volumes:
      # 将主机上的项目目录（由.env文件中的HOST_PROJECT_DIR变量指定）挂载到容器内的项目目录（由.env文件中的CONTAINER_PROJECT_DIR变量指定），方便数据共享和调试
      - /volume1/docker/my_website/data:/app/{project_name}/{project_name}/data
      - /volume1/docker/my_website/logs:/app/{project_name}/{project_name}/logs
      
    restart: always # 或者 unless-stopped/on-failure/no
    
    command:
      # 指定容器启动时执行的命令，通过运行指定的Python脚本，在Dockerfile的WORKDIR目录下执行，建议将WORKDIR设置为入口文件所在目录
      ["python", "start.py"]

# 以下是对应的调用命令：

# 要构建镜像（如果镜像尚未构建）并启动容器，需在包含此docker-compose.yml文件的目录下执行以下命令：
# docker-compose up -d
# 其中，-d参数表示在后台运行容器，这样容器启动后不会占用当前终端的输入输出，可继续在终端进行其他操作。

# 如果之后对项目代码或者配置做了修改，想要更新相关配置并重新启动容器（在某些情况下，比如代码修改但依赖没变化等），可再次执行以下命令：
# docker-compose up -d

# 若要停止容器运行，在包含此docker-compose.yml文件的目录下执行以下命令：
# docker-compose down
"""


def fastapi_view_py_content() -> str:
    """生成 project/fastapi_view.py 文件内容"""
    return """from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI, Request
from .utils import (log, CURRENT_SYSTEM)
from contextlib import asynccontextmanager
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

# pip install -i https://mirrors.aliyun.com/pypi/simple/ -U uvicorn
@asynccontextmanager
async def lifespan(app: FastAPI):
    \"\"\"
    生命周期函数
    https://fastapi.tiangolo.com/advanced/events/
    :param app: FastAPI对象
    :return: 
    \"\"\"
    # 应用启动时执行的代码
    log.info(f"启动 {__name__} ...")

    yield

    # 应用关闭时执行的代码
    log.info(f"关闭 {__name__} ...")


app = FastAPI(lifespan=lifespan)


# # 挂载静态文件目录，html=True 表示HTML文件会自动渲染后返回
# app.mount("/static", StaticFiles(directory="static", html=True), name="static")
#
# # 初始化Jinja2模板引擎
# templates = Jinja2Templates(directory="templates")
#
# # werobot制作的微信公众号接口，注意：在公众号填写链接的时候不要以 / 结尾，否则会报错
# app.add_route('/werobot', make_view(robot), ['GET', 'POST'])
# app.add_route('/werobot/', make_view(robot), ['GET', 'POST'])


@app.get("/{{item_id}}")
async def index(request: Request, item_id: str,
                q: Union[str, None] = None):  # 前台的示例url：http://127.0.0.1:8000/items/foo?q=1
    log.debug(request.url)
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}


class Item(BaseModel):
    name: str
    price: float


@app.post("/{{item_id}}")
async def index(request: Request, item_id: int, item: Item):
    log.debug(request.url)
    ret = {
        "item_id": item_id,
        "item": item
    }
    return ret


if __name__ == '__main__':
    import uvicorn

    # uvicorn fastapi_view:app --reload 需要在命令行中启动项目才能实现--reload
    if CURRENT_SYSTEM == 'Windows':  
        # 如果需要使用本地真实IP或者是映射本地端口就设置本地真实端口，直接在pycharm上运行重载会出现缓慢情况
        uvicorn.run("fastapi_view:app", host="127.0.0.1", port=8000, reload=True, log_level="debug")
    else:  # 生成环境下使用reload=False,否则workers>1会报错
        uvicorn.run("fastapi_view:app", host="0.0.0.0", port=8000, reload=False, log_level="info", workers=2)
"""


def constants_py_content(project_name: str) -> str:
    """
    生成 constants.py 文件内容。

    :param project_name: 项目名称
    :return: constants.py 文件内容
    """
    return f"""import os
import platform
from xiaoqiangclub import LoggerBase

# 版本号
VERSION = '0.0.1'
# 作者
AUTHOR = 'Xiaoqiang'
# 邮箱
EMAIL = 'xiaoqiangclub@hotmail.com'
# 项目描述
DESCRIPTION = '{project_name}'

# 当前运行的系统
CURRENT_SYSTEM = platform.system()

# 项目根目录
ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 创建数据存储目录 data
DATA_PATH = os.path.join(ROOT_PATH, 'data')
os.makedirs(DATA_PATH, exist_ok=True)

# 日志保存路径
LOG_PATH = os.path.join(ROOT_PATH, 'logs')
os.makedirs(LOG_PATH, exist_ok=True)
LOG_FILE = os.path.join(LOG_PATH, '{project_name}.log')

logger = LoggerBase('{project_name}', console_log_level='DEBUG', file_log_level='WARNING', log_file=LOG_FILE)
log = logger.logger
"""


def config_py_content() -> str:
    """
    生成 config.py 文件内容。

    :return: config.py 文件内容
    """
    return """from dataclasses import dataclass


@dataclass
class Config:
    pass
"""


def test_example_content() -> str:
    """
    生成 test_example.py 文件内容。

    :return: test_example.py 文件内容
    """
    return """import unittest


class TestExample(unittest.TestCase):
    def test_sample(self):
        self.assertEqual(1, 1)

if __name__ == "__main__":
    unittest.main()
"""


def setup_py_content(project_name: str) -> str:
    """
    生成 setup.py 文件内容，包含相关字段。

    :param project_name: 项目名称
    :return: setup.py 文件内容
    """
    return f"""import os
from {project_name} import (VERSION, AUTHOR, DESCRIPTION, EMAIL)
from setuptools import setup, find_packages


def get_long_description() -> str:
    \"\"\"获取详细描述\"\"\"
    try:
        if os.path.exists('README.md'):
            with open('README.md', 'r', encoding='utf-8') as f:
                return f.read()
        return DESCRIPTION
    except Exception as e:
        print(f"读取 README.md 失败: {{e}}")
        return DESCRIPTION


setup(
    name='{project_name}',
    version=VERSION,  # 示例版本号
    author=AUTHOR,
    author_email=EMAIL,
    description=DESCRIPTION,
    long_description=get_long_description(),  # 项目详细描述
    long_description_content_type='text/markdown',
    url='https://gitee.com/xiaoqiangclub/{project_name}',
    install_requires=[],  # 依赖包

    extras_require={{  # 可选的额外依赖
        # Windows 平台特定依赖
        'windows': [],
        # Linux 平台特定依赖
        'linux': []
    }},
    packages=find_packages(),  # 自动发现所有包
    classifiers=[  # 项目分类
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    license='MIT',  # 指明使用的许可证
    python_requires='>=3.10',  # 指定最低 Python 版本
    zip_safe=False,  # 是否可以放心地进行 zip 安装
    entry_points={{  # 命令行入口
        'console_scripts': [
            # 'xiaoqiangclub = xiaoqiangclub.cmd.xiaoqiangclub_cli:main',
        ],
    }},
)
"""


def license_content() -> str:
    """
    生成 LICENSE 文件内容。

    :return: LICENSE 文件内容
    """
    return """MIT License

Copyright (c) YEAR YOUR NAME

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""


def gitignore_content() -> str:
    """
    生成 .gitignore 文件内容。
    :return:
    """
    return """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.pybuilder/
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
#   For a library or package, you might want to ignore these files since the code is
#   intended to run in multiple environments; otherwise, check them in:
# .python-version

# pipenv
#   According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
#   However, in case of collaboration, if having platform-specific dependencies or dependencies
#   having no cross-platform support, pipenv may install_module dependencies that don't work, or not
#   install_module all needed dependencies.
#Pipfile.lock

# PEP 582; used by e.g. github.com/David-OConnor/pyflow
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/
/Pipfile.lock
/Pipfile
/.idea/
"""


# 创建项目结构
def create_structure(base_path: str, structure: Dict[str, str]) -> None:
    """
    创建项目结构。

    :param base_path: 基础路径
    :param structure: 项目结构字典
    """
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)


def create_python_project(project_name: Union[str, argparse.Namespace],
                          save_path: Union[str, argparse.Namespace] = None) -> None:
    """
    创建 Python 项目结构。

    :param project_name: 项目名称
    :param save_path: 保存路径
    """
    if isinstance(project_name, argparse.Namespace):
        save_path = project_name.directory
        project_name = project_name.name

    project_name = project_name.strip()
    save_path = save_path or os.getcwd()

    current_date = get_current_date()

    # 定义项目结构
    project_structure = {
        project_name + '_template': {
            project_name: {
                '__init__.py': file_header(f'{project_name}/__init__.py', 'init 文件',
                                           current_date) + init_py_content(project_name),  # 导入常量
                'config.py': file_header('config.py', '配置文件', current_date) + config_py_content(),
                'fastapi_view.py': file_header(f'{project_name}/fastapi_view.py', 'Fastapi视图文件',
                                               current_date) + fastapi_view_py_content(),
                'utils': {
                    '__init__.py': file_header(f'{project_name}/utils/__init__.py', 'utils 模块初始化文件',
                                               current_date) + utils_init_py_content(),
                    'constants.py': file_header(f'{project_name}/utils/constants.py', '常量定义文件',
                                                current_date) + constants_py_content(project_name),
                },
                'scripts': {
                    '__init__.py': file_header(f'{project_name}/scripts/__init__.py', 'scripts 模块初始化文件',
                                               current_date),
                },
            },
            'tests': {
                '__init__.py': file_header('tests/__init__.py', 'tests 模块初始化文件', current_date),
                'test_example.py': file_header('tests/test_example.py', '测试示例文件',
                                               current_date) + test_example_content(),
            },
            '.gitignore': gitignore_content(),
            'Dockerfile': dockerfile_content(project_name),
            'requirements.txt': "xiaoqiangclub",
            'docker-compose.yml': docker_compose_yaml_content(project_name),
            'README.md': '# ' + project_name + '\n\nDescription of the project.',
            'setup.py': file_header('setup.py', '项目安装配置文件', current_date) + setup_py_content(project_name),
            'LICENSE': license_content(),
        }
    }

    # 创建项目结构
    create_structure(save_path, project_structure)
    print(f"\n已生成Python项目结构：{format_path(os.path.join(save_path, project_name))}\n")


if __name__ == '__main__':
    # 示例用
    create_python_project('my_project')
