import time
import sys
import socket
import numpy as np
import pandas as pd
import json
import os
from cryptography.fernet import Fernet
import lz4.frame as lz4f
import struct

from SharedData.Logger import Logger
from SharedData.IO.SyncTable import SyncTable


class ClientSocket():
    @staticmethod
    def table_subscribe_thread(table, host, port, 
        lookbacklines=1000, lookbackdate=None, snapshot=False, bandwidth=1e6):
        
        while True:
            try:
                # Connect to the server
                client_socket = socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((host, port))

                # Send the subscription message
                msg = SyncTable.table_subscribe_message(
                    table, lookbacklines, lookbackdate, snapshot, bandwidth)
                msgb = msg.encode('utf-8')
                bytes_sent = client_socket.send(msgb)
                
                # Subscription loop
                client = json.loads(msg)
                client['conn'] = client_socket                
                client['addr'] = (host, port) 
                client = SyncTable.init_client(client,table)
                SyncTable.socket_subscription_loop(client)
                time.sleep(15)

            except Exception as e:
                msg = 'Retrying subscription %s,%s,%s,table,%s!\n%s' % \
                    (table.database, table.period,
                     table.source, table.tablename, str(e))
                Logger.log.warning(msg)
                time.sleep(15)

    @staticmethod
    def table_publish_thread(table, host, port, 
        lookbacklines=1000, lookbackdate=None, snapshot=False, bandwidth=1e6):
        
        while True:
            try:
                # Connect to the server
                client_socket = socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((host, port))

                # Send the subscription message
                msg = SyncTable.table_publish_message(
                    table, lookbacklines, lookbackdate, snapshot, bandwidth)
                msgb = msg.encode('utf-8')
                client_socket.sendall(msgb)

                response = client_socket.recv(1024)
                if response == b'':
                    msg = 'Subscription %s,%s,%s,table,%s closed on response!' % \
                        (table.database, table.period,
                            table.source, table.tablename)
                    Logger.log.error(msg)
                    client_socket.close()
                    break
                response = json.loads(response)
                if response['mtime'] > table.records.mtime:
                    Logger.log.warning('Remote %s is newer!' % table.relpath)
                
                if response['count'] > table.records.count:
                    Logger.log.warning('Remote %s has more records!' % table.relpath)
                                       

                # Subscription loop
                client = json.loads(msg)
                client['conn'] = client_socket                
                client['addr'] = (host, port) 
                client = SyncTable.init_client(client,table)
                client.update(response)
                
                SyncTable.socket_publish_loop(client)
                time.sleep(15)

            except Exception as e:
                msg = 'Retrying subscription %s,%s,%s,table,%s!\n%s' % \
                    (table.database, table.period,
                     table.source, table.tablename, str(e))
                Logger.log.warning(msg)
                time.sleep(15)
    


if __name__ == '__main__':
    import sys
    from SharedData.Logger import Logger
    from SharedData.SharedData import SharedData
    shdata = SharedData('SharedData.IO.ClientSocket', user='master')

    if len(sys.argv) >= 2:
        _argv = sys.argv[1:]
    else:
        msg = 'Please specify IP and port to bind!'
        Logger.log.error(msg)
        raise Exception(msg)

    args = _argv[0].split(',')
    host = args[0]
    port = int(args[1])
    database = args[2]
    period = args[3]
    source = args[4]
    tablename = args[5]
    if len(args) > 6:
        pubsub = int(args[6])
    
    table = shdata.table(database, period, source, tablename)
    if pubsub == 'publish':
        table.publish(host, port)
    elif pubsub == 'subscribe':
        table.subscribe(host, port)

    while True:
        time.sleep(1)        