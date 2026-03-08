LAUNCH: str = "" # 设置自定义启动命令，非空JAVA_PATH和SERVER_PATH配置无效
JAVA_PATH = "D:/Java/jdk8u472-b08/bin/java" # Java可执行文件路径
SERVER_PATH = "E:/mc/fwd-test/CatServer-4168d848-universal.jar" # 服务端核心jar包路径
RCON_HOST = '127.0.0.1' # 服务器IP，本地则为127.0.0.1
RCON_PORT = 25575 # RCON端口 (在server.properties中设置)
RCON_PASSWORD = 'testpassword' # RCON密码 (在server.properties中设置)
CHECK_INTERVAL = 10 # 检查在线人数的时间间隔，单位为秒
MODE = "v2" # 运行模式，v1模式只要检测到连接就自动开启服务端，v2模式需要验证KEY
KEY = b"testkey" # 验证KEY，仅v2模式使用
STOP_FLAG = b"stoptestkey" # 关闭服务端的KEY，v1,v2模式均可使用

# DATA
process = None
count = 0