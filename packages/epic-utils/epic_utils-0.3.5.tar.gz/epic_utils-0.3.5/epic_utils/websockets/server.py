from websockets.server import *
import asyncio
import json

class WebSocketServer():
    def __init__(self, port : int):
        self.port = port
        self.clients = []
        self.events = {}
        
    async def setup(self):
        async with serve(self.main, "localhost", self.port):
            await asyncio.Future()
        
    async def main(self, websocket):
        text_data = await websocket.recv()
        data = json.loads(text_data)
        typ = data["type"]
        if typ in self.events:
            self.events[typ](websocket, data)
        
    def on_event(self, event, callback):
        self.events[event] = callback
    
    def run(self):
        asyncio.run(self.setup())