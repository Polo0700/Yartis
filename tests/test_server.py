import asyncio
import websockets


class serverTest:
    def __init__(self, host="localhost", port=8765):
        self.host = host
        self.port = port
        self.url = f"ws://{host}:{port}"

    async def start(self):
        async with websockets.connect(self.url) as ws:
            await ws.send("prueba")
            respuesta = await ws.recv()
            print(f"Respuesta: {respuesta}")


if __name__ == "__main__":
    asyncio.run(serverTest().start())
