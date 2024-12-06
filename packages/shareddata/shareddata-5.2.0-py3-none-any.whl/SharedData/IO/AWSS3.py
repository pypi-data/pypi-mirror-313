import os
import sys
import logging
import subprocess
import boto3
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, timezone
import time
import pytz
import io
from tqdm import tqdm

from SharedData.Logger import Logger
from SharedData.MultiProc import io_bound_process


def S3GetSession(isupload=False):

    if 'S3_ACCESS_KEY_ID' in os.environ and 'S3_SECRET_ACCESS_KEY' in os.environ:
        if 'AWS_PROFILE' in os.environ:
            del os.environ['AWS_PROFILE']
        _session = boto3.Session(
            aws_access_key_id=os.environ['S3_ACCESS_KEY_ID'],
            aws_secret_access_key=os.environ['S3_SECRET_ACCESS_KEY'],
            region_name=os.environ.get('S3_DEFAULT_REGION','us-east-1'),
        )        
    elif 'AWS_ACCESS_KEY_ID' in os.environ and 'AWS_SECRET_ACCESS_KEY' in os.environ:
        if 'AWS_PROFILE' in os.environ:
            del os.environ['AWS_PROFILE']
        _session = boto3.Session(
            aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
            region_name=os.environ.get('AWS_DEFAULT_REGION','us-east-1'),
        )
    elif 'S3_AWS_PROFILE' in os.environ:
        _session = boto3.Session(profile_name=os.environ['S3_AWS_PROFILE'])
    else:
        raise Exception('S3_ACCESS_KEY_ID and S3_SECRET_ACCESS_KEY or AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY or S3_AWS_PROFILE must be set in environment variables')

    if 'S3_ENDPOINT_URL' in os.environ:
        _s3 = _session.resource(
            's3', endpoint_url=os.environ['S3_ENDPOINT_URL'])
    else:
        _s3 = _session.resource('s3')
    _bucket = _s3.Bucket(os.environ['S3_BUCKET'].replace('s3://', ''))
    return _s3, _bucket


def S3ListFolder(prefix):
    s3, bucket = S3GetSession()
    keys = np.array(
        [obj_s.key for obj_s in bucket.objects.filter(Prefix=prefix)])
    return keys


def S3Download(remote_path, local_path=None, \
        force_download=False, local_mtime=None,database_folder=None):
    bucket_name = os.environ['S3_BUCKET'].replace('s3://', '')
    if database_folder:
        if database_folder.endswith('/'):
            database_folder = database_folder[:-1]
        s3_path = str(remote_path).replace(database_folder, '').replace('\\', '/')[1:]
    else:
        s3_path = str(remote_path).replace(
            os.environ['DATABASE_FOLDER'], '').replace('\\', '/')[1:]
    s3, bucket = S3GetSession()
    # load obj
    obj = s3.Object(bucket_name, s3_path)
    remote_mtime = None
    try:
        # remote mtime
        remote_mtime = obj.last_modified.timestamp()
        if 'mtime' in obj.metadata:
            remote_mtime = float(obj.metadata['mtime'])
        remote_exists = True
    except:
        # remote file dont exist
        remote_exists = False

    local_exists = False
    if not local_path is None:
        remote_isnewer = False
        local_exists = os.path.isfile(str(local_path))
        local_mtime = None
        if local_exists:
            # local mtime
            local_mtime = datetime.fromtimestamp(os.path.getmtime(local_path)).timestamp()            
    elif not local_mtime is None:        
        local_exists = True

    remote_isnewer = False
    if (local_exists) & (remote_exists):
        # compare
        remote_isnewer = remote_mtime > local_mtime

    if remote_exists:
        if (not local_exists) | (remote_isnewer) | (force_download):
            # get object size for progress bar
            obj_size = obj.content_length / (1024*1024)  # in MB
            description = 'Downloading:%iMB, %s' % (obj_size, s3_path)
            io_obj = io.BytesIO()
            try:
                if obj_size > 50:
                    with tqdm(total=obj_size, unit='MB', unit_scale=True,\
                               desc=description) as pbar:
                        obj.download_fileobj(io_obj,
                            Callback=lambda bytes_transferred: \
                                pbar.update(bytes_transferred/(1024*1024)))
                else:
                    obj.download_fileobj(io_obj)
                return [io_obj, local_mtime, remote_mtime]
            except Exception as e:
                raise Exception('downloading %s,%s ERROR!\n%s' %
                                (Logger.user, remote_path, str(e)))

    return [None, local_mtime, remote_mtime]


