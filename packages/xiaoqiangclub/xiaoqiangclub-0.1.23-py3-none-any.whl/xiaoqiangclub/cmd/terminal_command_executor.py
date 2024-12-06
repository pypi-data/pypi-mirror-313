# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2024/11/3 10:23
# 文件名称： terminal_command_executor.py
# 项目描述： 使用Python执行命令行命令
# 开发工具： PyCharm
import io
import sys
import asyncio
import subprocess
from typing import Optional
from xiaoqiangclub.config.log_config import log


def decode_output(output: bytes) -> str:
    """
    尝试使用utf-8和gbk解码输出字节

    :param output: 输出字节
    :return: 解码后的字符串
    """
    try:
        return output.decode('utf-8')
    except UnicodeDecodeError:
        return output.decode('gbk')


async def run_command_async(cmd: str, stream_stdout: bool = True) -> Optional[str]:
    """
    异步运行给定的终端命令，并返回命令的输出作为Python字符串
    示例命令: await run_command_async('ls -l')

    :param cmd: 要执行的shell命令
    :param stream_stdout: 是否使用流式打印
    :return: 命令的输出作为Python字符串，若发生错误则返回None
    """
    try:
        process = await asyncio.create_subprocess_shell(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )

        if stream_stdout:
            async for line in process.stdout:
                print(decode_output(line), end='')  # 使用解码输出
                await asyncio.sleep(0)  # 刷新缓冲区
        else:
            stdout, _ = await process.communicate()
            return decode_output(stdout)
    except Exception as e:
        log.error(f"执行命令时发生错误: {e}")
        return None


def run_command(cmd: str, stream_stdout: bool = True) -> Optional[str]:
    """
    同步方式运行给定的终端命令，并返回命令的输出作为Python字符串
    示例命令: run_command('ls -l')

    :param cmd: 要执行的shell命令
    :param stream_stdout: 是否使用流式打印
    :return: 命令的输出作为Python字符串，若发生错误则返回None
    """
    try:
        if stream_stdout:
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            for line in iter(process.stdout.readline, b''):
                sys.stdout.write(decode_output(line))  # 使用解码输出
                sys.stdout.flush()  # 刷新缓冲区
            process.wait()  # 等待命令执行完成
        else:
            result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            return decode_output(result.stdout)
    except Exception as e:
        log.error(f"运行命令时发生错误: {e}")
        return None


# Windows系统下可设置控制台编码为utf-8
if sys.platform.startswith('win'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
