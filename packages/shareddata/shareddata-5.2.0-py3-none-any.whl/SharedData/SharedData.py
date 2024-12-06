import os
import psutil
import pandas as pd
import numpy as np
import json
import warnings
import time
import shutil
from datetime import datetime, timezone

from multiprocessing import shared_memory
from pathlib import Path
import importlib.metadata

# Ignore the "invalid value encountered in cast" warning
warnings.filterwarnings("ignore", message="invalid value encountered in cast")
# warnings.filterwarnings("ignore", category=RuntimeWarning)

import SharedData.Defaults as Defaults
from SharedData.Logger import Logger
from SharedData.TableMemory import TableMemory
from SharedData.TableDisk import TableDisk
from SharedData.TimeseriesContainer import TimeseriesContainer
from SharedData.TimeSeriesMemory import TimeSeriesMemory
from SharedData.TimeSeriesDisk import TimeSeriesDisk
from SharedData.Utils import datetype
from SharedData.IO.AWSS3 import S3ListFolder, S3GetSession, S3DeleteTable, S3DeleteTimeseries
from SharedData.Utils import remove_shm_from_resource_tracker, cpp
from SharedData.MultiProc import io_bound_unordered
from SharedData.IO.MongoDBClient import MongoDBClient
from SharedData.Database import DATABASE_PKEYS

