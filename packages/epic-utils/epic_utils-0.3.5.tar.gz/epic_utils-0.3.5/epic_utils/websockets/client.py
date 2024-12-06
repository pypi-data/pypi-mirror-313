from websockets.sync.client import connect
import json

class WebSocketClient():
    def __init__(self, url : str):
        self.url = url
        self.websocket = connect(url)
    
    def send(self, data : str):
        if not isinstance(data, str):
            data = json.dumps(data)
        self.websocket.send(data)
        
    async def recv(self):
        return await self.websocket.recv()
