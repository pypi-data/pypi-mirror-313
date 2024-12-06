import asyncio
import websockets
import argparse

def get_args():
    parser = argparse.ArgumentParser(description="Websocket tunnel configuration")
    parser.add_argument('--local_host', type=str, default='127.0.0.1', help="Local host address")
    parser.add_argument('--local_port', type=int, default=2222, help="Local port number")
    parser.add_argument('--remote_uri', type=str, required=True, help="Remote WebSocket URI wss://")

    return parser.parse_args()

# Configuration
args = get_args()
LOCAL_HOST = args.local_host
LOCAL_PORT = args.local_port
REMOTE_URI = args.remote_uri

async def forward_data(websocket, reader, writer):
    try:
        async for message in websocket:
            writer.write(message)
            await writer.drain()
    except Exception as e:
        print(f"Error in forward_data: {e}")
    finally:
        writer.close()
        await writer.wait_closed()

async def forward_socket_to_websocket(reader, websocket):
    try:
        while True:
            data = await reader.read(4096)
            if not data:
                break
            await websocket.send(data)
    except Exception as e:
        print(f"Error in forward_socket_to_websocket: {e}")

async def handle_client(reader, writer):
    try:
        async with websockets.connect(REMOTE_URI) as websocket:
            # Create tasks for bidirectional data forwarding
            to_server = asyncio.create_task(forward_socket_to_websocket(reader, websocket))
            to_client = asyncio.create_task(forward_data(websocket, reader, writer))

            await asyncio.gather(to_server, to_client)
    except Exception as e:
        print(f"Error in handle_client: {e}")
    finally:
        writer.close()
        await writer.wait_closed()

async def main():
    server = await asyncio.start_server(handle_client, LOCAL_HOST, LOCAL_PORT)
    async with server:
        print(f"Listening on {LOCAL_HOST}:{LOCAL_PORT}...")
        await server.serve_forever()

# Run the main function when the script is executed
if __name__ == "__main__":
    asyncio.run(main())