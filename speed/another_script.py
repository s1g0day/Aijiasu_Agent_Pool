import random
import subprocess
from argparse import ArgumentParser

AJIASU_PATH = "/usr/local/bin/ajiasu"  # 指定ajiasu的路径

def execute_command(command, input_text=None):
    """执行命令行命令并返回输出"""
    if input_text is not None:
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        stdout, _ = process.communicate(input=input_text)
        return stdout.strip()
    else:
        result = subprocess.run(command, capture_output=True, text=True)
        return result.stdout.strip()

def connect_to_node(node_id):
    """连接到指定节点"""
    command = [AJIASU_PATH, "connect", node_id]
    print(f"连接命令: {' '.join(command)}")
    # 输入proxy作为代理模式
    output = execute_command(command)
    if "ajiasu stopped. failure" in output:
        print("代理连接失败：服务器不可用于用户组。")
    else:
        print("未知的代理连接状态。")


if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument("-n", dest="node_id", default=None, help="请输入 node id")
    args = parser.parse_args()

    if args.node_id:
        connect_to_node(args.node_id)