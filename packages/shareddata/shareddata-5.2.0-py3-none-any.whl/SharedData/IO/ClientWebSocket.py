import time
import websockets
import numpy as np
import pandas as pd
import lz4.frame as lz4f
import asyncio
import struct
import json


from SharedData.Logger import Logger
from SharedData.IO.SyncTable import SyncTable


class ClientWebSocket():

    @staticmethod
    async def table_subscribe_thread(table, host, port,
            lookbacklines=1000, lookbackdate=None, snapshot=False, bandwidth=1e6):

        while True:
            try:
                # Connect to the server
                async with websockets.connect(f"ws://{host}:{port}") as websocket:

                    # Send the subscription message
                    msg = SyncTable.table_subscribe_message(
                        table, lookbacklines, lookbackdate, snapshot, bandwidth)
                    msgb = msg.encode('utf-8')
                    await websocket.send(msgb)

                    # Subscription loop
                    client = json.loads(msg)
                    client['conn'] = websocket
                    client['addr'] = (host, port) 
                    client = SyncTable.init_client(client,table)
                    await SyncTable.websocket_subscription_loop(client)
                    time.sleep(15)

            except Exception as e:
                msg = 'Retrying subscription %s,%s,%s,table,%s!\n%s' % \
                    (table.database, table.period,
                     table.source, table.tablename, str(e))
                Logger.log.warning(msg)
                time.sleep(15)
    
    @staticmethod
    async def table_publish_thread(table, host, port,
            lookbacklines=1000, lookbackdate=None, snapshot=False, bandwidth=1e6):

        while True:
            try:
                # Connect to the server
                async with websockets.connect(f"ws://{host}:{port}") as websocket:

                    # Send the subscription message
                    msg = SyncTable.table_publish_message(
                        table, lookbacklines, lookbackdate, snapshot, bandwidth)
                    msgb = msg.encode('utf-8')
                    await websocket.send(msgb)

                    response = await websocket.recv()
                    if response == b'':
                        msg = 'Subscription %s,%s,%s,table,%s closed  on response!' % \
                            (table.database, table.period,
                                table.source, table.tablename)
                        Logger.log.error(msg)
                        websocket.close()
                        break

                    response = json.loads(response)
                    
                    # Subscription loop
                    client = json.loads(msg)
                    client['conn'] = websocket
                    client['table'] = table
                    client['addr'] = (host, port)
                    client.update(response)
                    client = SyncTable.init_client(client,table)
                    
                    await SyncTable.websocket_publish_loop(client)
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
    shdata = SharedData('SharedData.IO.ClientWebSocket', user='master')

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
