import os
import io
import hashlib
import gzip
import shutil
import time
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
from pandas.tseries.offsets import BDay
from threading import Thread
from tqdm import tqdm

from SharedData.Logger import Logger
from SharedData.TimeSeriesDisk import TimeSeriesDisk
from SharedData.TimeSeriesMemory import TimeSeriesMemory
from SharedData.IO.AWSS3 import S3Upload, S3Download, UpdateModTime


class TimeseriesContainer:

    def __init__(self, shareddata, database, period, source,
                 user='master',type='DISK', startDate=None):

        self.shareddata = shareddata
        self.user = user
        self.database = database
        self.period = period
        self.source = source
        self.type = type

        # DATA DICTIONARY
        # tags[tag]
        self.tags = {}

        # TIME INDEX
        self.timeidx = {}
        self.ctimeidx = {}
        if self.period == 'W1':
            self.periodseconds = 7*60*60*24
            self.default_startDate = pd.Timestamp('1995-01-01')
        elif self.period == 'D1':
            self.periodseconds = 60*60*24
            self.default_startDate = pd.Timestamp('1995-01-01')
        elif self.period == 'M15':
            self.periodseconds = 60*15
            self.default_startDate = pd.Timestamp('2010-01-01')
        elif self.period == 'M1':
            self.periodseconds = 60
            self.default_startDate = pd.Timestamp('2010-01-01')

        if startDate is None:
            self.startDate = self.default_startDate
        else:
            self.startDate = pd.Timestamp(startDate)            
        self.getTimeIndex(self.startDate)
        self.getContinousTimeIndex(self.startDate)
        self.loaded = False        

    def getTimeIndex(self, startDate):
        if not startDate in self.timeidx.keys():
            lastdate = pd.Timestamp(datetime.now().year+1, 1, 1)

            if self.period == 'D1':
                self.timeidx[startDate] = pd.Index(
                    pd.bdate_range(start=startDate,
                                   end=np.datetime64(lastdate)))
                self.periodseconds = 60*60*24

            elif self.period == 'M15':
                self.timeidx[startDate] = pd.Index(
                    pd.bdate_range(start=startDate,
                                   end=np.datetime64(lastdate), freq='15min'))
                idx = (self.timeidx[startDate].hour > 6)
                idx = (idx) & (self.timeidx[startDate].hour < 22)
                idx = (idx) & (self.timeidx[startDate].day_of_week < 5)
                self.timeidx[startDate] = self.timeidx[startDate][idx]
                self.periodseconds = 60*15

            elif self.period == 'M1':
                self.timeidx[startDate] = pd.Index(
                    pd.bdate_range(start=startDate,
                                   end=np.datetime64(lastdate), freq='1min'))
                idx = (self.timeidx[startDate].hour > 6)
                idx = (idx) & (self.timeidx[startDate].hour < 22)
                idx = (idx) & (self.timeidx[startDate].day_of_week < 5)
                self.timeidx[startDate] = self.timeidx[startDate][idx]
                self.periodseconds = 60

        return self.timeidx[startDate]

    def getContinousTimeIndex(self, startDate):
        if not startDate in self.ctimeidx.keys():
            _timeidx = self.getTimeIndex(startDate)
            nsec = (_timeidx - startDate).astype(np.int64)
            periods = (nsec/(10**9)/self.periodseconds).astype(np.int64)
            self.ctimeidx[startDate] = np.empty(max(periods)+1)
            self.ctimeidx[startDate][:] = np.nan
            self.ctimeidx[startDate][periods.values] = np.arange(len(periods))
        return self.ctimeidx[startDate]

    def get_path(self):
        shm_name = self.user + '/' + self.database + '/' \
            + self.period + '/' + self.source + '/timeseries'
        if os.name == 'posix':
            shm_name = shm_name.replace('/', '\\')

        path = Path(os.environ['DATABASE_FOLDER'])
        path = path / self.user
        path = path / self.database
        path = path / self.period
        path = path / self.source
        path = path / 'timeseries'
        path = Path(str(path).replace('\\', '/'))
        if (self.type == 'DISK'):
            os.makedirs(path.parent, exist_ok=True)
            
        return path, shm_name

    # READ
    def load(self):
        # read if not loaded
        if self.type == 'DISK':
            self.read()
            
            path, shm_name = self.get_path()
            tagslist = path.rglob('*.bin')
            for tag in tagslist:
                if tag.is_file():
                    tagname = str(tag).replace(str(path),'').replace('.bin','').replace('\\','/')
                    if (tagname[0] == '/') | (tagname[0] == '\\'):
                        tagname = tagname[1:]
                    if not tagname in self.tags.keys():
                        self.tags[tagname] = TimeSeriesDisk(self.shareddata, self, self.database,
                                                    self.period, self.source, tag=tagname, user=self.user)
        else:
            shdatalist = self.shareddata.list_memory()
            path, shm_name = self.get_path()
            idx = [shm_name in str(s) for s in shdatalist.index]
            if not np.any(idx):
                self.read()
            else:
                # map
                self.map(shm_name, shdatalist.index[idx])

    def map(self, shm_name, shm_name_list):
        for shm in shm_name_list:
            tag = shm.replace(shm_name, '')[1:].replace('\\', '/')
            self.tags[tag] = TimeSeriesMemory(self.shareddata, self, self.database,
                                        self.period, self.source, tag=tag)

    def read(self):
        tini = time.time()
        datasize = 1
        path, shm_name = self.get_path()
        headpath = Path(str(path)+'_head.bin')
        tailpath = Path(str(path)+'_tail.bin')
        head_io = None
        tail_io = None
    
        force_download = (self.type == 'MEMORY')

        [head_io_gzip, head_local_mtime, head_remote_mtime] = \
            S3Download(str(headpath)+'.gzip', str(headpath), force_download)
        if not head_io_gzip is None:
            head_io = io.BytesIO()

            total_size = head_io_gzip.seek(0, 2)
            head_io_gzip.seek(0)
            with gzip.GzipFile(fileobj=head_io_gzip, mode='rb') as gz:
                with tqdm(total=total_size, unit='B', unit_scale=True,
                            desc='Unzipping %s' % (shm_name), dynamic_ncols=True) as pbar:
                    chunk_size = int(1024*1024)
                    while True:
                        chunk = gz.read(chunk_size)
                        if not chunk:
                            break
                        head_io.write(chunk)
                        pbar.update(len(chunk))
            
            if self.type == 'MEMORY':
                TimeseriesContainer.write_file(
                    head_io, headpath, mtime=head_remote_mtime, shm_name=shm_name)
            elif self.type == 'DISK':
                with open(headpath, 'wb') as f:
                    f.write(b'\x00')
            UpdateModTime(headpath, head_remote_mtime)

        [tail_io_gzip, tail_local_mtime, tail_remote_mtime] = \
            S3Download(str(tailpath)+'.gzip', str(tailpath), force_download)
        if not tail_io_gzip is None:
            tail_io = io.BytesIO()
            tail_io_gzip.seek(0)
            with gzip.GzipFile(fileobj=tail_io_gzip, mode='rb') as gz:
                shutil.copyfileobj(gz, tail_io)
            
            if self.type == 'MEMORY':                        
                TimeseriesContainer.write_file(
                    tail_io, tailpath, mtime=tail_remote_mtime, shm_name=shm_name)
            elif self.type == 'DISK':
                with open(tailpath, 'wb') as f:                            
                    f.write(b'\x00')
            UpdateModTime(tailpath, tail_remote_mtime)

        
        if (head_io is None):
            # read local
            if os.path.isfile(str(headpath)):
                if (headpath.stat().st_size > 1) & (self.type == 'DISK'):
                    head_io = open(str(headpath), 'rb')
                elif self.type == 'MEMORY':
                    head_io = open(str(headpath), 'rb')

        if (tail_io is None):
            if os.path.isfile(str(tailpath)):
                if (tailpath.stat().st_size > 1) & (self.type == 'DISK'):
                    tail_io = open(str(tailpath), 'rb')
                elif self.type == 'MEMORY':
                    tail_io = open(str(tailpath), 'rb')

        if not head_io is None:
            datasize += self.read_io(head_io, headpath, shm_name, ishead=True)
            # delete head file if type was memory 
            if (headpath.stat().st_size > 1) & (self.type == 'DISK'):
                head_io.close()
                mtime = headpath.stat().st_mtime
                with open(headpath, 'wb') as f:                            
                    f.write(b'\x00')
                os.utime(headpath, (mtime, mtime))


        if not tail_io is None:
            datasize += self.read_io(tail_io, tailpath, shm_name, ishead=False)
            # delete tail file if type was memory 
            if (tailpath.stat().st_size > 1) & (self.type == 'DISK'):
                tail_io.close()
                mtime = tailpath.stat().st_mtime
                with open(tailpath, 'wb') as f:                            
                    f.write(b'\x00')
                os.utime(tailpath, (mtime, mtime))

        te = time.time()-tini+0.000001
        datasize = datasize/(1024*1024)
        Logger.log.debug('read %s/%s %.2fMB in %.2fs %.2fMBps ' %
                         (self.source, self.period, datasize, te, datasize/te))

    def read_io(self, io_obj, path, shm_name, ishead=True):
        datasize = 0
        # read
        io_obj.seek(0)
        io_data = io_obj.read()
        _io_data = io_data[:-24]
        datasize = len(_io_data)
        datasizemb = datasize/(1024*1024)
        if datasizemb > 100:
            message = 'Verifying:%iMB %s' % (datasizemb, shm_name)
            block_size = 100 * 1024 * 1024  # or any other block size that you prefer
            nb_total = datasize
            read_bytes = 0
            _m = hashlib.md5()
            # Use a with block to manage the progress bar
            with tqdm(total=nb_total, unit='B', unit_scale=True, desc=message) as pbar:
                # Loop until we have read all the data
                while read_bytes < nb_total:
                    # Read a block of data
                    chunk_size = min(block_size, nb_total-read_bytes)
                    # Update the shared memory buffer with the newly read data
                    _m.update(_io_data[read_bytes:read_bytes+chunk_size])
                    read_bytes += chunk_size  # update the total number of bytes read so far
                    # Update the progress bar
                    pbar.update(chunk_size)
            _m = _m.digest()
        else:
            _m = hashlib.md5(io_data[:-24]).digest()
        # _m = hashlib.md5(io_data[:-24]).digest()
        m = io_data[-16:]
        if not self.compare_hash(m,_m):
            Logger.log.error('Timeseries file %s corrupted!' % (shm_name))
            raise Exception('Timeseries file %s corrupted!' % (shm_name))
        io_obj.seek(0)
        separator = np.frombuffer(io_obj.read(8), dtype=np.int64)[0]
        while (separator == 1):
            _header = np.frombuffer(io_obj.read(40), dtype=np.int64)
            _tag_b = io_obj.read(int(_header[0]))
            _tag = _tag_b.decode(encoding='UTF-8', errors='ignore')
            _idx_b = io_obj.read(int(_header[1]))
            _idx = pd.to_datetime(np.frombuffer(_idx_b, dtype=np.int64))
            _colscsv_b = io_obj.read(int(_header[2]))
            _colscsv = _colscsv_b.decode(encoding='UTF-8', errors='ignore')
            _cols = _colscsv.split(',')
            r = _header[3]
            c = _header[4]
            total_bytes = int(r*c*8)
            _data = np.frombuffer(io_obj.read(total_bytes),
                                  dtype=np.float64).reshape((r, c))
            df = pd.DataFrame(_data, index=_idx, columns=_cols)
            if self.type == 'DISK':
                if ishead:
                    self.tags[_tag] = TimeSeriesDisk(self.shareddata, self, self.database,
                                                    self.period, self.source, tag=_tag, value=df, user=self.user, overwrite=True)
                else:
                    if not _tag in self.tags.keys():
                        self.tags[_tag] = TimeSeriesDisk(self.shareddata, self, self.database,
                                                    self.period, self.source, tag=_tag, value=df, user=self.user, overwrite=True)
                    else:
                        data = self.tags[_tag].data
                        iidx = df.index.intersection(data.index)
                        icol = df.columns.intersection(data.columns)
                        data.loc[iidx, icol] = df.loc[iidx, icol].copy()
                        
            elif self.type == 'MEMORY':
                if not _tag in self.tags.keys():
                    self.tags[_tag] = TimeSeriesMemory(self.shareddata, self, self.database,
                                                self.period, self.source, tag=_tag, value=df, user=self.user, overwrite=True)
                else:
                    data = self.tags[_tag].data
                    iidx = df.index.intersection(data.index)
                    icol = df.columns.intersection(data.columns)
                    data.loc[iidx, icol] = df.loc[iidx, icol].copy()
            separator = np.frombuffer(io_obj.read(8), dtype=np.int64)[0]
        io_obj.close()

        return datasize

    def compare_hash(self,h1,h2):
        l1 = len(h1)
        l2 = len(h2)
        l = min(l1,l2)
        return h1[:l]==h2[:l]

    # WRITE
    def flush(self):
        if self.type == 'DISK':
            for tag in self.tags:
                self.tags[tag].shf.flush()

    def write(self, startDate=None):
        path, shm_name = self.get_path()
        mtime = datetime.now().timestamp()
        partdate = pd.Timestamp(datetime(datetime.now().year, 1, 1))
        firstdate = pd.Timestamp('1970-01-01')
        if not startDate is None:
            firstdate = startDate
        if firstdate < partdate:
            self.write_head(path, partdate, mtime, shm_name)
        self.write_tail(path, partdate, mtime, shm_name)
        self.flush()

    def write_head(self, path, partdate, mtime, shm_name):
        io_obj = self.create_head_io(partdate)

        threads = []    
        io_obj.seek(0)
        gzip_io = io.BytesIO()
        with gzip.GzipFile(fileobj=gzip_io, mode='wb', compresslevel=1) as gz:
            shutil.copyfileobj(io_obj, gz)
        threads = [*threads, Thread(target=S3Upload,
                                    args=(gzip_io, str(path)+'_head.bin.gzip', mtime))]

        if self.type == 'DISK':
            with open(str(path)+'_head.bin', 'wb') as f:
                f.write(b'\x00')
            os.utime(str(path)+'_head.bin', (mtime, mtime))

        for i in range(len(threads)):
            threads[i].start()

        for i in range(len(threads)):
            threads[i].join()

    def create_head_io(self, partdate):
        io_obj = io.BytesIO()
        for tag in self.tags.keys():            
            dftag = self.tags[tag].data.loc[:partdate-BDay(1)]
            # create binary df
            df = dftag.dropna(how='all', axis=0).copy()
            r, c = df.shape
            tag_b = str.encode(tag, encoding='UTF-8', errors='ignore')
            idx = (df.index.astype(np.int64))
            idx_b = idx.values.tobytes()
            cols = df.columns.values
            colscsv = ','.join(cols)
            colscsv_b = str.encode(colscsv, encoding='UTF-8', errors='ignore')
            nbtag = len(tag_b)
            nbidx = len(idx_b)
            nbcols = len(colscsv_b)
            header = np.array([1, nbtag, nbidx, nbcols, r, c]).astype(np.int64)
            io_obj.write(header)
            io_obj.write(tag_b)
            io_obj.write(idx_b)
            io_obj.write(colscsv_b)
            io_obj.write(np.ascontiguousarray(df.values.astype(np.float64)))

        m = hashlib.md5(io_obj.getvalue()).digest()
        io_obj.write(np.array([0]).astype(np.int64))
        io_obj.write(m)
        return io_obj

    def write_tail(self, path, partdate, mtime, shm_name):
        io_obj = self.create_tail_io(partdate)

        threads = []        
        io_obj.seek(0)
        gzip_io = io.BytesIO()
        with gzip.GzipFile(fileobj=gzip_io, mode='wb', compresslevel=1) as gz:
            shutil.copyfileobj(io_obj, gz)
        threads = [*threads, Thread(target=S3Upload,
                                    args=(gzip_io, str(path)+'_tail.bin.gzip', mtime))]
        
        if self.type == 'DISK':
            with open(str(path)+'_tail.bin', 'wb') as f:
                f.write(b'\x00')
            os.utime(str(path)+'_tail.bin', (mtime, mtime))

        for i in range(len(threads)):
            threads[i].start()

        for i in range(len(threads)):
            threads[i].join()

    def create_tail_io(self, partdate):
        io_obj = io.BytesIO()
        for tag in self.tags.keys():
            if self.type == 'DISK':
                self.tags[tag].shf.flush()
            dftag = self.tags[tag].data.loc[partdate:]
            # create binary df
            df = dftag.dropna(how='all', axis=0)
            r, c = df.shape
            tag_b = str.encode(tag, encoding='UTF-8', errors='ignore')
            idx = (df.index.astype(np.int64))
            idx_b = idx.values.tobytes()
            cols = df.columns.values
            colscsv = ','.join(cols)
            colscsv_b = str.encode(colscsv, encoding='UTF-8', errors='ignore')
            nbtag = len(tag_b)
            nbidx = len(idx_b)
            nbcols = len(colscsv_b)
            header = np.array([1, nbtag, nbidx, nbcols, r, c]).astype(np.int64)
            io_obj.write(header)
            io_obj.write(tag_b)
            io_obj.write(idx_b)
            io_obj.write(colscsv_b)
            io_obj.write(np.ascontiguousarray(df.values.astype(np.float64)))

        m = hashlib.md5(io_obj.getvalue()).digest()
        io_obj.write(np.array([0]).astype(np.int64))
        io_obj.write(m)
        return io_obj

    @staticmethod
    def write_file(io_obj, path, mtime, shm_name):
        with open(path, 'wb') as f:
            nb = len(io_obj.getbuffer())
            size_mb = nb / (1024*1024)
            if size_mb > 100:
                blocksize = 1024*1024*100
                descr = 'Writing:%iMB %s' % (size_mb, shm_name)
                with tqdm(total=nb, unit='B', unit_scale=True, desc=descr) as pbar:
                    written = 0
                    while written < nb:
                        # write in chunks of max 100 MB size
                        chunk_size = min(blocksize, nb-written)
                        f.write(io_obj.getbuffer()[written:written+chunk_size])
                        written += chunk_size
                        pbar.update(chunk_size)
            else:
                f.write(io_obj.getbuffer())
            f.flush()
        os.utime(path, (mtime, mtime))

    def free(self):
        _tags = list(self.tags.keys())
        for tag in _tags:
            self.tags[tag].free()
        path = f'{self.user}/{self.database}/{self.period}/{self.source}/timeseries'
        if path in self.shareddata.data.keys():
            del self.shareddata.data[path]
        

    # GETTER AND SETTER
    def __getitem__(self, key):
        if key in self.tags.keys():
            return self.tags[key].data
        else:
            raise Exception('Tag %s not found in %s/%s/%s' %
                    (key, self.database, self.period, self.source))
        
    def __setitem__(self, key, value):
        if key in self.tags.keys():
            self.tags[key] = value
        else:
            raise Exception('Tag %s not found in %s/%s/%s' %
                    (key, self.database, self.period, self.source))