from package import *
import config
import forwarding

def get_number_of_players() -> int:
    try:
        with MCRcon(config.RCON_HOST, config.RCON_PASSWORD, port=config.RCON_PORT) as mcr:
            response = mcr.command("list")
            # 通常格式为: "There are X out of Y players online: Name1, Name2..."
            # 或者: "Players: X/Y"
            # There are 0/20 players online:
            # There are 0 of a max of 20 players online
            if "out of" in response:
                parts = response.split("out of")
                count_player = parts[0].split("are")[1].strip()
                # print(f"解析出的在线人数: {count_player}")
                # print("原始", response)
                return int(count_player)
            elif "of a max of" in response:
                parts = response.split("of a max of")
                count_player = parts[0].split("are")[1].strip()
                # print(f"解析出的在线人数: {count_player}")
                # print("原始", response)
                return int(count_player)
            elif "/" in response:
                response = response.split(" ")
                for part in response:
                    if "/" in part:
                        count_player = part.split("/")[0].strip()
                        break
                # print(f"解析出的在线人数: {count_player}")
                # print("原始", response)
                return int(count_player)
            else:
                print(f"无法解析在线人数，原始响应: {response}")
                return -2
    except Exception as e:
        # print(f'无法连接到RCON: {e}')
        return -1


def start_server():
    if runing_check():
        return -1 # 服务端已在运行
    tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    tcp_server.bind(('0.0.0.0', config.PORT))

    tcp_server.listen(1)
    conn, addr = tcp_server.accept()
    data = conn.recv(1024)
    conn.close()
    tcp_server.close()
    time.sleep(1)
    if data == config.STOP_FLAG:
        print("关闭脚本")
        return -3
    if config.MODE == "v2":
        if data != config.KEY:
            print(f"验证失败，收到key: {data}")
            return -2
    print(f'准备启动服务端')
    config.count = 0
    if os.name == 'nt': # Windows
        head = "start "
        end = ""
    elif os.name == 'posix': # Linux/Mac
        head = ""
        end = " &"
    if config.LAUNCH:
        os.system(head + config.LAUNCH + end)
    else:
        os.system(head + f"{config.JAVA_PATH} -jar {config.SERVER_PATH} nogui" + end)
        # config.process = subprocess.Popen([config.JAVA_PATH, '-jar', config.SERVER_PATH, 'nogui'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return 0

def runing_check():
    if get_number_of_players() == -1:
        # print('服务端已关闭')
        return False
    return True

def stop_server():
    try:
        with MCRcon(config.RCON_HOST, config.RCON_PASSWORD, port=config.RCON_PORT) as mcr:
            mcr.command('stop')
    except Exception as e:
        print(f'无法连接到RCON: {e}')

def stop_flag():
    # if config.process is None:
    #     return False
    if not runing_check():
        return False
    count_player = get_number_of_players()
    print(f"解析出的在线人数: {count_player}")
    if count_player == -1:
        # 无法获取在线人数，服务端不是启动状态 or 连接RCON失败
        return False
    if count_player == 0:
        config.count += 1
    else:
        config.count = 0
    if config.count >= 3: # 连续3次在线人数为0，关闭MC Server
        return True
    else:
        return False
    return False

if not os.path.exists("./minecraft-server"):
    os.mkdir("./minecraft-server")
os.chdir("./minecraft-server")
if True:
    while True:
        time.sleep(3)
        if not runing_check():
            print('服务端未在运行，等待消息')
            if start_server() == -3: break
            time.sleep(3)
            time.sleep(config.WAIT_FOR_THE_RUNTIME) # 等待服务端启动
        else:
            thread = threading.Thread(target=forwarding.run, daemon=True)
            thread.start()
            while True:
                time.sleep(config.CHECK_INTERVAL) 
                if stop_flag():
                    print('在线人数为0，准备关闭服务端')
                    config.server.close()
                    stop_server()
                    break
else:
    # 这里是不使用自动控制代码，有需求自己修改上方条件
    if config.LAUNCH:
        config.process = subprocess.Popen(config.LAUNCH.split(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        config.process = subprocess.Popen([config.JAVA_PATH, '-jar', config.SERVER_PATH, 'nogui'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    