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
    elif "ajiasu done" in output:
        print("代理连接成功。")
    else:
        print("未知的代理连接状态。")

def extract_node_id(node_info):
    """从节点信息中提取节点ID"""
    parts = node_info.split()
    if len(parts) >= 1:
        return parts[0]
    else:
        return None

def aijiasu_random_nodeid_conncet(nodes):
    # 随机选择一个节点
    node_id = random.choice(nodes)
    if node_id:
        # 连接到提取的节点
        connect_to_node(node_id)
        print(f"已连接至节点：{node_id}")
    else:
        print("未能提取节点ID")

if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument("-f", dest="nodeid_file", default=None, help="请输入 nodeid 文件")
    args = parser.parse_args()

    if args.nodeid_file:
        # 获取可用节点列表
        with open(args.nodeid_file, 'r', encoding='utf-8') as speed_success:
            speed_success = speed_success.readlines()
        # 去除列表中所有的 \n
        nodes = [item.strip() for item in speed_success]
        aijiasu_random_nodeid_conncet(nodes)