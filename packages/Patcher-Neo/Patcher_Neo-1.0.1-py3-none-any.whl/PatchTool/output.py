import asyncio
import websockets

async def handle_connection(websocket, path):
    while True:
        message = await websocket.recv()
        print(f"Received message: {message}")
        await websocket.send(f"Server: {message}")

start_server = websockets.serve(handle_connection, "192.168.1.100", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

import asyncio
import websockets

async def main():
    async with websockets.connect("ws://192.168.1.100:8765") as websocket:
        while True:
            message = input("Enter a message: ")
            await websocket.send(message)
            response = await websocket.recv()
            print(response)

asyncio.get_event_loop().run_until_complete(main())