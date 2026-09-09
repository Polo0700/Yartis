import asyncio

import websockets

from brain import opencode


class server:
    def __init__(self, host="localhost", port=8765):
        self.host = host
        self.port = port
        self.clientes = []

    async def handler(self, websocket):
        try:
            self.clientes.append(websocket)
            async for message in websocket:
                if not isinstance(message, str):
                    print(f"Mensaje recibido no es una cadena: {message}")
                    continue
                if message == "0x0x0Polo0700Audio":
                    print("Yartis ha detenido la reproducción de audio")
                    for cliente in self.clientes:
                        if cliente != websocket:
                            try:
                                await cliente.send(message)
                            except Exception as e:
                                print(f"Error al enviar mensaje a cliente: {e}")
                                self.clientes.remove(cliente)
                elif message == "0x0x0Polo0701Audio":
                    print("Yartis está hablando")
                    for cliente in list(self.clientes):
                        if cliente != websocket:
                            try:
                                await cliente.send(message)
                            except Exception as e:
                                print(f"Error al enviar mensaje a cliente: {e}")
                                self.clientes.remove(cliente)
                elif not message.startswith("0x0x0Polo0702VozRes|"):
                    print(f"Yartis ha recibido la respuesta: {message}")
                    respuesta = await opencode.peticion().ejecutar(message)
                    await websocket.send(respuesta)
                else:
                    _, mensajeVoz = message.split("|", 1)
                    print(f"Yartis ha recibido la respuesta de voz: {mensajeVoz}")
                    await websocket.send(mensajeVoz)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            if websocket in self.clientes:
                try:
                    self.clientes.remove(websocket)
                except Exception as e:
                    print(f"error: {e}")

    async def start(self):
        async with websockets.serve(self.handler, self.host, self.port):
            print(f"servidor en ws://{self.host}:{self.port}")
            await asyncio.Future()


if __name__ == "__main__":
    s = server()
    asyncio.run(s.start())