def UpdateModTime(local_path, remote_mtime):
    # update modification time to remote mtime 
    remote_mtime_local_tz_ts = datetime.fromtimestamp(remote_mtime, timezone.utc).timestamp()
    os.utime(local_path, (remote_mtime_local_tz_ts, remote_mtime_local_tz_ts))


def S3SaveLocal(local_path, io_obj, remote_mtime):
    path = Path(local_path)
    if not path.parent.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
    with open(local_path, 'wb') as f:
        f.write(io_obj.getbuffer())
        f.flush()
    # update modification time
    remote_mtime_local_tz_ts = datetime.fromtimestamp(remote_mtime, timezone.utc).timestamp()
    os.utime(local_path, (remote_mtime_local_tz_ts, remote_mtime_local_tz_ts))


def S3Upload(file_io, path, mtime, database_folder=None):
    if database_folder:
        if database_folder.endswith('/'):
            database_folder = database_folder[:-1]
        remotefilepath = str(path).replace(
            database_folder, os.environ['S3_BUCKET'])
    else:
        remotefilepath = str(path).replace(
            os.environ['DATABASE_FOLDER'], os.environ['S3_BUCKET'])
    remotefilepath = remotefilepath.replace('\\', '/')

    # Check the file size
    file_size = file_io.seek(0, os.SEEK_END) / (1024*1024)  # in MB
    file_name = remotefilepath.replace(os.environ['S3_BUCKET'], '')[1:]
    description = 'Uploading:%iMB, %s' % (file_size, file_name)

    trials = 3
    success = False
    file_io.close = lambda: None  # prevents boto3 from closing io
    while trials > 0:
        try:
            s3, bucket = S3GetSession(isupload=True)
            mtime_utc = datetime.fromtimestamp(mtime, timezone.utc).timestamp()
            mtime_str = str(mtime_utc)

            file_io.seek(0)
            if file_size > 50:
                with tqdm(total=file_size, unit='MB', unit_scale=True, desc=description) as pbar:
                    bucket.upload_fileobj(file_io, file_name,
                                          ExtraArgs={'Metadata': {
                                              'mtime': mtime_str}},
                                          Callback=lambda bytes_transferred: pbar.update(bytes_transferred/(1024*1024)))
            else:
                bucket.upload_fileobj(file_io, file_name, ExtraArgs={
                                      'Metadata': {'mtime': mtime_str}})
            success = True
            break
        except Exception as e:
            Logger.log.warning(Logger.user+' Uploading to S3 '+path +
                               ' FAILED! retrying(%i,3)...\n%s ' % (trials, str(e)))
            trials = trials - 1

    if not success:
        Logger.log.error(Logger.user+' Uploading to S3 '+path+' ERROR!')
        raise Exception(Logger.user+' Uploading to S3 '+path+' ERROR!')


def S3SyncUpload(file_io, path, mtime, database_folder=None):        
    if database_folder:
        remotefilepath = str(path).replace(
            database_folder, os.environ['S3_BUCKET'])
    else:
        remotefilepath = str(path).replace(
            os.environ['DATABASE_FOLDER'], os.environ['S3_BUCKET'])
    remotefilepath = remotefilepath.replace('\\', '/')
    bucket_name = os.environ['S3_BUCKET'].replace('s3://', '')
    if database_folder:
        s3_path = str(remotefilepath).replace(database_folder, '').replace('\\', '/')[1:]
    else:
        s3_path = str(remotefilepath).replace(
            os.environ['DATABASE_FOLDER'], '').replace('\\', '/')[1:]
    
    # Check the file size
    file_size = file_io.seek(0, os.SEEK_END) / (1024*1024)  # in MB
    file_name = remotefilepath.replace(os.environ['S3_BUCKET'], '')[1:]
    description = 'Uploading:%iMB, %s' % (file_size, file_name)

    trials = 3
    success = False
    file_io.close = lambda: None  # prevents boto3 from closing io
    while trials > 0:
        try:
            s3, bucket = S3GetSession(isupload=True)
            # local mtime
            mtime_utc = datetime.fromtimestamp(mtime,timezone.utc).timestamp()
            mtime_str = str(mtime_utc)

            # load obj
            obj = s3.Object(bucket_name, s3_path)
            remote_mtime = None
            try:
                # remote mtime
                remote_mtime = obj.last_modified.timestamp()
                if 'mtime' in obj.metadata:
                    remote_mtime = float(obj.metadata['mtime'])
                remote_exists = True
            except:
                # remote file dont exist
                remote_exists = False
            
            remote_isnewer = False
            if remote_exists:
                # compare
                remote_isnewer = remote_mtime >= mtime_utc

            if not remote_isnewer:
                file_io.seek(0)
                if file_size > 50:
                    with tqdm(total=file_size, unit='MB', unit_scale=True, desc=description) as pbar:
                        bucket.upload_fileobj(file_io, file_name,
                                            ExtraArgs={'Metadata': {
                                                'mtime': mtime_str}},
                                            Callback=lambda bytes_transferred: pbar.update(bytes_transferred/(1024*1024)))
                else:
                    bucket.upload_fileobj(file_io, file_name, ExtraArgs={
                                        'Metadata': {'mtime': mtime_str}})
            success = True
            break
        except Exception as e:
            Logger.log.warning(Logger.user+' Uploading to S3 '+path +
                               ' FAILED! retrying(%i,3)...\n%s ' % (trials, str(e)))
            trials = trials - 1

    if not success:
        Logger.log.error(Logger.user+' Uploading to S3 '+path+' ERROR!')
        raise Exception(Logger.user+' Uploading to S3 '+path+' ERROR!')


