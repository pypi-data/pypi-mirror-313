import os
import logging
import boto3
import time
import pytz
import json
from io import StringIO
from pathlib import Path
import pandas as pd
from datetime import datetime, timedelta, timezone
import numpy as np
import hashlib
import pymongo

from botocore.exceptions import ClientError
from SharedData.IO.MongoDBClient import MongoDBClient
from pymongo import IndexModel, ASCENDING, DESCENDING, TEXT


def add_auth_header(request, **kwargs):
    """
    Adds an Authorization header to the given HTTP request.
    
    Parameters:
    - request: The HTTP request object to which the Authorization header will be added.
    - **kwargs: Additional keyword arguments for future flexibility.
    """
    # Add the Authorization header
    token = os.environ['SHAREDDATA_TOKEN']
    request.headers['X-Custom-Authorization'] = token

def KinesisGetSession():
    if 'KINESIS_ACCESS_KEY_ID' in os.environ and 'KINESIS_SECRET_ACCESS_KEY' in os.environ:        
        _session = boto3.Session(
            aws_access_key_id=os.environ['KINESIS_ACCESS_KEY_ID'],
            aws_secret_access_key=os.environ['KINESIS_SECRET_ACCESS_KEY'],
            region_name=os.environ.get('KINESIS_DEFAULT_REGION','us-east-1'),
            botocore_session=boto3.Session()._session,  
        )                
    elif 'AWS_ACCESS_KEY_ID' in os.environ and 'AWS_SECRET_ACCESS_KEY' in os.environ:        
        _session = boto3.Session(
            aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
            region_name=os.environ.get('AWS_DEFAULT_REGION','us-east-1'),
            botocore_session=boto3.Session()._session,  # Use a separate botocore session
        )        
    elif 'KINESIS_AWS_PROFILE' in os.environ:
        _session = boto3.Session(profile_name=os.environ['KINESIS_AWS_PROFILE'])
    else:
        raise Exception('KINESIS_ACCESS_KEY_ID and KINESIS_SECRET_ACCESS_KEY or AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY or KINESIS_AWS_PROFILE must be set in environment variables')

    if 'KINESIS_ENDPOINT_URL' in os.environ:
        _kinesis = _session.client(
            'kinesis', endpoint_url=os.environ['KINESIS_ENDPOINT_URL'])
    else:
        _kinesis = _session.client('kinesis')

    if 'SHAREDDATA_TOKEN' in os.environ:
        _kinesis.meta.events.register(
            'before-sign.kinesis', add_auth_header)
    
    return _kinesis

# LOGS BUS
class KinesisLogStreamHandler(logging.StreamHandler):
    # reference: https://docs.python.org/3/library/logging.html#logging.LogRecord
    def __init__(self, user='guest'):
        # By default, logging.StreamHandler uses sys.stderr if stream parameter is not specified
        logging.StreamHandler.__init__(self)

        self.user = user
        self.stream_buffer = []
        self.client = None
        self.stream_name = os.environ['LOG_STREAMNAME']

        if not self.get_client():
            raise Exception('Logging failed check aws credentials!')

        self.create_stream()
        
    def get_client(self):
        success = False
        trials = 3
        while trials>0:
            trials-=1
            try:                
                self.client = KinesisGetSession()
                success = True
                break
            except Exception as e:
                print('Failed to connect to kinesis retying 1/%i\n%s' % (trials, e))
                time.sleep(1)
                pass
        return success

    def create_stream(self):

        try:
            self.client.create_stream(
                StreamName=self.stream_name,
                ShardCount=1,
                StreamModeDetails={
                    'StreamMode': 'PROVISIONED'
                }
            )
            time.sleep(10)
        except Exception as e:
            pass

    def emit(self, record):
        try:
            # msg = self.format(record)
            user = os.environ['USERNAME']+'@'+os.environ['COMPUTERNAME']            
            dt = datetime.fromtimestamp(record.created, timezone.utc)
            asctime = dt.strftime('%Y-%m-%dT%H:%M:%S%z')
            msg = {
                'user_name': user,
                'asctime': asctime,
                'logger_name': record.name,
                'level': record.levelname,
                'message': str(record.msg).replace('\'', '\"'),
                # 'function_name': record.funcName,
                # 'file_name': record.filename,
            }
            msg = json.dumps(msg)
            if self.client:
                self.stream_buffer.append({
                    'Data': str(msg).encode(encoding="UTF-8", errors="strict"),
                    'PartitionKey': user,
                })
            else:
                stream = self.stream
                stream.write(msg)
                stream.write(self.terminator)

            self.flush()
        except Exception:
            self.handleError(record)

    def flush(self):
        self.acquire()
        try:
            if self.client and self.stream_buffer:
                self.client.put_records(
                    StreamName=self.stream_name,
                    Records=self.stream_buffer
                )

                self.stream_buffer.clear()
        except Exception as e:
            print(f"An error occurred during flush operation.Stream buffer: {self.stream_buffer}")
            print(f"Exception: {e}")            

            if not self.get_client():
                raise Exception('Logging failed check aws credentials!')
            
        finally:
            if self.stream and hasattr(self.stream, "flush"):
                self.stream.flush()
            self.release()

