import time
import shlex
import requests
import subprocess
from argparse import ArgumentParser
from requests.exceptions import ConnectionError

# 全局变量用于保存当前子进程
current_process = None

def call_another_python_script(speed_success):
    global current_process
    # 启动子进程并保存到全局变量中
    command_string = f"python another_script.py -f {speed_success}"
    # 将命令字符串解析为列表
    command = shlex.split(command_string)
    # 启动子进程并保存到全局变量中
    current_process = subprocess.Popen(command)

def terminate_process():
    global current_process
    # 如果当前有子进程正在运行，则终止它
    if current_process and current_process.poll() is None:
        current_process.terminate()
        current_process.wait()  # 等待子进程终止

def get_server_ip():
    # 使用 requests 模块获取当前服务器的 IP 地址
    url = "https://api.ipify.org?format=json"
    proxies = {
        'http': 'socks5://127.0.0.1:1080',  # 修改为您的 SOCKS5 代理地址和端口
        'https': 'socks5://127.0.0.1:1080'
    }
    try:
        response = requests.get(url, proxies=proxies)
        data = response.json()
        return data['ip']
    except ConnectionError as e:
        print("连接错误:", e)
        return None

def main(speed_success):
    try:
        while True:
            call_another_python_script(speed_success)
            print("\n调用另一个 Python 脚本成功")
            time.sleep(61)  # 每 * 秒调用一次
            server_ip = get_server_ip()
            if server_ip:
                print("当前服务器 IP 地址:", server_ip)
            else:
                print("获取服务器 IP 地址失败，等待重试...")
            terminate_process()  # 终止之前的子进程
    except KeyboardInterrupt:
        print("程序终止")
if __name__ == "__main__":


    parser = ArgumentParser()
    parser.add_argument("-f", dest="nodeid_file", default=None, help="请输入 nodeid 文件")
    args = parser.parse_args()

    if args.nodeid_file:
        print(f"Read file: {args.nodeid_file}")
        main(args.nodeid_file)