import json
import websockets


class websocket_server:
    def __init__(self,host,port):
        self.host = host
        self.post = port
        self.connected_users = set()

    async def start(self):
        # 替换为你的本地IP地址
        self._server = await websockets.serve(self.main_logic, self.host, self.post)
        
    async def main_logic(self, websocket, path):
        try:
            self.connected_users.add(websocket)
            async for message in websocket:
                if message == 'hello!':
                    continue
                await self.process_message(message)
                
        except Exception as e:
            if websocket in self.connected_users:  # 检查连接是否在集合中
                self.connected_users.remove(websocket)  # 移除用户
        finally:
            if websocket in self.connected_users:  # 检查连接是否在集合中
                self.connected_users.remove(websocket)  # 移除用户
                
    async def process_message(self, message):
            if message == 'hello!':
                return
            else:
                await self.broadcast(json.dumps({"error": "Unknown command"}))
                
    async def broadcast(self, response):
        if self.connected_users:  # 确保有用户连接
            disconnected_users = set()
            for user in self.connected_users.copy():  # 迭代副本以避免修改错误
                if user.open:  # 检查连接是否打开
                    try:
                        await user.send(response)
                    except websockets.ConnectionClosed:
                        disconnected_users.add(user)  # 将已关闭的用户添加到集合中
                    except Exception as e:
                        disconnected_users.add(user)  # 将已关闭的用户添加到集合中
            # 一次性移除已关闭的用户
            self.connected_users -= disconnected_users