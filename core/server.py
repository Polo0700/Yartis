import asyncio
import websockets
from brain import opencode


class server:
    def __init__(self, host="localhost", port=8765):
        self.host = host
        self.port = port

    async def handler(self, websocket):
        async for message in websocket:
            try:
                respuesta = opencode.peticion().ejecutar(message)
                await websocket.send(respuesta)
            except Exception as e:
                print(f"Error: {e}")

    async def start(self):
        async with websockets.serve(self.handler, self.host, self.port):
            print(f"servidor en ws://{self.host}:{self.port}")
            await asyncio.Future()
