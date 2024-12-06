
import time
import sys
import socket
import threading
import time
import select
import numpy as np
import pandas as pd
import json
import os
from cryptography.fernet import Fernet
import lz4.frame as lz4f
import struct

from SharedData.Logger import Logger
from SharedData.IO.SyncTable import SyncTable

#TODO: DONT SERVE DATA IF TABLE IS NOT IN MEMORY
class ServerSocket():
    
    # Dict to keep track of all connected client sockets
    clients = {}
    # Create a lock to protect access to the clients Dict
    lock = threading.Lock()
    server = None
    shdata = None
    accept_clients = None

    @staticmethod
    def runserver(shdata, host, port):

        SyncTable.shdata = shdata

        ServerSocket.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # This line allows the address to be reused
        ServerSocket.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Create the server and start accepting clients in a new thread
        ServerSocket.accept_clients = threading.Thread(
            target=ServerSocket.accept_clients_thread, args=(host, port))
        ServerSocket.accept_clients.start()

    @staticmethod
    def accept_clients_thread(host, port):
        ServerSocket.server.bind((host, port))
        ServerSocket.server.listen()

        Logger.log.info(f'Listening on {host}:{port}')

        while True:
            conn, addr = ServerSocket.server.accept()
            threading.Thread(target=ServerSocket.handle_client_thread,
                             args=(conn, addr)).start()

    @staticmethod
    def handle_client_thread(conn, addr):
        Logger.log.debug(f"New client connected: {addr}")
        conn.settimeout(30.0)

        # Add the client socket to the list of connected clients
        with ServerSocket.lock:
            ServerSocket.clients[conn] = {
                'watchdog': time.time_ns(),
                'transfer_rate': 0.0,
                'download': 0,
                'upload': 0,
                'authenticated': False,
            }

        client = ServerSocket.clients[conn]
        client['conn'] = conn
        client['addr'] = addr
                
        try:
            ServerSocket.handle_client_socket(client)
        except Exception as e:
            Logger.log.error(f"Client {addr} disconnected with error: {e}")
        finally:
            with ServerSocket.lock:
                ServerSocket.clients.pop(conn)
            Logger.log.info(f"Client {addr} disconnected.")
            conn.close()

    @staticmethod
    def handle_client_socket(client):
        
        conn = client['conn']
        tini = time.time()
        while not client['authenticated']:
            # Check if there is data ready to be read from the client
            ready_to_read, _, _ = select.select([conn], [], [], 0)
            if not ready_to_read:
                if time.time()-tini > 5:
                    break
                time.sleep(0.001)                
            else:
                # Receive data from the client
                data = conn.recv(1024)
                if not data:
                    break
                else:
                    # clear watchdog
                    client['watchdog'] = time.time_ns()                    
                    
                    login_msg = json.loads(data.decode())
                    client.update(login_msg)

                    # authenticate
                    key = os.environ['SHAREDDATA_SECRET_KEY'].encode()
                    token = os.environ['SHAREDDATA_TOKEN']
                    cipher_suite = Fernet(key)
                    received_token = cipher_suite.decrypt(login_msg['token'].encode())
                    if received_token.decode() != token:
                        errmsg = 'Client %s authentication failed!' % (client['addr'][0])
                        Logger.log.error(errmsg)
                        raise Exception(errmsg)
                    else:
                        client['authenticated'] = True
                        Logger.log.info('Client %s authenticated' % (client['addr'][0]))
                                                
                        client = SyncTable.init_client(client)
                        if client['action'] == 'subscribe':
                            if client['container'] == 'table':
                                SyncTable.socket_publish_loop(client)
                        elif client['action'] == 'publish':
                            if client['container'] == 'table':
                                # reply with mtime and count
                                responsemsg = {
                                    'mtime': float(client['records'].mtime),
                                    'count': int(client['records'].count),
                                }
                                conn.sendall(json.dumps(responsemsg).encode())

                                SyncTable.socket_subscription_loop(client)


if __name__ == '__main__':

    from SharedData.Logger import Logger
    from SharedData.SharedData import SharedData
    shdata = SharedData('SharedData.IO.ServerSocket', user='master')

    if len(sys.argv) >= 2:
        _argv = sys.argv[1:]
    else:
        errmsg = 'Please specify IP and port to bind!'
        Logger.log.error(errmsg)
        raise Exception(errmsg)
    
    args = _argv[0].split(',')
    host = args[0]
    port = int(args[1])    
        
    ServerSocket.runserver(shdata, host, port)
    
    Logger.log.info('ROUTINE STARTED!')

    lasttotalupload = 0
    lasttotaldownload = 0
    lasttime = time.time()
    while True:        
        # Create a list of keys before entering the loop
        client_keys = list(ServerSocket.clients.keys())
        nclients = 0
        totalupload = 0
        totaldownload = 0
        for client_key in client_keys:
            nclients = nclients+1
            c = ServerSocket.clients.get(client_key)
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
        time.sleep(15)