# TODO: MISSING SEMAPHORE FOR TIMESERIES
# TODO: ADD SHUTDOWN COMMAND TO WORKERS
class SharedData:    

    def __init__(self, source, 
                 user='guest',access_key_id=None,secret_access_key=None, quiet=False):
        self.source = source
        self.user = user
        if not access_key_id is None:
            os.environ['AWS_ACCESS_KEY_ID'] = access_key_id
            if not secret_access_key is None:
                os.environ['AWS_SECRET_ACCESS_KEY'] = secret_access_key
            else:
                raise Exception('secret_access_key is None')
        
        # DATA DICTIONARY
        self.data = {}

        # MONGODB VARIABLES
        self._mongodb = None

        # LOGIN VARIABLES
        self.islogged = False
        self.source = source
        self.user = user   
        
        # Ie. "/nvme0/db,/nvme1/db,..."
        self.dbfolders = [os.environ['DATABASE_FOLDER']]
        if 'DATABASE_FOLDERS' in os.environ.keys():
            _dbfolders = os.environ['DATABASE_FOLDERS'].split(',')
            self.dbfolders = list(np.unique(list(_dbfolders)+self.dbfolders))    
        
        # CONNEC TO LOGGER
        Logger.connect(self.source, self.user)

        # REMOVES SHARED MEMORY FROM RESOURCE TRACKER
        if (os.name == 'posix'):
            remove_shm_from_resource_tracker()
        
        # INIT TABLE SCHEMA
        self.init_schema()

        if not self.islogged:
            self.islogged = True
            if not quiet:
                try:
                    SHAREDDATA_VERSION = importlib.metadata.version("shareddata")
                    Logger.log.info('User:%s,SharedData:%s CONNECTED!' %
                                    (self.user, SHAREDDATA_VERSION))
                except:
                    Logger.log.info('User:%s CONNECTED!' % (self.user))
        
    ###############################################
    ############# DATA CONTAINERS #################
    ###############################################
    
    ############# TABLE #################
    def table(self, database, period, source, tablename,
            names=None, formats=None, size=None, hasindex=True,\
            value=None, user='master', overwrite=False,\
            type='DISK', partitioning=None):
        
        if not database in DATABASE_PKEYS:
            errmsg = f'Invalid database {database}'
            raise Exception(errmsg)
        
        path = f'{user}/{database}/{period}/{source}/table/{tablename}'
        if not path in self.data.keys():
            if type == 'DISK':
                self.data[path] = TableDisk(self, database, period, source,
                                        tablename, records=value, names=names, formats=formats, size=size, hasindex=hasindex,
                                        user=user, overwrite=overwrite, partitioning=partitioning)
            elif type == 'MEMORY':
                self.data[path] = TableMemory(self, database, period, source,
                                        tablename, records=value, names=names, formats=formats, size=size, hasindex=hasindex,
                                        user=user, overwrite=overwrite)
            
        return self.data[path].records

    ############# TIMESERIES #################
    def timeseries(self, database, period, source, tag=None, user='master',
                   startDate=None,type='DISK',
                   columns=None, value=None, overwrite=False): # tags params

        path = f'{user}/{database}/{period}/{source}/timeseries'
        if not path in self.data.keys():
            self.data[path] = TimeseriesContainer(self, database, period, source, 
                user=user, type=type, startDate=startDate)
            
        if not startDate is None:
            if self.data[path].startDate != startDate:
                raise Exception('Timeseries startDate is already set to %s' %
                                self.data[path].startDate)
            
        if tag is None:
            return self.data[path]
                    
        if (overwrite) | (not tag in self.data[path].tags.keys()):
            if (columns is None) & (value is None):
                self.data[path].load()
                if not tag in self.data[path].tags.keys():
                    errmsg = 'Tag %s/%s doesnt exist' % (path, tag)
                    Logger.log.error(errmsg)                    
                    raise Exception(errmsg)
            else:
                if self.data[path].type == 'DISK':
                    self.data[path].tags[tag] = TimeSeriesDisk(
                        self, self.data[path],database, period, source, tag,
                        value=value, columns=columns, user=user,
                        overwrite=overwrite)                    
                elif self.data[path].type == 'MEMORY':
                    if overwrite == True:
                        raise Exception('Overwrite is not supported for MEMORY type')                    
                    self.data[path].tags[tag] = TimeSeriesMemory(
                        self, self.data[path],database, period, source, tag,
                        value=value, columns=columns, user=user)
                

        return self.data[path].tags[tag].data

    ############# DATAFRAME #################
    def dataframe(self, database, period, source,
                  date=None, value=None, user='master'):
        pass

    ###############################################
    ######### SHARED MEMORY MANAGEMENT ############
    ###############################################    
    def init_schema(self):
        self.schema = None

        # DB TABLES
        names = [
            'symbol', 'mtime', 
            'last_scan_local','folder_local', 'created_local', 'last_modified_local', 'mtime_local', 'mtime_head_local', 'mtime_tail_local', 'size_local', 'files_local',
            'mutex_pid', 'mutex_type', 'mutex_isloaded',
            'last_scan_remote','folder_remote', 'last_modified_remote', 'mtime_remote', 'mtime_head_remote', 'mtime_tail_remote', 'size_remote', 'files_remote','storage_class_remote',
            'user', 'database', 'period', 'source', 'container', 'tablename','partition', 'partitioning_period',
            'names', 'formats', 'size', 'hasindex', 'type'
        ]

        formats = [
            '|S128', '<M8[ns]',  # symbol, mtime
            '<M8[ns]', '|S32', '<M8[ns]', '<M8[ns]', '<M8[ns]', '<M8[ns]', '<M8[ns]', '<f8', '<i4',  # local fields
            '<i8', '<i8', '<i8', # mutex fields
            '<M8[ns]', '|S32', '<M8[ns]', '<M8[ns]', '<M8[ns]', '<M8[ns]', '<f8', '<i4', '|S32',  # remote fields 
            '|S32', '|S32', '|S16', '|S32', '|S32', '|S64', '|S32', '|S16',  # metadata fields
            '|S256', '|S128', '<i8', '<i4', '|S16' # schema fields
        ]

        computername = os.environ['COMPUTERNAME']
        self.schema = self.table('Symbols','D1','SCHEMA',computername,
            names=names,formats=formats,size=100e3)
            
    @staticmethod
    def mutex(shm_name, pid):        
        dtype_mutex = np.dtype({'names': ['pid', 'type', 'isloaded'],\
                                'formats': ['<i8', '<i8', '<i8']})
        try:
            shm_mutex = shared_memory.SharedMemory(
                name=shm_name + '#mutex', create=True, size=dtype_mutex.itemsize)
            ismalloc = False
        except:                                            
            shm_mutex = shared_memory.SharedMemory(
                name=shm_name + '#mutex', create=False)
            ismalloc = True        
        mutex = np.ndarray((1,), dtype=dtype_mutex,buffer=shm_mutex.buf)[0]        
        SharedData.acquire(mutex, pid, shm_name)        
        # register process id access to memory
        fpath = Path(os.environ['DATABASE_FOLDER'])
        fpath = fpath/('shm/'+shm_name.replace('\\', '/')+'#mutex.csv')
        os.makedirs(fpath.parent, exist_ok=True)
        with open(fpath, "a+") as f:
            f.write(str(pid)+',')
        return [shm_mutex, mutex, ismalloc]
    
    @staticmethod
    def acquire(mutex, pid, relpath):
        tini = time.time()
        # semaphore is process safe
        telapsed = 0
        hdrptr = mutex.__array_interface__['data'][0]
        semseek = 0
        firstcheck = True
        while cpp.long_compare_and_swap(hdrptr, semseek, 0, pid) == 0:
            # check if process that locked the mutex is still running
            telapsed = time.time() - tini
            if (telapsed > 15) | ((firstcheck) & (telapsed > 1)):
                lockingpid = mutex['pid']
                if not psutil.pid_exists(lockingpid):
                    if cpp.long_compare_and_swap(hdrptr, semseek, lockingpid, pid) != 0:
                        break
                if not firstcheck:
                    Logger.log.warning('%s waiting for semaphore...' % (relpath))
                tini = time.time()
                firstcheck = False
            time.sleep(0.000001)

    @staticmethod
    def release(mutex, pid, relpath):
        hdrptr = mutex.__array_interface__['data'][0]
        semseek = 0
        if cpp.long_compare_and_swap(hdrptr, semseek, pid, 0) != 1:
            errmsg = '%s Tried to release semaphore without acquire!' % (relpath)
            Logger.log.error(errmsg)
            raise Exception(errmsg)

    # TODO: check free memory before allocate    
    @staticmethod
    def malloc(shm_name, create=False, size=None):
        ismalloc = False
        shm = None
        if not create:
            try:
                shm = shared_memory.SharedMemory(
                    name=shm_name, create=False)
                ismalloc = True
            except:
                pass            
        elif (create) & (not size is None):
            try:
                shm = shared_memory.SharedMemory(
                    name=shm_name, create=True, size=size)                
                ismalloc = False
            except:                                            
                shm = shared_memory.SharedMemory(
                    name=shm_name, create=False)
                ismalloc = True
                
        elif (create) & (size is None):
            raise Exception(
                'SharedData malloc must have a size when create=True')
        
        # register process id access to memory
        fpath = Path(os.environ['DATABASE_FOLDER'])
        fpath = fpath/('shm/'+shm_name.replace('\\', '/')+'.csv')
        os.makedirs(fpath.parent, exist_ok=True)
        pid = os.getpid()
        with open(fpath, "a+") as f:
            f.write(str(pid)+',')

        return [shm, ismalloc]

    @staticmethod
    def free(shm_name):
        if os.name == 'posix':
            try:
                shm = shared_memory.SharedMemory(
                    name=shm_name, create=False)
                shm.close()
                shm.unlink()
                fpath = Path(os.environ['DATABASE_FOLDER'])
                fpath = fpath/('shm/'+shm_name.replace('\\', '/')+'.csv')
                if fpath.is_file():
                    os.remove(fpath)
            except:
                pass

    @staticmethod
    def freeall():
        shm_names = SharedData.list_memory()
        for shm_name in shm_names.index:
            SharedData.free(shm_name)

    ######### LIST ############    
    def list_all(self, keyword='', user='master', list_timeseries=True):
                        
        dfremote = self.list_remote(keyword,user=user)

        dflocal = self.list_local(keyword,user=user)
                        
        ls = dfremote.copy()
        ls = ls.reindex(index=ls.index.union(dflocal.index),
                        columns=ls.columns.union(dflocal.columns))
        ls.loc[dflocal.index,dflocal.columns] = dflocal.values

        if len(ls)>0:
            ls = ls.reindex(columns=['folder_local', 'created_local', 'last_modified_local','size_local','files_local',
                    'folder_remote', 'last_modified_remote', 'size_remote', 'files_remote','storage_class_remote',
                    'user','database','period','source','container', 'tablename','partition'])            
            ls['partitioning_period'] = ls['partition'].apply(lambda x: datetype(x))
            # fill nans local
            ls['folder_local'] = ls['folder_local'].fillna('')
            ls['created_local'] = pd.to_datetime(ls['created_local'])
                        
            # idx = ls['last_modified_local']>datetime.now(timezone.utc)
            # ls.loc[idx,'last_modified_local'] = datetime.now(timezone.utc)

            ls['last_modified_local'] = pd.to_datetime(ls['last_modified_local'])
            ls['size_local'] = ls['size_local'].fillna(0)
            ls['files_local'] = ls['files_local'].fillna(0)
            # fill nans remote
            ls['folder_remote'] = ls['folder_remote'].fillna('')
            ls['last_modified_remote'] = pd.to_datetime(ls['last_modified_remote'])            
            ls['size_remote'] = ls['size_remote'].fillna(0)
            ls['files_remote'] = ls['files_remote'].fillna(0)
            ls['storage_class_remote'] = ls['storage_class_remote'].fillna('')
            ls['user'] = ls['user'].fillna('')
            ls['database'] = ls['database'].fillna('')
            ls['period'] = ls['period'].fillna('')
            ls['source'] = ls['source'].fillna('')
            ls['container'] = ls['container'].fillna('')
            ls['tablename'] = ls['tablename'].fillna('')
            ls['partition'] = ls['partition'].fillna('')
            ls['partitioning_period' ]= ls['partitioning_period'].fillna('')
            ls.sort_index(inplace=True)

        return ls
    
    def list_remote(self, keyword='', user='master'):
        mdprefix = user+'/'+keyword        
        # list_remote
        s3, bucket = S3GetSession()
        arrobj = np.array([[obj.key , obj.last_modified, obj.size, obj.storage_class]
                    for obj in bucket.objects.filter(Prefix=mdprefix)])
        dfremote = pd.DataFrame()
        if arrobj.size>0:
            dfremote = pd.DataFrame(
                arrobj, 
                columns=['full_path','last_modified_remote','size_remote','storage_class_remote']
            )    
            dfremote['path'] = dfremote['full_path'].apply(lambda x: str(Path(x).parent))
            dfremote['filename_remote'] = dfremote['full_path'].apply(lambda x: str(Path(x).name))    
            dfremote['folder_remote'] = 's3://'+bucket.name        
            dfremote['size_remote'] = dfremote['size_remote'].astype(np.int64)    
            dfremote['user'] = dfremote['path'].apply(lambda x: x.split(os.sep)[0])
            dfremote['database'] = dfremote['path'].apply(lambda x: x.split(os.sep)[1])    
            dfremote['period'] = dfremote['path'].apply(lambda x: x.split(os.sep)[2] if len(x.split(os.sep))>2 else '')
            dfremote['source'] = dfremote['path'].apply(lambda x: x.split(os.sep)[3] if len(x.split(os.sep))>3 else '')
            dfremote['container'] = dfremote['path'].apply(lambda x: x.split(os.sep)[4] if len(x.split(os.sep))>4 else '')        
            dfremote['tablename'] = dfremote['path'].apply(lambda x: '/'.join(x.split(os.sep)[5:]) if len(x.split(os.sep))>5 else '')
            dfremote['partition'] = dfremote['tablename'].apply(lambda x: x.split('/')[1] if '/' in x else '')
            dfremote['tablename'] = dfremote['tablename'].apply(lambda x: x.split('/')[0])        
            dfremote['files_remote'] = 1
            # change path for metadata
            metadataidx = dfremote['database' ]=='Metadata'
            dfremote.loc[metadataidx,'path'] = dfremote.loc[metadataidx,'full_path'].apply(lambda x: x.rstrip('.bin.gzip'))        
            dfremote.loc[metadataidx,'container'] = 'metadata'
            dfremote.loc[metadataidx,'period'] = ''
            dfremote.loc[metadataidx,'source'] = ''
            dfremote.loc[metadataidx,'tablename'] = ''
            dfremote.loc[metadataidx,'partition'] = ''
            # change path for timeseries
            timeseriesidx = dfremote['filename_remote'].apply(lambda x: x.startswith('timeseries_'))
            dfremote.loc[timeseriesidx,'container'] = 'timeseries'
            # group by path
            dfremote = dfremote.groupby('path').agg(
                    {               
                        'folder_remote':'first',
                        'last_modified_remote':'max',
                        'size_remote':'sum',                
                        'storage_class_remote':'first',                
                        'user':'first',
                        'database':'first',
                        'period':'first',
                        'source':'first',
                        'container':'first',
                        'tablename':'first',
                        'partition':'first',
                        'files_remote':'sum'
                    }
                )
            
        return dfremote
    
    def list_local(self, keyword='', user='master'):
        mdprefix = user+'/'+keyword
        dflocal = pd.DataFrame()
        records = []
        for dbfolder in self.dbfolders:
            localpath = Path(dbfolder) / Path(mdprefix)    
            for root, dirs, files in os.walk(localpath):
                for name in files:
                    if name.endswith((".bin")):
                        full_path = os.path.join(root, name)
                        modified_time_local = datetime.fromtimestamp(os.path.getmtime(full_path)).astimezone(timezone.utc)
                        created_time_local = datetime.fromtimestamp(os.path.getctime(full_path)).astimezone(timezone.utc)
                        size = np.int64(os.path.getsize(full_path))
                        records.append({
                            'full_path': full_path,
                            'path': root.replace(dbfolder,'').replace('\\','/').rstrip('/').lstrip('/'),
                            'filename_local': name,
                            'folder_local' : dbfolder,
                            'created_local' : created_time_local,
                            'last_modified_local': modified_time_local,
                            'size_local': size
                        })
        if len(records)>0:
            dflocal = pd.DataFrame(records)
            dflocal['user'] = dflocal['path'].apply(lambda x: x.split(os.sep)[0])            
            dflocal['database'] = dflocal['path'].apply(lambda x: x.split(os.sep)[1])
            dflocal['period'] = dflocal['path'].apply(lambda x: x.split(os.sep)[2] if len(x.split(os.sep))>2 else '')
            dflocal['source'] = dflocal['path'].apply(lambda x: x.split(os.sep)[3] if len(x.split(os.sep))>3 else '')
            dflocal['container'] = dflocal['path'].apply(lambda x: x.split(os.sep)[4] if len(x.split(os.sep))>4 else '')
            dflocal['tablename'] = dflocal['path'].apply(lambda x: '/'.join(x.split(os.sep)[5:]) if len(x.split(os.sep))>5 else '')
            dflocal['partition'] = dflocal['tablename'].apply(lambda x: x.split('/')[1] if '/' in x else '')
            dflocal['tablename'] = dflocal['tablename'].apply(lambda x: x.split('/')[0])        
            dflocal['files_local'] = 1
            # change path for metadata
            metadataidx = dflocal['database' ]=='Metadata'
            dflocal.loc[metadataidx,'path'] += '/'+dflocal.loc[metadataidx,'filename_local'].apply(lambda x: x.rstrip('.bin'))
            dflocal.loc[metadataidx,'container'] = 'metadata'
            dflocal.loc[metadataidx,'period'] = ''
            dflocal.loc[metadataidx,'source'] = ''
            dflocal.loc[metadataidx,'tablename'] = ''
            dflocal.loc[metadataidx,'partition'] = ''
            # change path for timeseries
            timeseriesidx = dflocal['container']=='timeseries'
            dflocal.loc[timeseriesidx,'path'] += '/'+dflocal.loc[timeseriesidx,'filename_local'].apply(lambda x: x.rstrip('.bin'))    
            dflocal = dflocal.groupby('path').agg(
                    {               
                        'folder_local':'first',
                        'created_local':'min',
                        'last_modified_local':'max',
                        'size_local':'sum',
                        'user':'first',
                        'database':'first',
                        'period':'first',
                        'source':'first',
                        'container':'first',
                        'tablename':'first',
                        'partition':'first',
                        'files_local':'sum'
                    }
                )    
                                
        return dflocal

    def list_disks(self):
        disk_usage = {}
        for directory in self.dbfolders:
            if not os.path.exists(directory):
                Path(directory).mkdir(parents=True, exist_ok=True)
            # Get disk usage statistics
            os.sync()
            time.sleep(0.001)
            total, used, free = shutil.disk_usage(directory)            
            disk_usage[directory] = {
                "total": total // (2**30),  # Convert bytes to GB
                "used": used // (2**30),
                "free": free // (2**30),
                "percent_used": (used / total) * 100,
            }
        dfdisks = pd.DataFrame(disk_usage).T
        dfdisks.sort_values('percent_used', inplace=True)
        return dfdisks

    @staticmethod
    def list_memory():
        folder = Path(os.environ['DATABASE_FOLDER'])/'shm'
        shm_names = pd.DataFrame()
        for root, _, filepaths in os.walk(folder):
            for filepath in filepaths:
                if filepath.endswith('.csv'):
                    fpath = os.path.join(root, filepath)
                    shm_name = fpath.removeprefix(str(folder))[1:]
                    shm_name = shm_name.removesuffix('.csv')
                    if os.name == 'posix':
                        shm_name = shm_name.replace('/', '\\')
                    elif os.name == 'nt':
                        shm_name = shm_name.replace('\\', '/')
                    try:
                        shm = shared_memory.SharedMemory(
                            name=shm_name, create=False)
                        shm_names.loc[shm_name, 'size'] = shm.size
                        shm.close()
                    except:
                        try:
                            if fpath.is_file():
                                os.remove(fpath)
                        except:
                            pass
        shm_names = shm_names.sort_index()
        return shm_names
      
    ######### LOAD ############    

    def load_table(self,table,args, user='master'):    
        result = {}
        result['path'] = table.name        
        try:
            if table['partition']!= '':
                tablename = table['tablename'] + '/' + table['partition']
            else:
                tablename = table['tablename']
                    
            tbl = self.table(table['database'],table['period'],table['source'],tablename, user=user)
            result['hasindex'] = tbl.table.hdr['hasindex']
            result['mtime'] = pd.Timestamp.fromtimestamp(tbl.mtime)
            result['size'] = tbl.recordssize*tbl.dtype.itemsize
            result['count'] = tbl.count
            result['recordssize'] = tbl.recordssize
            result['itemsize'] = tbl.dtype.itemsize
            result['names'] = ','.join([s[0] for s in tbl.dtype.descr])
            result['formats'] = ','.join([s[1] for s in tbl.dtype.descr])
            tbl.free()            
        except Exception as e:
            Logger.log.error(f'Loading {table.name} Error: {e}')                    
        
        return result
    
    def load_tables(self, tables, maxproc=8):
        try:
            tables = tables[tables['container']=='table']
            Logger.log.info('Loading tables...')
            results = io_bound_unordered(self.load_table,tables,[],maxproc=maxproc)
            Logger.log.info('Tables loaded!')              
            results = [r for r in results if r != -1]
            if len(results)>0:
                df = pd.DataFrame(results).set_index('path')
                tables.loc[df.index,df.columns] = df.values
            return True
        except Exception as e:
            Logger.log.error(f'load_tables error {e}')
        return False

    def load_db(self, database, user='master',maxproc=8):
        try:
            tables = self.list_all(database, user)
            tables = tables[tables['container']=='table']
            Logger.log.info('Loading tables...')
            self.load_tables(tables, maxproc=maxproc)
            return True
        except Exception as e:
            Logger.log.error(f'load_db error {e}')        
        return False


    ######### DELETE ############
    
    def delete_table(self, database, period, source, tablename, user='master'):
        try:
            path = f'{user}/{database}/{period}/{source}/table/{tablename}'
            if path in self.data.keys():
                self.data[path].free()
                del self.data[path]
            
            raise NotImplementedError(f'Delete {path} not implemented')
            localpath = None

            if localpath.exists():
                delfiles = ['data.bin','dateidx.bin','pkey.bin','symbolidx.bin','portidx.bin']
                for file in delfiles:
                    delpath = Path(localpath/file)
                    if delpath.exists():
                        os.remove(delpath)
                 # if folder is empty remove it
                if not any(localpath.iterdir()):
                    shutil.rmtree(localpath)                
            
            S3DeleteTable(path)
            return True
        except Exception as e:
            Logger.log.error(f'Delete {path} Error: {e}')
            return False
        
    def delete_timeseries(self, database, period, source, 
                          tag=None, user='master'):
        try:            
            path = f'{user}/{database}/{period}/{source}/timeseries'
            if tag is None:
                # delete timeseries container
                if path in self.data.keys():
                    del self.data[path]                
                localpath = Path(os.environ['DATABASE_FOLDER'])/Path(path.replace('/timeseries',''))
                if self.dbfolderdict:
                    key = database+'/'+period+'/'+source
                    if key in self.dbfolderdict:
                        localpath = Path(self.dbfolderdict[key])/Path(path.replace('/timeseries',''))
                    else:
                        key = database+'/'+period
                        if key in self.dbfolderdict:
                            localpath = Path(self.dbfolderdict[key])/Path(path.replace('/timeseries',''))                            
                if localpath.exists():
                    shutil.rmtree(localpath)
                S3DeleteTimeseries(path)
                return True
            else:                
                # delete timeseries tag
                ts = self.timeseries(database,period,source,tag,user=user)
                tstag = self.data[path].tags[tag]
                fpath, shm_name = tstag.get_path()
                del self.data[path].tags[tag]
                del ts
                os.remove(fpath)
                return True
            
        except Exception as e:
            Logger.log.error(f'Delete {path}/{tag} Error: {e}')
            return False           
        

    ############# MONGODB #############
    # Getter for db
    @property
    def mongodb(self):
        if self._mongodb is None:
            self._mongodb = MongoDBClient()
        return self._mongodb    