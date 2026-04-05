# 此文件是对[https://github.com/Mz1z/Mrp]的修改
# 基于[Apache-2.0 license]分发

from package import *
import config

# 转发客户端到服务器的流量
async def trans_c2s(reader, r_writer):
    while not reader.at_eof():
        data = await reader.read(256)
        if data[:0x8] == config.RCON_FLAG.encode():
            await RCON_command(data[0x8:].decode())
            continue
        r_writer.write(data)
        await r_writer.drain()
    r_writer.close()
        
# 转发服务器到客户端的流量
async def trans_s2c(r_reader, writer):
    while not r_reader.at_eof():
        r_data = await r_reader.read(256)
        writer.write(r_data)
        await writer.drain()
    writer.close()

async def handle(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f'> Receive connection: {addr}!')
    
    # 启动反向代理连接
    r_reader, r_writer = await asyncio.open_connection(config.MC_ADDR, config.MC_PORT)
    
    ret = await asyncio.gather(
        trans_c2s(reader, r_writer),
        trans_s2c(r_reader, writer)
    )

    print(f'> Close connection: {addr} !')
    
# 主服务器进程
async def main():
    config.server = await asyncio.start_server(
        handle, "0.0.0.0", config.PORT)
        
    addr = config.server.sockets[0].getsockname()
    print(f'Serving on {addr}')
    async with config.server:
        await config.server.serve_forever()
        

async def RCON_command(command: str) -> str:
    try:
        with MCRcon(config.RCON_HOST, config.RCON_PASSWORD, port=config.RCON_PORT) as mcr:
            response = mcr.command(command)
            return response
    except Exception as e:
        print(f'无法连接到RCON: {e}')
        return ""
    
def run():
    asyncio.run(main())