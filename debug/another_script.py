import subprocess
import random

AJIASU_PATH = "/usr/local/bin/ajiasu"  # 指定ajiasu的路径
PROTOCOL_INPUT_TEXT = "proxy\n"  # 定义协议类型，\n是必须的相当于输入proxy后的回车确认

def execute_command(command, input_text=None):
    """执行命令行命令并返回输出"""
    if input_text is not None:
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        stdout, _ = process.communicate(input=input_text)
        return stdout.strip()
    else:
        result = subprocess.run(command, capture_output=True, text=True)
        return result.stdout.strip()

def get_available_nodes():
    """获取可用节点列表"""
    command = [AJIASU_PATH, "list"]
    output = execute_command(command)
    # 解析节点信息
    lines = output.split("\n")
    nodes = [line.split(" - ")[-1].strip() for line in lines if line.strip() and "ok" in line]
    with open('log/get_available_nodes.log', 'w') as f: f.write('\n'.join(nodes))
    print("所有节点已写入: log/get_available_nodes.log")
    return nodes

def connect_to_node_0(node_id):
    """连接到指定节点"""
    command = [AJIASU_PATH, "connect", node_id]
    print(f"连接命令: {' '.join(command)}")
    # 输入proxy作为代理模式
    execute_command(command, input_text=PROTOCOL_INPUT_TEXT)

def connect_to_node(node_id):
    """连接到指定节点"""
    command = [AJIASU_PATH, "connect", node_id]
    print(f"连接命令: {' '.join(command)}")
    # 输入proxy作为代理模式
    output = execute_command(command, input_text=PROTOCOL_INPUT_TEXT)
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

def aijiasu_main():
    # 获取可用节点列表
    nodes = get_available_nodes()
    
    if nodes:
        # 随机选择一个节点
        selected_node = random.choice(nodes)
        # 提取节点ID
        node_id = extract_node_id(selected_node)
        if node_id:
            # 连接到提取的节点
            connect_to_node(node_id)
            print(f"已连接至节点：{node_id}")
        else:
            print("未能提取节点ID")
    else:
        print("未找到可用节点")

if __name__ == "__main__":
    aijiasu_main()