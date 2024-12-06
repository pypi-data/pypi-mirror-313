# THIRD PARTY LIBS
import os
import pandas as pd
import numpy as np
import time
from numba import jit
from pathlib import Path

from SharedData.Logger import Logger


class TimeSeriesMemory:

    def __init__(self, shareddata, container, database, period, source, tag,
                 value=None, startDate=None, columns=None, user='master'):

        self.shareddata = shareddata
        self.container = container
        self.user = user
        self.database = database
        self.period = period
        self.source = source
        self.tag = tag

        self.periodseconds = container.periodseconds

        # test if shared memory already exists
        if self.ismalloc():
            self.create_map = 'map'
        else:
            self.create_map = 'create'
            
        self.init_time = time.time()
        self.download_time = pd.NaT
        self.last_update = pd.NaT
        self.first_update = pd.NaT

        # Time series dataframe
        self.data = pd.DataFrame()
        self.index = pd.Index([])
        self.columns = pd.Index([])

        # initalize
        try:
            if self.create_map == 'create':
                if (not startDate is None) & (value is None):
                    # create new shared memory empty
                    self.startDate = startDate
                    self.columns = columns
                    self.malloc_create()

                elif (not value is None):
                    # create new shared memory with value
                    self.startDate = value.index[0]
                    self.columns = value.columns
                    self.malloc_create()
                    sidx = np.array([self.get_loc_symbol(s)
                                    for s in self.columns])
                    ts = value.index.values.astype(np.int64)/10**9  # seconds
                    tidx = self.get_loc_timestamp(ts)
                    self.setValuesJit(self.data.values, tidx,
                                      sidx, value.values)

                elif (value is None):
                    Logger.log.error('Tag %s/%s not mapped!' %
                                     (self.source, self.tag))
                    # read & allocate data
                    tini = time.time()
                    datasize = self.container.read()
                    datasize /= (1024*1024)
                    te = time.time()-tini+0.000001
                    Logger.log.debug('read %s/%s %.2fMB in %.2fs %.2fMBps ' %
                                     (self.source, self.tag, datasize, te, datasize/te))

            elif self.create_map == 'map':
                # map existing shared memory
                self.malloc_map()
                if (not value is None):
                    iidx = value.index.intersection(self.data.index)
                    icol = value.columns.intersection(self.data.columns)
                    self.data.loc[iidx, icol] = value.loc[iidx, icol].copy()
        except Exception as e:
            path, shm_name = self.get_path()
            Logger.log.error('Error initalizing %s!\n%s' % (shm_name, str(e)))
            self.free()

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
        path = path / self.tag
        path = Path(str(path).replace('\\', '/'))
        
        return path, shm_name

    def ismalloc(self):
        path, shm_name = self.get_path()
        [self.shm, ismalloc] = self.shareddata.malloc(shm_name)
        return ismalloc

    def malloc_create(self):
        path, shm_name = self.get_path()
        self.symbolidx = {}
        for i in range(len(self.columns)):
            self.symbolidx[self.columns.values[i]] = i
        self.index = self.container.getTimeIndex(self.startDate)
        self.ctimeidx = self.container.getContinousTimeIndex(self.startDate)
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

            self.shmarr[:] = np.nan

            self.data = pd.DataFrame(self.shmarr,
                                     index=self.index,
                                     columns=self.columns,
                                     copy=False)

            return True
        except Exception as e:
            Logger.log.error('Failed to malloc_create\n%s' % str(e))
            raise Exception('Failed to malloc_create\n%s' % str(e))            

    def malloc_map(self):
        try:  # try map memory file
            path, shm_name = self.get_path()
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

            return True
        except Exception as e:
            Logger.log.error('Failed to malloc_map\n%s' % str(e))
            return False

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
        path, shm_name = self.get_path()
        self.shareddata.free(shm_name)
