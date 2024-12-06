
import time
import sys
import time
import asyncio
import websockets
import json
import os
from cryptography.fernet import Fernet

from SharedData.IO.SyncTable import SyncTable

# TODO: DONT SERVE DATA IF TABLE IS NOT IN MEMORY
class ServerWebSocket():

    BUFF_SIZE = int(128*1024)
    
    # Dict to keep track of all connected client sockets
    clients = {}
    # Create a lock to protect access to the clients Dict
    lock = asyncio.Lock()
    server = None
    accept_clients = None

    @staticmethod
    async def runserver(shdata, host, port):

        Logger.log.info(f'Listening on {host}:{port}')

        ServerWebSocket.shdata = shdata

        ServerWebSocket.server = await websockets.serve(ServerWebSocket.handle_client_thread, host, port)

        await ServerWebSocket.server.wait_closed()

    @staticmethod
    async def handle_client_thread(conn, path):
        addr = conn.remote_address
        Logger.log.info(f"New client connected: {addr}")
        # conn.settimeout(60.0)

        # Add the client socket to the list of connected clients
        async with ServerWebSocket.lock:
            ServerWebSocket.clients[conn] = {
                'watchdog': time.time_ns(),
                'transfer_rate': 0.0,
            }

        client = ServerWebSocket.clients[conn]
        client['conn'] = conn
        client['addr'] = addr

        try:
            await ServerWebSocket.handle_client_websocket(client)
        except Exception as e:
            Logger.log.error(f"Client {addr} disconnected with error: {e}")
        finally:
            async with ServerWebSocket.lock:
                ServerWebSocket.clients.pop(conn)
            Logger.log.info(f"Client {addr} disconnected.")
            conn.close()

    @staticmethod
    async def handle_client_websocket(client):

        client['authenticated'] = False
        conn = client['conn']

        # Receive data from the client
        data = await conn.recv()
        if data:
            # clear watchdog
            client['watchdog'] = time.time_ns()
            data = data.decode()
            login_msg = json.loads(data)
            # authenticate
            key = os.environ['SHAREDDATA_SECRET_KEY'].encode()
            token = os.environ['SHAREDDATA_TOKEN']
            cipher_suite = Fernet(key)
            received_token = cipher_suite.decrypt(login_msg['token'].encode())
            if received_token.decode() != token:
                errmsg = 'Client %s authentication failed!' % (
                    client['addr'][0])
                Logger.log.error(errmsg)
                raise Exception(errmsg)
            else:
                client['authenticated'] = True
                Logger.log.info('Client %s authenticated' %
                                (client['addr'][0]))

                client.update(login_msg) # load client message
                client = SyncTable.init_client(client)
                if client['action'] == 'subscribe':
                    if client['container'] == 'table':
                        await SyncTable.websocket_publish_loop(client)
                elif client['action'] == 'publish':
                    if client['container'] == 'table':
                        # reply with mtime and count
                        responsemsg = {
                            'mtime': float(client['records'].mtime),
                            'count': int(client['records'].count),
                        }
                        await conn.send(json.dumps(responsemsg))
                        await SyncTable.websocket_subscription_loop(client)

async def send_heartbeat():
    lasttotalupload = 0
    lasttotaldownload = 0
    lasttime = time.time()
    while True:
        # Create a list of keys before entering the loop
        client_keys = list(ServerWebSocket.clients.keys())
        nclients = 0
        totalupload = 0
        totaldownload = 0
        for client_key in client_keys:
            nclients = nclients+1
            c = ServerWebSocket.clients.get(client_key)
            if c is not None:
                if 'upload' in c:
                    totalupload += c['upload']
                
                if 'download' in c:
                    totaldownload += c['download']
                
        te = time.time()-lasttime
        lasttime = time.time()
        download = (totaldownload-lasttotaldownload)/te
        upload = (totalupload-lasttotalupload)/te
        lasttotaldownload = totaldownload
        lasttotalupload = totalupload        

        Logger.log.debug('#heartbeat#host:%s,port:%i,clients:%i,download:%.2fMB/s,upload:%.2fMB/s' \
                         % (host, port, nclients, download/1024, upload/1024))        
        await asyncio.sleep(15)

async def main():
    await asyncio.gather(
        ServerWebSocket.runserver(shdata, host, port),
        send_heartbeat()
    )

if __name__ == '__main__':

    from SharedData.Logger import Logger
    from SharedData.SharedData import SharedData
    shdata = SharedData('SharedData.IO.ServerWebSocket', user='master')
    SyncTable.shdata = shdata
    
    if len(sys.argv) >= 2:
        _argv = sys.argv[1:]
    else:
        msg = 'Please specify IP and port to bind!'
        Logger.log.error(msg)
        raise Exception(msg)

    args = _argv[0].split(',')
    host = args[0]
    port = int(args[1])    
    
    Logger.log.info('ROUTINE STARTED!')
    
    asyncio.run(main())
