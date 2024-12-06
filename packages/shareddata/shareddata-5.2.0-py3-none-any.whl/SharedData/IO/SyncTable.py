import time
import sys
import socket
import numpy as np
import pandas as pd
import json
import os
from cryptography.fernet import Fernet
import lz4.frame as lz4f
import asyncio
import struct


from SharedData.Logger import Logger


class SyncTable():

    shdata = None

    BUFF_SIZE = int(128 * 1024)

    @staticmethod
    def recvall(sock, n):
        # Helper function to recv n bytes or return None if EOF is hit
        data = bytearray()
        while len(data) < n:
            packet = sock.recv(n - len(data))
            if not packet:
                return None
            data.extend(packet)
        return data
    
    @staticmethod
    def init_client(client,table=None):

        if table is None:
            client['records'] = SyncTable.shdata.table(client['database'], client['period'],
                                                    client['source'], client['tablename'])        
            client['table'] = client['records'].table
        else:
            client['table'] = table
            client['records'] = table.records
            
        client['hasindex'] = client['table'].hasindex
        client['upload'] = 0
        client['download'] = 0
        if not 'snapshot' in client:
            client['snapshot'] = False

        count = client['records'].count.copy()
        if client['hasindex']:
            # mtime update check
            if isinstance(client['mtime'], float):
                client['mtime'] = pd.Timestamp.fromtimestamp(float(client['mtime']))

            # loockback from line or date
            client['lookbackfromid'] = None
            if 'lookbackdate' in client:                
                client['lookbackfromid'], _ = client['records'].get_date_loc(pd.Timestamp(client['lookbackdate']))
                if client['lookbackfromid'] == -1:
                    client['lookbackfromid'] = count

            if client['lookbackfromid'] is not None:
                client['lookbackid'] = client['lookbackfromid']
            else:
                client['lookbackid'] = count - int(client['lookbacklines'])
            
            if client['lookbackid'] < 0:
                client['lookbackid'] = 0
            
            client['lastsenttimesize'] = client['records'].size - client['lookbackid']
            client['lastsentimestartrow'] = client['lookbackid']
            client['lastsenttime'] = np.full((client['lastsenttimesize'],),
                                   fill_value=client['mtime'], dtype='datetime64[ns]')
                    
        client['maxrows'] = int(
                np.floor(SyncTable.BUFF_SIZE/client['records'].itemsize))
                        
        client['lastmsgtime'] = time.time()

        return client
    
    # PUBLISH
    @staticmethod
    def get_ids2send(client):
        ids2send = []
                
        lastcount = client['count']

        if client['hasindex']:
            # mtime update check                    
            if client['lookbackfromid'] is not None:
                lookbackid = client['lookbackfromid']
            else:
                lookbackid = client['records'].count- client['lookbacklines']                
            if lookbackid < 0:
                lookbackid = 0
            client['lookbackid'] = lookbackid

            if client['records'].count>lookbackid:
                tblcount = client['records'].count.copy()
                lastsenttimestartid = lookbackid - client['lastsentimestartrow']
                lastsenttimeendid = tblcount - client['lastsentimestartrow']

                currmtime = client['records'][lookbackid:tblcount]['mtime'].copy()
                updtidx = currmtime > client['lastsenttime'][lastsenttimestartid:lastsenttimeendid]
                if updtidx.any():
                    updtids = np.where(updtidx)
                    if len(updtids) > 0:
                        ids2send.extend(updtids[0]+lookbackid)
                        client['lastsenttime'][lastsenttimestartid:lastsenttimeendid] = currmtime
                                        
            if client['snapshot']:
                client['snapshot'] = False
                lastcount = lookbackid

        # count update check
        curcount = client['records'].count.copy()
        if curcount > lastcount:
            newids = np.arange(lastcount, curcount)
            ids2send.extend(newids)
            client['count'] = curcount

        if len(ids2send) > 0:
            client['lastmsgtime'] = time.time() # reset lastmsgtime
            ids2send = np.unique(ids2send)
            ids2send = np.sort(ids2send)
        
        return client, ids2send

    @staticmethod
    def table_publish_message(table, lookbacklines, lookbackdate, snapshot, bandwidth):
        shnumpy = table.records        
                
        key = os.environ['SHAREDDATA_SECRET_KEY'].encode()        
        cipher_suite = Fernet(key)
        cipher_token = cipher_suite.encrypt(os.environ['SHAREDDATA_TOKEN'].encode())
        msg = {
            'token': cipher_token.decode(),
            'action': 'publish',
            'database': table.database,
            'period': table.period,
            'source': table.source,
            'container': 'table',
            'tablename': table.tablename,
            'count': int(shnumpy.count),
            'mtime': float(shnumpy.mtime),
            'lookbacklines': lookbacklines,
            'bandwidth': bandwidth
        }
        if isinstance(lookbackdate, pd.Timestamp):            
            msg['lookbackdate'] = lookbackdate.strftime('%Y-%m-%d')
        if snapshot:
            msg['snapshot'] = True
        msg = json.dumps(msg)
        return msg
    
    @staticmethod
    def socket_publish_loop(client):
        
        Logger.log.info('Publishing updates of %s/%s/%s/%s -> %s' %
                        (client['database'], client['period'],
                         client['source'], client['tablename'], client['addr'][0]))
        
        conn = client['conn']
        records = client['records']        
        while True:
            try:
                client, ids2send = SyncTable.get_ids2send(client)
                
                if len(ids2send) > 0:
                    rows2send = len(ids2send)
                    sentrows = 0         
                    msgsize = min(client['maxrows'], rows2send)
                    bandwidth = client['bandwidth']
                    tini = time.time_ns()
                    bytessent = 0
                    while sentrows < rows2send:
                        t = time.time_ns()
                        message = records[ids2send[sentrows:sentrows + msgsize]].tobytes()
                        compressed = lz4f.compress(message)
                        msgbytes = len(compressed)
                        bytessent+=msgbytes+4                        
                        msgmintime = msgbytes/bandwidth
                        length = struct.pack('!I', len(compressed))
                        conn.sendall(length+compressed)
                        sentrows += msgsize
                        msgtime = (time.time_ns()-t)*1e-9
                        ratelimtime = max(msgmintime-msgtime,0)
                        if ratelimtime > 0:
                            time.sleep(ratelimtime)

                    totalsize = (sentrows*records.itemsize)/1e6
                    totaltime = (time.time_ns()-tini)*1e-9
                    transfer_rate = totalsize/totaltime                                            
                    client['transfer_rate'] = transfer_rate
                    client['upload'] += bytessent

                if time.time()-client['lastmsgtime'] > 15:
                    # send heartbeat
                    conn.sendall(b'ping')
                    client['lastmsgtime'] = time.time()

                # clear watchdog
                client['watchdog'] = time.time_ns()
                time.sleep(0.001)
            except Exception as e:
                Logger.log.error(
                    'Client %s disconnected with error:%s' % (client['addr'], e))
                time.sleep(5)
                break
    
    @staticmethod
    async def websocket_publish_loop(client):
                
        Logger.log.info('Publishing updates of %s/%s/%s/%s -> %s' %
                        (client['database'], client['period'],
                         client['source'], client['tablename'], client['addr'][0]))
                
        conn = client['conn']
        records = client['records']
        while True:
            try:
                client, ids2send = SyncTable.get_ids2send(client)

                if len(ids2send) > 0:
                    rows2send = len(ids2send)
                    sentrows = 0
                    msgsize = min(client['maxrows'], rows2send)
                    bandwidth = client['bandwidth']
                    tini = time.time_ns()
                    bytessent = 0
                    while sentrows < rows2send:
                        t = time.time_ns()
                        message = records[ids2send[sentrows:sentrows +
                                                 msgsize]].tobytes()
                        compressed = lz4f.compress(message)
                        msgbytes = len(compressed)
                        bytessent+=msgbytes                        
                        msgmintime = msgbytes/bandwidth                        
                        await conn.send(compressed)
                        sentrows += msgsize
                        msgtime = (time.time_ns()-t)*1e-9
                        ratelimtime = max(msgmintime-msgtime, 0)
                        if ratelimtime > 0:
                            await asyncio.sleep(ratelimtime)

                    totalsize = (sentrows*records.itemsize)/1e6
                    totaltime = (time.time_ns()-tini)*1e-9
                    if totaltime > 0:
                        transfer_rate = totalsize/totaltime
                    else:
                        transfer_rate = 0
                    client['transfer_rate'] = transfer_rate
                    client['upload'] += msgbytes

                # clear watchdog
                client['watchdog'] = time.time_ns()
                await asyncio.sleep(0.001)
            except Exception as e:
                Logger.log.error(
                    'Client %s disconnected with error:%s' % (client['addr'], e))
                time.sleep(5)
                break
        
    # SUBSCRIBE    
    @staticmethod
    def table_subscribe_message(table, lookbacklines, lookbackdate, snapshot, bandwidth):
        shnumpy = table.records        
                
        key = os.environ['SHAREDDATA_SECRET_KEY'].encode()        
        cipher_suite = Fernet(key)
        cipher_token = cipher_suite.encrypt(os.environ['SHAREDDATA_TOKEN'].encode())
        msg = {
            'token': cipher_token.decode(),
            'action': 'subscribe',
            'database': table.database,
            'period': table.period,
            'source': table.source,
            'container': 'table',
            'tablename': table.tablename,
            'count': int(shnumpy.count),
            'mtime': float(shnumpy.mtime),
            'lookbacklines': lookbacklines,
            'bandwidth': bandwidth
        }
        if isinstance(lookbackdate, pd.Timestamp):            
            msg['lookbackdate'] = lookbackdate.strftime('%Y-%m-%d')
        if snapshot:
            msg['snapshot'] = True
        msg = json.dumps(msg)
        return msg
    
    @staticmethod
    def socket_subscription_loop(client):

        table = client['table']
        records = table.records
        client_socket = client['conn']

        bytes_buffer = bytearray()
        
        while True:
            try:
                # Receive data from the server
                data = SyncTable.recvall(client_socket, 4)                
                if (data == b'') | (data is None):
                    msg = 'Subscription %s,%s,%s,table,%s closed !' % \
                        (table.database, table.period,
                            table.source, table.tablename)
                    Logger.log.warning(msg)
                    client_socket.close()
                elif data==b'ping':
                    client['watchdog'] = time.time_ns()
                else:  
                    length = struct.unpack('!I', data)[0]       
                    client['download'] += length+4
                    compressed = SyncTable.recvall(client_socket, length)
                    if not compressed:
                        msg = 'Subscription %s,%s,%s,table,%s closed !' % \
                        (table.database, table.period,
                            table.source, table.tablename)
                        Logger.log.warning(msg)
                        client_socket.close()
                        raise Exception(msg)

                    data = lz4f.decompress(compressed)
                    bytes_buffer.extend(data)
                    bytes_buffer = records.read_stream(bytes_buffer)

            except Exception as e:
                msg = 'Subscription %s,%s,%s,table,%s error!\n%s' % \
                    (table.database, table.period,
                        table.source, table.tablename, str(e))
                Logger.log.error(msg)
                client_socket.close()                
                break
    
    @staticmethod
    async def websocket_subscription_loop(client):
        table = client['table']
        websocket = client['conn']
        shnumpy = table.records
        bytes_buffer = bytearray()

        while True:
            try:
                # Receive data from the server
                data = await websocket.recv()                
                if data == b'':
                    msg = 'Subscription %s,%s,%s,table,%s closed !' % \
                        (table.database, table.period,
                            table.source, table.tablename)
                    Logger.log.warning(msg)
                    websocket.close()
                else:
                    # Decompress the data
                    client['download'] += len(data)
                    data = lz4f.decompress(data)
                    bytes_buffer.extend(data)
                    bytes_buffer = shnumpy.read_stream(bytes_buffer)
                    
            except Exception as e:
                msg = 'Subscription %s,%s,%s,table,%s error!\n%s' % \
                    (table.database, table.period,
                     table.source, table.tablename, str(e))
                Logger.log.error(msg)
                websocket.close()
                break

    