class KinesisLogStreamConsumer():
    def __init__(self, user='guest', save_to_db=False):
        self.user = user        
        self.save_to_db = save_to_db

        self.mongodb = None
        if self.save_to_db:
            self.mongodb = MongoDBClient()
            self.db = self.mongodb.client['SharedData']
            if 'logs' not in self.db.list_collection_names():
                # Create logs collection as timeseries collection
                self.db.create_collection("logs", timeseries={
                    'timeField': "asctime",
                    'metaField': "metadata",
                    'granularity': "seconds"
                })

        self.dflogs = pd.DataFrame([],
                                   columns=['shardid', 'sequence_number', 'user_name', 'asctime', 'logger_name', 'level', 'message'])

        self.lastlogfilepath = Path(os.environ['DATABASE_FOLDER']) / 'Logs'
        self.lastlogfilepath = self.lastlogfilepath / \
            ((datetime.utcnow() + timedelta(days=-1)).strftime('%Y%m%d')+'.log')
        self.last_day_read = False

        self.logfilepath = Path(os.environ['DATABASE_FOLDER']) / 'Logs'
        self.logfilepath = self.logfilepath / \
            (datetime.utcnow().strftime('%Y%m%d')+'.log')
        self.logfileposition = 0

        self.readLogs()

    def read_last_day_logs(self):
        self.last_day_read = True
        if self.lastlogfilepath.is_file():
            try:
                _dflogs = pd.read_csv(self.lastlogfilepath, header=None, sep=';',
                                      engine='python', on_bad_lines='skip')
                _dflogs.columns = ['shardid', 'sequence_number',
                                   'user_name', 'asctime', 'logger_name', 'level', 'message']
                self.dflogs = pd.concat([_dflogs, self.dflogs], axis=0)
            except:
                pass

    def readLogs(self):
        if not self.last_day_read:
            self.read_last_day_logs()

        _logfilepath = Path(os.environ['DATABASE_FOLDER']) / 'Logs'
        _logfilepath = _logfilepath / \
            (datetime.utcnow().strftime('%Y%m%d')+'.log')
        if self.logfilepath != _logfilepath:
            self.logfileposition = 0
            self.logfilepath = _logfilepath

        if self.logfilepath.is_file():
            try:
                with open(self.logfilepath, 'r') as file:
                    file.seek(self.logfileposition)
                    newlines = '\n'.join(file.readlines())
                    dfnewlines = pd.read_csv(StringIO(newlines), header=None, sep=';',
                                             engine='python', on_bad_lines='skip')
                    dfnewlines.columns = [
                        'shardid', 'sequence_number', 'user_name', 'asctime', 'logger_name', 'level', 'message']
                    self.dflogs = pd.concat([self.dflogs, dfnewlines])
                    self.logfileposition = file.tell()
            except:
                pass

        return self.dflogs

    def getLogs(self):
        df = self.readLogs()
        if not df.empty:
            idxhb = np.array(['#heartbeat#' in s for s in df['message'].astype(str)])
            idshb = np.where(idxhb)[0]
            if len(idshb > 100):
                idshb = idshb[-100:]
            ids = np.where(~idxhb)[0]
            ids = np.sort([*ids, *idshb])
            df = df.iloc[ids, :]
        return df

    def connect(self):
        try:            
            self.client = KinesisGetSession()
        except:
            print('Could not connect to AWS!')
            return False

        try:
            print("Trying to create stream %s..." %
                  (os.environ['LOG_STREAMNAME']))
            self.client.create_stream(
                StreamName=os.environ['LOG_STREAMNAME'],
                ShardCount=1,
                StreamModeDetails={
                    'StreamMode': 'PROVISIONED'
                }
            )
            time.sleep(10)
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceInUseException':
                print("Stream already exists")
            else:
                print("Trying to create stream unexpected error: %s" % e)
                pass

        try:
            self.stream = self.client.describe_stream(
                StreamName=os.environ['LOG_STREAMNAME'])
        except:
            print('Could not describe stream!')
            return False

        if self.stream and 'StreamDescription' in self.stream:
            self.stream = self.stream['StreamDescription']
            for i in range(len(self.stream['Shards'])):
                readfromstart = True
                shardid = self.stream['Shards'][i]['ShardId']
                if not self.dflogs.empty and (shardid in self.dflogs['shardid'].values):
                    readfromstart = False
                    seqnum = self.dflogs[self.dflogs['shardid']
                                         == shardid].iloc[-1]['sequence_number']
                    try:
                        shard_iterator = self.client.get_shard_iterator(
                            StreamName=self.stream['StreamName'],
                            ShardId=self.stream['Shards'][i]['ShardId'],
                            ShardIteratorType='AFTER_SEQUENCE_NUMBER',
                            StartingSequenceNumber=seqnum
                        )
                    except:
                        print(
                            'Failed retrieving shard iterator, reading from start...')
                        readfromstart = True
                
                if readfromstart:
                    print('############### READING FROM START ###############')                    
                    if 'KINESALITE' in os.environ:
                        shard_iterator = self.client.get_shard_iterator(
                            StreamName=self.stream['StreamName'],
                            ShardId=self.stream['Shards'][i]['ShardId'],                            
                            ShardIteratorType='LATEST'                            
                        )
                        
                    else:
                        start_of_day = pd.Timestamp.utcnow().floor('D').timestamp()

                        shard_iterator = self.client.get_shard_iterator(
                                            StreamName=self.stream['StreamName'],
                                            ShardId=self.stream['Shards'][i]['ShardId'],
                                            ShardIteratorType='AT_TIMESTAMP',
                                            Timestamp=start_of_day
                                        )
                    
                self.stream['Shards'][i]['ShardIterator'] = shard_iterator['ShardIterator']
        else:
            print('Failed connecting StreamDescriptor not found!')
            return False

        return True

    def consume(self):
        try:
            for i in range(len(self.stream['Shards'])):
                response = self.client.get_records(
                    ShardIterator=self.stream['Shards'][i]['ShardIterator'],
                    Limit=1000)
                self.stream['Shards'][i]['ShardIterator'] = response['NextShardIterator']
                if len(response['Records']) > 0:
                    for r in response['Records']:
                        try:
                            rec = r['Data'].decode(
                                encoding="UTF-8", errors="strict")
                            rec = json.loads(rec.replace(
                                "\'", "\"").replace(';', ','))

                            line = '%s;%s;%s;%s;%s;%s;%s' % (self.stream['Shards'][i]['ShardId'],
                                                             r['SequenceNumber'], rec['user_name'], rec['asctime'],
                                                             rec['logger_name'], rec['level'], rec['message'])

                            dt = datetime.strptime(
                                rec['asctime'][:-5], '%Y-%m-%dT%H:%M:%S')

                            logfilepath = Path(
                                os.environ['DATABASE_FOLDER']) / 'Logs'
                            logfilepath = logfilepath / \
                                (dt.strftime('%Y%m%d')+'.log')
                            if not logfilepath.parents[0].is_dir():
                                os.makedirs(logfilepath.parents[0])
                            
                            with open(logfilepath, 'a+', encoding='utf-8') as f:
                                f.write(line.replace(
                                    '\n', ' ').replace('\r', ' ')+'\n')
                                f.flush()

                            if self.save_to_db:
                                # Parse asctime string to datetime with timezone info
                                asctime_str = rec['asctime']
                                asctime = datetime.strptime(asctime_str, '%Y-%m-%dT%H:%M:%S%z')
                                # Insert into MongoDB
                                document = {
                                    "asctime": asctime,
                                    "metadata": {
                                        "user_name": rec['user_name'].replace('\\','/'),
                                        "logger_name": rec['logger_name'].replace('\\','/'),
                                        "level": rec['level']
                                    },
                                    "message": rec['message'],
                                    "shard_id": self.stream['Shards'][i]['ShardId'],
                                    "sequence_number": r['SequenceNumber']
                                }                                
                                unique_string = asctime_str + document['sequence_number'] + document['shard_id']
                                _id = hashlib.sha256(unique_string.encode('utf-8')).hexdigest()
                                document['_id'] = _id
                                try:
                                    self.db.logs.insert_one(document)
                                except pymongo.errors.DuplicateKeyError:
                                    print(f"Document with _id {_id} already exists in the collection.")
                                except Exception as e:
                                    print(f"An error occurred inserting to mongodb: {e}")

                        except Exception as e:
                            print('Invalid record:%s\nerror:%s' %
                                  (str(rec), str(e)))
            return True
        except:
            return False


