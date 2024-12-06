# THIRD PARTY LIBS
import os
import pandas as pd
import numpy as np
import time
from numba import jit
from pathlib import Path

from SharedData.Logger import Logger


class TimeSeriesDisk:

    def __init__(self, shareddata, container, database, period, source, tag,
             value=None, columns=None, user='master',overwrite=False):

        self.shareddata = shareddata
        self.container = container
        self.user = user
        self.database = database
        self.period = period
        self.source = source
        self.tag = tag[1:] if tag[0]=="\\" or tag[0]=="/" else tag
        
        self.periodseconds = container.periodseconds
        self.startDate = self.container.startDate
        self.index = self.container.getTimeIndex(self.startDate)
        self.ctimeidx = self.container.getContinousTimeIndex(self.startDate)
        
        self.columns = None
        if not columns is None:
            self.columns = columns
            self.symbolidx = {}
            for i in range(len(self.columns)):
                self.symbolidx[self.columns.values[i]] = i
        elif not value is None:
            self.columns = value.columns
            self.symbolidx = {}
            for i in range(len(self.columns)):
                self.symbolidx[self.columns.values[i]] = i

        self.path, self.shm_name = self.get_path()
        self.exists = os.path.isfile(self.path)                        
                    
        self.data = None        
                        
        self.init_time = time.time()
        try:            
            copy = False
            if (self.exists) & (not overwrite):
                _data = self.malloc_map()
                
                if not self.columns is None:
                    if not _data.columns.equals(self.columns):
                        copy = True

                if not self.index.equals(_data.index):
                    copy = True

                if not copy:
                    self.data = _data
                    if self.columns is None:
                        self.columns = self.data.columns
                        self.symbolidx = {}
                        for i in range(len(self.columns)):
                            self.symbolidx[self.columns.values[i]] = i
                else:
                    _data = _data.copy(deep=True)                    
                    del self.shf
                    self.columns = _data.columns
                    self.symbolidx = {}
                    for i in range(len(self.columns)):
                        self.symbolidx[self.columns.values[i]] = i
                    self.malloc_create()
                    sidx = np.array([self.get_loc_symbol(s)
                                for s in self.columns])
                    ts = _data.index.values.astype(np.int64)/10**9  # seconds
                    tidx = self.get_loc_timestamp(ts)
                    self.setValuesJit(self.data.values, tidx,
                                        sidx, _data.values)
                    del _data
                                
            elif (not self.exists) | (overwrite):
                # create new empty file
                self.malloc_create()

            if (not value is None):
                sidx = np.array([self.get_loc_symbol(s)
                                for s in self.columns])
                ts = value.index.values.astype(np.int64)/10**9  # seconds
                tidx = self.get_loc_timestamp(ts)
                self.setValuesJit(self.data.values, tidx,
                                    sidx, value.values)
                self.shf.flush()
                        
        except Exception as e:            
            errmsg = 'Error initalizing %s!\n%s' % (self.shm_name, str(e))
            Logger.log.error(errmsg)
            raise Exception(errmsg)

        self.init_time = time.time() - self.init_time

    def get_path(self):
        shm_name = self.user + '/' + self.database + '/' \
            + self.period + '/' + self.source + '/timeseries/' + self.tag
        if os.name == 'posix':
            shm_name = shm_name.replace('/', '\\')

        path = Path(os.environ['DATABASE_FOLDER'])
        path = path / self.user
        path = path / self.database
        path = path / self.period
        path = path / self.source
        path = path / 'timeseries'
        path = path / (self.tag+'.bin')
        path = Path(str(path).replace('\\', '/'))
        os.makedirs(path.parent, exist_ok=True)
        
        return path, shm_name

    def malloc_create(self):
        filepath = self.path
                            
        try:  # try create file
                                    
            idx_b = self.index.astype(np.int64).values.tobytes()
            nb_idx = len(idx_b)
            r = len(self.index)

            colscsv_b = str.encode(','.join(self.columns),
                                   encoding='UTF-8', errors='ignore')            
            nb_cols = len(colscsv_b)
            c = len(self.columns)
            
            nb_data = int(r*c*8)
            
            header_b = np.array([r, c, nb_cols, nb_idx, nb_data]).astype(
                np.int64).tobytes()
            nb_header = len(header_b)

            nb_total = nb_header+nb_cols+nb_idx+nb_data
            nb_offset = nb_header+nb_cols+nb_idx

            totalbytes = int(nb_total)
            if not Path(filepath).is_file():
                # create folders
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                with open(filepath, 'wb') as f:
                    # Seek to the end of the file
                    f.seek(totalbytes-1)
                    # Write a single null byte to the end of the file
                    f.write(b'\x00')
                    if os.name == 'posix':
                        os.posix_fallocate(f.fileno(), 0, totalbytes)
                    elif os.name == 'nt':
                        pass  # TODO: implement preallocation for windows in pyd
            elif (Path(filepath).stat().st_size < totalbytes):
                with open(filepath, 'ab') as f:
                    # Seek to the end of the file
                    f.seek(totalbytes-1)
                    # Write a single null byte to the end of the file
                    f.write(b'\x00')
                    if os.name == 'posix':
                        os.posix_fallocate(f.fileno(), 0, totalbytes)
                    elif os.name == 'nt':
                        pass  # TODO: implement preallocation for windows in pyd

            # write data
            with open(filepath, 'rb+') as f:
                f.seek(0)
                f.write(header_b)
                f.write(colscsv_b)
                f.write(idx_b)                

            
            self.shf = np.memmap(filepath,'<f8','r+',nb_offset,(r,c))
            self.shf[:] = np.nan
            self.shf.flush()
            self.data = pd.DataFrame(self.shf,                                     
                                     index=self.index,
                                     columns=self.columns,
                                     copy=False)
            self.data.index.name = 'date'            
            

            return True
        except Exception as e:
            Logger.log.error('Failed to malloc_create\n%s' % str(e))
            raise Exception('Failed to malloc_create\n%s' % str(e))            

    def malloc_map(self):        
        filepath = self.path
        
        with open(filepath, 'rb') as f:
            nb_header = 40
            header = np.frombuffer(f.read(nb_header), dtype=np.int64)            
            r = header[0]
            c = header[1]
            nb_cols = header[2]
            nb_idx = header[3]
            nb_data = header[4]
            
            cols_b = f.read(nb_cols)
            _columns = cols_b.decode(
                encoding='UTF-8', errors='ignore').split(',')
            _columns = pd.Index(_columns)

            idx_b = f.read(nb_idx)
            _index = pd.to_datetime(np.frombuffer(idx_b, dtype=np.int64))
                                                
            nb_offset = nb_header+nb_cols+nb_idx
            self.shf = np.memmap(filepath,'<f8','r+',nb_offset,(r,c))

            _data = pd.DataFrame(self.shf,
                                index=_index,
                                columns=_columns,
                                copy=False)
            _data.index.name = 'date'
            
        return _data

    # get / set
    def get_loc_symbol(self, symbol):
        if symbol in self.symbolidx.keys():
            return self.symbolidx[symbol]
        else:
            return np.nan

    def get_loc_timestamp(self, ts):
        istartdate = self.startDate.timestamp()  # seconds
        if not np.isscalar(ts):
            tidx = self.get_loc_timestamp_Jit(ts, istartdate,
                                              self.periodseconds, self.ctimeidx)
            return tidx
        else:
            tids = np.int64(ts)  # seconds
            tids = np.int64(tids - istartdate)
            tids = np.int64(tids/self.periodseconds)
            if tids < self.ctimeidx.shape[0]:
                tidx = self.ctimeidx[tids]
                return tidx
            else:
                return np.nan

    @staticmethod
    @jit(nopython=True, nogil=True, cache=True)
    def get_loc_timestamp_Jit(ts, istartdate, periodseconds, ctimeidx):
        tidx = np.empty(ts.shape, dtype=np.float64)
        len_ctimeidx = len(ctimeidx)
        for i in range(len(tidx)):
            tid = np.int64(ts[i])
            tid = np.int64(tid-istartdate)
            tid = np.int64(tid/periodseconds)
            if tid < len_ctimeidx:
                tidx[i] = ctimeidx[tid]
            else:
                tidx[i] = np.nan
        return tidx

    @staticmethod
    @jit(nopython=True, nogil=True, cache=True)
    def setValuesSymbolJit(values, tidx, sidx, arr):
        if not np.isnan(sidx):
            s = np.int64(sidx)
            i = 0
            for t in tidx:
                if not np.isnan(t):
                    values[np.int64(t), s] = arr[i]
                i = i+1

    @staticmethod
    @jit(nopython=True, nogil=True, cache=True)
    def setValuesJit(values, tidx, sidx, arr):
        i = 0
        for t in tidx:
            if not np.isnan(t):
                j = 0
                for s in sidx:
                    if not np.isnan(s):
                        values[np.int64(t), np.int64(s)] = arr[i, j]
                    j = j+1
            i = i+1

    # C R U D
    def malloc(self, value=None):
        tini = time.time()

        # Create write ndarray
        path, shm_name = self.get_path()

        if os.environ['LOG_LEVEL'] == 'DEBUG':
            Logger.log.debug('malloc %s ...%.2f%% ' % (shm_name, 0.0))

        try:  # try create memory file
            r = len(self.index)
            c = len(self.columns)

            idx_b = self.index.astype(np.int64).values.tobytes()
            colscsv_b = str.encode(','.join(self.columns.values),
                                   encoding='UTF-8', errors='ignore')
            nb_idx = len(idx_b)
            nb_cols = len(colscsv_b)
            nb_data = int(r*c*8)
            header_b = np.array([r, c, nb_idx, nb_cols, nb_data]).astype(
                np.int64).tobytes()
            nb_header = len(header_b)

            nb_buf = nb_header+nb_idx+nb_cols+nb_data
            nb_offset = nb_header+nb_idx+nb_cols

            [self.shm, ismalloc] = self.shareddata.malloc(
                shm_name, create=True, size=nb_buf)

            i = 0
            self.shm.buf[i:nb_header] = header_b
            i = i + nb_header
            self.shm.buf[i:i+nb_idx] = idx_b
            i = i + nb_idx
            self.shm.buf[i:i+nb_cols] = colscsv_b

            self.shmarr = np.ndarray((r, c),
                                     dtype=np.float64, buffer=self.shm.buf, offset=nb_offset)

            if not value is None:
                self.shmarr[:] = value.values.copy()
            else:
                self.shmarr[:] = np.nan

            self.data = pd.DataFrame(self.shmarr,
                                     index=self.index,
                                     columns=self.columns,
                                     copy=False)

            if not value is None:
                value = self.data

            if os.environ['LOG_LEVEL'] == 'DEBUG':
                Logger.log.debug('malloc create %s ...%.2f%% %.2f sec! ' %
                                 (shm_name, 100, time.time()-tini))
            self.create_map = 'create'
            return True
        except Exception as e:
            pass

        # map memory file
        [self.shm, ismalloc] = self.shareddata.malloc(shm_name)

        i = 0
        nb_header = 40
        header = np.frombuffer(self.shm.buf[i:nb_header], dtype=np.int64)
        i = i + nb_header
        nb_idx = header[2]
        idx_b = bytes(self.shm.buf[i:i+nb_idx])
        self.index = pd.to_datetime(np.frombuffer(idx_b, dtype=np.int64))
        i = i + nb_idx
        nb_cols = header[3]
        cols_b = bytes(self.shm.buf[i:i+nb_cols])
        self.columns = cols_b.decode(
            encoding='UTF-8', errors='ignore').split(',')

        r = header[0]
        c = header[1]
        nb_data = header[4]
        nb_offset = nb_header+nb_idx+nb_cols

        self.shmarr = np.ndarray((r, c), dtype=np.float64,
                                 buffer=self.shm.buf, offset=nb_offset)

        self.data = pd.DataFrame(self.shmarr,
                                 index=self.index,
                                 columns=self.columns,
                                 copy=False)

        if not value is None:
            iidx = value.index.intersection(self.data.index)
            icol = value.columns.intersection(self.data.columns)
            self.data.loc[iidx, icol] = value.loc[iidx, icol]

        if os.environ['LOG_LEVEL'] == 'DEBUG':
            Logger.log.debug('malloc map %s/%s/%s ...%.2f%% %.2f sec! ' %
                             (self.source, self.period, self.tag, 100, time.time()-tini))
        self.create_map = 'map'
        return False

    def free(self):
        if hasattr(self, 'shf'):
            self.shf.flush()  # Ensure all changes are written back to the file
            del self.shf  # Delete the memmap object
            if hasattr(self, 'data'):
                del self.data  # Ensure DataFrame is also deleted if it exists
            
        path = f'{self.user}/{self.database}/{self.period}/{self.source}/timeseries'
        if path in self.shareddata.data.keys():
            del self.shareddata.data[path].tags[self.tag]
            