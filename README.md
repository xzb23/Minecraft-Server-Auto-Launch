# Minecraft-Server-Auto-Launch
用于自动控制Minecraft服务端启动/停止的Python脚本

以及游戏消息和RCON消息的转发
## 使用教程
1. 手动启动一次服务端
2. 在Minecraft服务端`server.properties`配置文件中配置`enable-rcon`为`true`, 配置`rcon.port`和`rcon.password`
3. 配置`config.py`中的配置项
4. 正常启动python脚本  
### tips 
1. 客户端正在开发中 [MSAL-Client](https://github.com/xzb23/MSAL-v2-Mode-Client)
2. 对于无法使用python脚本的情况，请自行编译为可执行文件
## 开发计划
- [ ] 日志系统
- [ ] 客户端
- [x] 游戏消息和RCON消息的转发（针对部分只能开放一个端口的游戏云）
## 鸣谢
[Mrp](https://github.com/Mz1z/Mrp) - 参考使用了其部分代码