# WORKER BUS
class KinesisStreamProducer():
    def __init__(self, stream_name):
        self.stream_name = stream_name
        self.client = None
        self.stream_buffer = []
        try:            
            self.client = KinesisGetSession()
        except Exception:
            print('Kinesis client initialization failed.')

        try:
            self.client.create_stream(
                StreamName=stream_name,
                ShardCount=1,
                StreamModeDetails={
                    'StreamMode': 'PROVISIONED'
                }
            )
            time.sleep(10)
        except Exception as e:
            pass

    def produce(self, record, partitionkey):        
        _rec = json.dumps(record)
        self.stream_buffer.append({
            'Data': str(_rec).encode(encoding="UTF-8", errors="strict"),
            'PartitionKey': partitionkey,
        })
        trials = 3
        while trials > 0:
            try:
                self.client.put_records(
                    StreamName=self.stream_name,
                    Records=self.stream_buffer
                )
                break
            except:
                self.client = KinesisGetSession()
                trials -= 1
        self.stream_buffer = []

class KinesisStreamConsumer():
    def __init__(self, stream_name):
        self.stream_name = stream_name
        self.stream_buffer = []
        self.last_sequence_number = None
        self.get_stream()

    def get_stream(self):
        self.client = KinesisGetSession()

        try:
            self.client.create_stream(
                StreamName=self.stream_name,
                ShardCount=1,
                StreamModeDetails={
                    'StreamMode': 'PROVISIONED'
                }
            )
            time.sleep(10)
        except Exception as e:
            pass
        
        while True:
            try:
                self.stream = self.client.describe_stream(StreamName=self.stream_name)
                if self.stream and 'StreamDescription' in self.stream:
                    self.stream = self.stream['StreamDescription']
                    i = 0
                    for i in range(len(self.stream['Shards'])):
                        shardid = self.stream['Shards'][i]['ShardId']
                        if self.last_sequence_number is None:
                            shard_iterator = self.client.get_shard_iterator(
                                StreamName=self.stream['StreamName'],
                                ShardId=shardid,
                                ShardIteratorType='LATEST'
                            )
                        else:
                            try:
                                shard_iterator = self.client.get_shard_iterator(
                                    StreamName=self.stream['StreamName'],
                                    ShardId=shardid,
                                    ShardIteratorType='AFTER_SEQUENCE_NUMBER',
                                    StartingSequenceNumber=self.last_sequence_number
                                )
                            except:
                                print('############### RESETING SHARD ITERATOR SEQUENCE ###############')
                                shard_iterator = self.client.get_shard_iterator(
                                    StreamName=self.stream['StreamName'],
                                    ShardId=shardid,
                                    ShardIteratorType='LATEST'
                                )

                        self.stream['Shards'][i]['ShardIterator'] = shard_iterator['ShardIterator']

                if self.stream['StreamStatus'] != 'ACTIVE':
                    raise Exception('Stream status %s' % (self.stream['StreamStatus']))                
                
                return True
            except Exception as e:
                print('Failed connecting StreamDescriptor not found!')
                print('Exception: %s' % (e))
                self.client = KinesisGetSession()
                time.sleep(1)                
        

    def consume(self):
        success = False

        for i in range(len(self.stream['Shards'])):
            try:
                response = self.client.get_records(
                    ShardIterator=self.stream['Shards'][i]['ShardIterator'],
                    Limit=100)
                success = True
                self.stream['Shards'][i]['ShardIterator'] = response['NextShardIterator']
                if len(response['Records']) > 0:
                    for r in response['Records']:
                        try:
                            rec = json.loads(r['Data'])
                            self.last_sequence_number = r['SequenceNumber']
                            self.stream_buffer.append(rec)
                        except Exception as e:
                            print('Invalid record:'+str(r['Data']))
                            print('Invalid record:'+str(e))

            except Exception as e:
                print('Kinesis consume exception:%s' % (e))
                break

        return success