def S3DeleteTable(remote_path):
    try:    
        s3, bucket = S3GetSession()
        objects_to_delete = bucket.objects.filter(Prefix=remote_path)
        delete_us = []
        for obj in objects_to_delete:
            if (remote_path+'/head.bin.gzip' == obj.key)\
                or (remote_path+'/tail.bin.gzip' == obj.key):
                delete_us.append({'Key': obj.key})
        # Batch deletes to avoid errors caused by long delete lists
        batch_size = 1000  # Adjust if necessary
        for i in range(0, len(delete_us), batch_size):
            batch = delete_us[i:i+batch_size]
            bucket.delete_objects(Delete={'Objects': batch})
    except Exception as e:
        Logger.log.error(f"S3Delete {remote_path} ERROR!\n{str(e)}")
        raise Exception(f"S3Delete {remote_path} ERROR!\n{str(e)}")
    

def S3DeleteTimeseries(remote_path):
    try:    
        s3, bucket = S3GetSession()
        objects_to_delete = bucket.objects.filter(Prefix=remote_path)
        delete_us = []
        for obj in objects_to_delete:
            if (remote_path+'/timeseries_head.bin.gzip' == obj.key)\
                or (remote_path+'/timeseries_tail.bin.gzip' == obj.key):
                delete_us.append({'Key': obj.key})
        # Batch deletes to avoid errors caused by long delete lists
        batch_size = 1000  # Adjust if necessary
        for i in range(0, len(delete_us), batch_size):
            batch = delete_us[i:i+batch_size]
            bucket.delete_objects(Delete={'Objects': batch})
    except Exception as e:
        Logger.log.error(f"S3Delete {remote_path} ERROR!\n{str(e)}")
        raise Exception(f"S3Delete {remote_path} ERROR!\n{str(e)}")
    
def S3DeleteFolder(remote_path):    
    try:    
        s3, bucket = S3GetSession()
        objects_to_delete = bucket.objects.filter(Prefix=remote_path)
        delete_us = []
        for obj in objects_to_delete:
            delete_us.append({'Key': obj.key})
        # Batch deletes to avoid errors caused by long delete lists
        batch_size = 1000  # Adjust if necessary
        for i in range(0, len(delete_us), batch_size):
            batch = delete_us[i:i+batch_size]
            bucket.delete_objects(Delete={'Objects': batch})
    except Exception as e:
        Logger.log.error(f"S3Delete {remote_path} ERROR!\n{str(e)}")
        raise Exception(f"S3Delete {remote_path} ERROR!\n{str(e)}")
    

def S3GetMtime(remote_path):
    bucket_name = os.environ['S3_BUCKET'].replace('s3://', '')
    s3_path = str(remote_path).replace(
        os.environ['DATABASE_FOLDER'], '').replace('\\', '/')[1:]
    s3, bucket = S3GetSession()
    # load obj
    obj = s3.Object(bucket_name, s3_path)
    remote_mtime = None
    try:
        # remote mtime
        remote_mtime = obj.last_modified.timestamp()
        if 'mtime' in obj.metadata:
            remote_mtime = float(obj.metadata['mtime'])
    except Exception as e:
        # print(e)
        # remote file dont exist
        pass
    return remote_mtime