import pandas as pd
import numpy as np
import time
from datetime import datetime
from tqdm import tqdm
import os

from SharedData.Logger import Logger
from SharedData.TableIndexJit import get_symbol_loc, get_portfolio_loc, get_tag_loc, djb2_hash
from SharedData.Utils import mmaparray2df
       
class SharedNumpy(np.ndarray):

    def __new__(cls, type, *args, **kwargs):
        if type == 'MEMORY':
            obj = np.ndarray.__new__(cls, *args, **kwargs)
            obj.table = None
            return obj
        elif type == 'DISK':
            memmap = args[0]
            obj = memmap.view(cls)
            obj.memmap = memmap
            obj.table = None
            obj._df = None
            return obj
        else:
            raise Exception('Unknown type %s!' % (type))

    
    def preallocate(self):
        # TODO: REVISE PREALLOCATE NOT CONSUMING MEMORY
        arr = super().__getitem__(slice(0, self.size))
        sizeb = self.size*self.itemsize
        sizemb = sizeb / 10**6
        if sizemb > 500:
            blocksize = int(1000*10**6/self.itemsize)
            descr = 'Preallocating:%iMB %s' % (sizemb, self.table.relpath)
            with tqdm(total=sizeb, unit='B', unit_scale=True, desc=descr) as pbar:
                allocated = 0
                while allocated < self.size:
                    # write in chunks of max 100 MB size
                    chunk_size = min(blocksize, self.size-allocated)
                    arr['mtime'][allocated:chunk_size] = np.datetime64('NaT')
                    allocated += chunk_size
                    pbar.update(chunk_size*self.itemsize)
        else:
            arr['mtime'][:] = np.datetime64('NaT')

    def free(self):
        self.table.free()

    def trim(self):
        self.table.trim()

    def write(self,force_write=False):
        if self.count > 0:
            self.table.write(force_write)
        

    def rememmap(self):
        memmap = np.memmap(self.table.filepath, self.table.recdtype, 'r+', self.table.hdr.dtype.itemsize, (self.recordssize,))
        new_instance = memmap.view(self.__class__)
        new_instance.table = self.table
        new_instance.memmap = memmap
        self.table.records = new_instance
        return new_instance
    
    def reload(self):
        return self.table.reload()
    
    ################################# SYNC TABLE ########################################
    def subscribe(self, host, port=None, lookbacklines=1000, lookbackdate=None, method='websocket', snapshot=False, bandwidth=1e6, protocol='http'):
        self.table.subscribe(host, port, lookbacklines,
                             lookbackdate, method, snapshot, bandwidth,protocol)
        
    def publish(self, host, port=None, lookbacklines=1000, lookbackdate=None, method='websocket', snapshot=False, bandwidth=1e6, protocol='http'):
        self.table.publish(host, port, lookbacklines,
                             lookbackdate, method, snapshot, bandwidth,protocol)
    
    def read_stream(self, buffer):
        
        if len(buffer) >= self.itemsize:
            # Determine how many complete records are in the buffer
            num_records = len(
                buffer) // self.itemsize
            # Take the first num_records worth of bytes
            record_data = buffer[:num_records *
                                        self.itemsize]
            # And remove them from the buffer
            del buffer[:num_records *
                                self.itemsize]
            # Convert the bytes to a NumPy array of records
            rec = np.frombuffer(
                record_data, dtype=self.dtype)
            
            if self.table.hasindex:
                # Upsert all records at once
                self.upsert(rec)
            else:
                # Extend all records at once
                self.extend(rec)

        return buffer

    ############################## KEYLESS OPERATIONS ########################################

    def insert(self, new_records, acquire=True):
        errmsg = ''
        try:
            if acquire:
                self.table.acquire()

            nrec = new_records.size
            _count = self.count
            if (_count + nrec <= self.size):
                # convert new_records
                if (self.dtype != new_records.dtype):
                    new_records = self.convert(new_records)
                # fill mtime
                nidx = np.isnat(new_records['mtime'])
                if nidx.any():
                    new_records['mtime'][nidx] = time.time_ns()

                arr = super().__getitem__(slice(0, self.size))
                arr[_count:_count+nrec] = new_records
                self.count = _count + nrec
                self.mtime = datetime.now().timestamp()
            else:
                errmsg = 'Table max size reached!'
                Logger.log.error(errmsg)
        except Exception as e:
            errmsg = 'Error inserting %s!\n%s' % (self.table.relpath, str(e))
            Logger.log.error(errmsg)
        finally:
            if acquire:
                self.table.release()
            if errmsg:
                raise Exception(errmsg)

    def extend(self, new_records, acquire=True):
        errmsg = ''
        if self.table.type == 'MEMORY':
                raise Exception(
                    'Table %s is in memory, extend not supported!' % (self.table.relpath))

        if self.table.hdr['hasindex'] == 1:
            raise Exception(
                'Table %s has index, extend not supported!' % (self.table.relpath))
        
        try:            
            if acquire:
                self.table.acquire()
            
            if self.size < self.recordssize:
                self = self.rememmap()

            nrec = new_records.size
            _count = self.count.copy()
            
            if (_count + nrec > self.recordssize):
                # extend table by 10MB
                rec = self.table.records
                page_size = 4096
                extend_size = int(np.round(100 * 1024 * 1024 / page_size) * page_size)
                new_rows = int(np.floor(extend_size/rec.dtype.itemsize))
                new_rows = max(new_rows, nrec)

                new_recordssize = rec.size + new_rows
                hdr_bytes = self.table.hdr.dtype.itemsize
                rec_bytes = rec.dtype.itemsize * rec.size                
                totalbytes = hdr_bytes + rec_bytes + rec.dtype.itemsize*new_rows
                
                with open(self.table.filepath, 'ab+') as f:
                    # Seek to the end of the file
                    f.seek(totalbytes-1)
                    # Write a single null byte to the end of the file
                    f.write(b'\x00')
                    if os.name == 'posix':
                        os.posix_fallocate(f.fileno(), 0, totalbytes)
                    elif os.name == 'nt':
                        pass  # TODO: implement preallocation for windows in pyd

                # remap extended file
                self.table.shf_data.flush()
                self.table.shf_data = np.memmap(
                    self.table.filepath,rec.dtype,'r+',
                    hdr_bytes,(new_recordssize,) )
                self.table.records = SharedNumpy('DISK', self.table.shf_data)
                self.table.records.table = self.table                
                self.recordssize = new_recordssize

            # convert new_records
            if (self.dtype != new_records.dtype):
                new_records = self.convert(new_records)
            # fill mtime
            nidx = np.isnat(new_records['mtime'])
            if nidx.any():
                new_records['mtime'][nidx] = time.time_ns()
            # insert data
            self.table.records.insert(new_records, acquire=False)
            
            return self.table.records
        

        except Exception as e:
            errmsg = 'Error extending %s!\n%s' % (self.table.relpath, str(e))
            Logger.log.error(errmsg)
        finally:
            if acquire:
                self.table.release()
            if errmsg:
                raise Exception(errmsg)

    ############################## PRIMARY KEY OPERATIONS ########################################
    @property
    def loc(self):
        return _LocIndexer(self)

    def upsert(self, new_records, acquire=True):
        # TODO: check if index variables are valid
        if self.table.hdr['hasindex'] == 0:
            raise Exception('Table %s has no index!' % (self.table.relpath))

        if new_records.size > 0:

            # convert to same dtype record
            if isinstance(new_records, pd.DataFrame):
                new_records = self.table.df2records(new_records)
            elif (self.dtype != new_records.dtype):
                new_records = self.convert(new_records)

            # fill mtime
            nidx = np.isnat(new_records['mtime'])
            if nidx.any():
                new_records['mtime'][nidx] = time.time_ns()

            # remove invalid mtime
            invalididx = new_records['mtime'].astype(int) > time.time_ns()
            if invalididx.any():
                new_records = new_records[~invalididx]

            # check for null date
            if self.table.database!='Symbols':
                invalididx = np.isnat(new_records['date'])
                if invalididx.any():
                    new_records = new_records[~invalididx]

            if new_records.size > 0:
                # single record to array
                if new_records.shape == ():
                    new_records = np.array([new_records])

                try:
                    success = True
                    if acquire:
                        self.table.acquire()

                    # check if index is created & valid
                    if self.table.hdr['isidxcreated'] == 0:
                        self.index.create_index(self, self.pkey)

                    # upsert
                    minchgid = self.count
                    arr = super().__getitem__(slice(0, self.size))

                    self.table.hdr['isidxcreated'] == 0

                    self.count, minchgid = self.index.upsert_func(
                        arr, self.count, new_records, self.pkey,
                        self.index.dateiniidx, self.index.dateendidx, self.index.dateunit,
                        self.index.portlastidx, self.index.portprevidx,
                        self.index.symbollastidx, self.index.symbolprevidx)

                    self.table.hdr['isidxcreated'] == 1
                    minchgid = int(minchgid)
                    self.minchgid = minchgid
                    self.mtime = datetime.now().timestamp()

                except Exception as e:
                    Logger.log.error('Error upserting %s!\n%s' %
                                     (self.table.relpath, str(e)))
                    success = False
                finally:
                    if acquire:
                        self.table.release()
                    # table full
                    if self.count == self.size:
                        Logger.log.warning('Table %s is full!' %
                                           (self.table.relpath))
                    if not success:
                        raise Exception('Error upserting %s!' %
                                        (self.table.relpath))
                return minchgid

        return self.count

    def sort_index(self, start=0):
        self.index.sort_index(self, start)

    def get_loc(self, keys, acquire=True):
        success = False
        try:
            if acquire:
                self.table.acquire()

            # check if index is created & valid
            if self.table.hdr['isidxcreated'] == 0:
                self.index.create_index(self, self.pkey)

            loc = self.index.get_loc_func(
                self[:], self.pkey, keys).astype(np.int64)
            success = True
        except Exception as e:
            Logger.log.error('Error getting loc for %s!\n%s' %
                             (self.table.relpath, str(e)))
            loc = np.array([])
        finally:
            if acquire:
                self.table.release()
            if not success:
                raise Exception('Error getting loc for %s!' %
                                (self.table.relpath))
        return loc

    def get_date_loc(self, date):
        success = False
        try:
            self.table.acquire()

            # check if index is created & valid
            if self.table.hdr['isidxcreated'] == 0:
                self.index.create_index(self, self.pkey)

            if isinstance(date, np.datetime64):
                date = pd.Timestamp(date)
            dtint = int(date.value/24/60/60/10**9)
            dtiniid = self.index.dateiniidx[dtint]
            dtendid = self.index.dateendidx[dtint]
            success = True
        except Exception as e:
            Logger.log.error('Error getting date_loc for %s!\n%s' %
                             (self.table.relpath, str(e)))
        finally:
            self.table.release()
            if not success:
                raise Exception('Error getting date_loc for %s!' %
                                (self.table.relpath))
        return [dtiniid, dtendid+1]

    def get_symbol_loc(self, symbol, maxids=0):
        success = False
        try:
            self.table.acquire()
            # check if index is created & valid
            if self.table.hdr['isidxcreated'] == 0:
                self.index.create_index(self, self.pkey)

            if not isinstance(symbol, bytes):
                symbol = symbol.encode('utf-8')
            
            _rec = np.full((1,),np.nan,dtype=self.dtype)
            _rec['symbol'] = symbol
            loc = get_symbol_loc(self[:], self.index.symbollastidx,
                                 self.index.symbolprevidx, _rec, maxids)
            success = True
        except Exception as e:
            Logger.log.error('Error getting symbol_loc for %s!\n%s' %
                             (self.table.relpath, str(e)))
        finally:
            self.table.release()
            if not success:
                raise Exception('Error getting symbol_loc for %s!' %
                                (self.table.relpath))
        return loc

    def get_portfolio_loc(self, portfolio, maxids=0):
        success = False
        try:
            self.table.acquire()
            # check if index is created & valid
            if self.table.hdr['isidxcreated'] == 0:
                self.index.create_index(self, self.pkey)

            if not isinstance(portfolio, bytes):
                portfolio = portfolio.encode('utf-8')
            
            _rec = np.full((1,),np.nan,dtype=self.dtype)
            _rec['portfolio'] = portfolio
            loc = get_portfolio_loc(
                self[:], self.index.portlastidx, self.index.portprevidx, _rec, maxids)
            success = True
        except Exception as e:
            Logger.log.error('Error getting portfolio_loc for %s!\n%s' %
                             (self.table.relpath, str(e)))
        finally:
            self.table.release()
            if not success:
                raise Exception('Error getting portfolio_loc for %s!' %
                                (self.table.relpath))
        return loc

    def get_tag_loc(self, tag, maxids=0):
        success = False
        try:
            self.table.acquire()
            # check if index is created & valid
            if self.table.hdr['isidxcreated'] == 0:
                self.index.create_index(self, self.pkey)

            if not isinstance(tag, bytes):
                tag = tag.encode('utf-8')

            _rec = np.full((1,),np.nan,dtype=self.dtype)
            _rec['tag'] = tag

            loc = get_tag_loc(
                self[:], self.index.portlastidx, self.index.portprevidx, _rec, maxids)
            success = True
        except Exception as e:
            Logger.log.error('Error getting tag_loc for %s!\n%s' %
                             (self.table.relpath, str(e)))
        finally:
            self.table.release()
            if not success:
                raise Exception('Error getting tag_loc for %s!' %
                                (self.table.relpath))
        return loc

    ############################## CONVERSION ##############################
    @property
    def df(self):
        mmap_df = False
        if self._df is not None:
            if self._df.shape[0] < self.count:
                mmap_df = True
        else:
            mmap_df = True
            
        if mmap_df:
            indexcols = len(self.table.index.pkeycolumns)
            self._df = mmaparray2df(self[:], indexcols)            

        return self._df
                    
    def records2df(self, records):
        return self.table.records2df(records)

    def df2records(self, df):
        return self.table.df2records(df)

    def convert(self, new_records):
        rec = np.full((new_records.size,), fill_value=np.nan, dtype=self.dtype)
        for col in self.dtype.names:
            if col in new_records.dtype.names:
                try:
                    rec[col] = new_records[col].astype(self.dtype[col])
                except:
                    Logger.log.error('Could not convert %s!' % (col))
        return rec

    def tags2df(self, dt, seltags, datetags=None):
        idx = pd.Index([])
        df = pd.DataFrame(columns=seltags)
        dfmtime = pd.DataFrame(columns=seltags)
        tag = seltags[0]        
        for tag in seltags:
            try:
                rec = self.loc[dt,tag]
                if len(rec)>0:            
                    values = self.records2df(rec).loc[dt].droplevel(0)
                    idx = idx.union(values.index)
                    df = df.reindex(idx)    
                    if not datetags is None:
                        if tag in datetags:
                            values['value'] = values['value'].apply(lambda x: pd.Timestamp.fromtimestamp(x))
                    df[tag] = values['value']
                    dfmtime[tag] = values['mtime']
            except Exception as e:
                Logger.log.error('Could not get %s %s!' % (tag,e))
        return df, dfmtime


    ############################## GETTERS / SETTERS ##############################    

    def __getitem__(self, key):
        if hasattr(self, 'table'):
            if self.size < self.recordssize:
                self = self.rememmap()

            arr = super().__getitem__(slice(0, self.count))  # slice arr
            if self.count > 0:
                return arr.__getitem__(key)
            else:
                return arr
        else:
            return super().__getitem__(key)
    
    def get_exists_remote(self):
        return self.table.get_exists_remote()

    @property
    def records(self):
        return super().__getitem__(slice(0, self.size))

    @property
    def count(self):
        return self.table.hdr['count']

    @count.setter
    def count(self, value):
        self.table.hdr['count'] = value

    @property
    def recordssize(self):
        return self.table.hdr['recordssize']

    @recordssize.setter
    def recordssize(self, value):
        self.table.hdr['recordssize'] = value

    @property
    def mtime(self):
        return self.table.hdr['mtime']

    @mtime.setter
    def mtime(self, value):
        self.table.hdr['mtime'] = value

    @property
    def minchgid(self):
        return self.table.hdr['minchgid']

    @minchgid.setter
    def minchgid(self, value):
        value = min(value, self.table.hdr['minchgid'])
        self.table.hdr['minchgid'] = value

    @property
    def index(self):
        return self.table.index

    @index.setter
    def index(self, value):
        self.table.index = value

    @property
    def pkey(self):
        return self.table.index.pkey

    @pkey.setter
    def pkey(self, value):
        self.table.index.pkey = value


class _LocIndexer:
    def __init__(self, data):
        self.data = data

    def __setitem__(self, key, value):
        # Custom behavior here
        errmsg = "Error: loc is readonly!"
        Logger.log.error(errmsg)
        raise Exception(errmsg)
        
    def __getitem__(self, index):                
        if isinstance(index, tuple):
            row_index, col_index = index
        elif isinstance(index, pd.MultiIndex):
            row_index = index
            col_index = slice(None)
        elif isinstance(index, slice):
            row_index = index
            col_index = slice(None)
            return self.data[row_index]
        elif isinstance(index, str):
            row_index = None
            col_index = index
        
        if isinstance(row_index, slice):
            # start slice
            start = row_index.start
            if start is None:
                start = 0
            elif isinstance(start, pd.Timestamp):
                start = start.normalize()
                start = self.data.get_date_loc(start)[0]
                if start == -1:
                    start = np.where(self.data['date'] >= np.datetime64(start))[0]
                    if len(start) > 0:
                        start = start[0]
                    else:
                        return None
            # stop slice
            stop = row_index.stop
            if stop is None:
                stop = self.data.count
            elif isinstance(stop, pd.Timestamp):
                stop = stop.normalize()
                stop = self.data.get_date_loc(stop)[0]
                if stop == -1:
                    stop = np.where(self.data['date'] >= np.datetime64(stop))[0]
                    if len(stop) > 0:
                        stop = stop[0]
                    else:
                        stop = self.data.count
            # step slice
            step = row_index.step
            if step is None:
                step = 1

            if isinstance(col_index, str):
                if not col_index in self.data.dtype.names:
                    row_key = col_index
                    # check first index
                    if self.data.table.index.pkeycolumns[1] == 'symbol':
                        if start<0:
                            loc = self.data.get_symbol_loc(row_key,abs(start))
                        else:
                            loc = self.data.get_symbol_loc(row_key)
                    elif self.data.table.index.pkeycolumns[1] == 'tag':
                        if start<0:
                            loc = self.data.get_tag_loc(row_key,abs(start))
                        else:
                            loc = self.data.get_tag_loc(row_key)
                    elif self.data.table.index.pkeycolumns[1] == 'portfolio':
                        if start<0:
                            loc = self.data.get_portfolio_loc(row_key,abs(start))
                        else:
                            loc = self.data.get_portfolio_loc(row_key)
                    
                    if len(loc) > 0:
                        loc = np.array(loc[::-1])
                        loc = loc[(loc>=start) & (loc<stop)]
                        return self.data[loc]

            return self.data[start:stop:step][col_index]

        elif isinstance(row_index,pd.MultiIndex):
            dtype = np.dtype([(x,row_index.get_level_values(x).dtype) for x in row_index.names])
            rec = np.array([tuple(x) for x in row_index.values],dtype=dtype)
            rec = self.data.convert(rec)
            loc = self.data.get_loc(rec)
            loc = np.array(loc)
            loc = loc[loc>=0]
            return self.data[loc][col_index]
        
        elif isinstance(row_index, tuple):
            if len(row_index) == 2:
                row_slice, row_key = row_index
                if isinstance(row_slice, slice):
                    # start slice
                    start = row_slice.start
                    if start is None:
                        start = 0
                    elif isinstance(start, pd.Timestamp):
                        start = start.normalize()
                        start = self.data.get_date_loc(start)[0]
                        if start == -1:
                            start = np.where(self.data['date'] >= np.datetime64(start))[0]
                            if len(start) > 0:
                                start = start[0]
                            else:
                                return None
                    # stop slice
                    stop = row_slice.stop
                    if stop is None:
                        stop = self.data.count
                    elif isinstance(stop, pd.Timestamp):
                        stop = stop.normalize()
                        stop = self.data.get_date_loc(stop)[0]
                        if stop == -1:
                            stop = np.where(self.data['date'] >= np.datetime64(stop))[0]
                            if len(stop) > 0:
                                stop = stop[0]
                            else:
                                stop = self.data.count
                    # step slice
                    step = row_slice.step
                    if step is None:
                        step = 1                                                
                    
                    if isinstance(row_key, str):
                        if self.data.table.index.pkeycolumns[1] == 'symbol':
                            if start<0:
                                loc = self.data.get_symbol_loc(row_key,abs(start))
                            else:
                                loc = self.data.get_symbol_loc(row_key)
                        elif self.data.table.index.pkeycolumns[1] == 'tag':
                            if start<0:
                                loc = self.data.get_tag_loc(row_key,abs(start))
                            else:
                                loc = self.data.get_tag_loc(row_key)
                        elif self.data.table.index.pkeycolumns[1] == 'portfolio':
                            if start<0:
                                loc = self.data.get_portfolio_loc(row_key,abs(start))
                            else:
                                loc = self.data.get_portfolio_loc(row_key)
                        
                        if len(loc) > 0:
                            loc = np.array(loc[::-1])
                            loc = loc[(loc>=start) & (loc<stop)]
                            return self.data[loc][col_index]                            
                        else:
                            return None
                        
                    elif row_key is None:
                        return self.data[start:stop:step][col_index]
        
        elif isinstance(row_index, int):
            if isinstance(col_index, str):
                if not col_index in self.data.dtype.names:
                    row_key = col_index
                    # check first index
                    if self.data.table.index.pkeycolumns[1] == 'symbol':
                        if row_index<0:
                            loc = self.data.get_symbol_loc(row_key,abs(row_index))
                        else:
                            loc = self.data.get_symbol_loc(row_key)
                    elif self.data.table.index.pkeycolumns[1] == 'tag':
                        if row_index<0:
                            loc = self.data.get_tag_loc(row_key,abs(row_index))
                        else:
                            loc = self.data.get_tag_loc(row_key)
                    elif self.data.table.index.pkeycolumns[1] == 'portfolio':
                        if row_index<0:
                            loc = self.data.get_portfolio_loc(row_key,abs(row_index))
                        else:
                            loc = self.data.get_portfolio_loc(row_key)
                    
                    if len(loc) > 0:
                        loc = np.array(loc[::-1])
                        loc = loc[(loc>=row_index)]
                        return self.data[loc][row_index]
                    
            return self.data[row_index][col_index]
        elif isinstance(row_index, pd.Timestamp):
            if isinstance(col_index, str):
                if not col_index in self.data.dtype.names:
                    row_key = col_index
                    # check first index
                    if self.data.table.index.pkeycolumns[1] == 'symbol':                        
                        loc = self.data.get_symbol_loc(row_key)
                    elif self.data.table.index.pkeycolumns[1] == 'tag':                        
                        loc = self.data.get_tag_loc(row_key)
                    elif self.data.table.index.pkeycolumns[1] == 'portfolio':                    
                        loc = self.data.get_portfolio_loc(row_key)
                    if len(loc) > 0:
                        loc = np.array(loc[::-1])
                        dti,dte = self.data.get_date_loc(row_index)
                        if not dti == -1:
                            loc = loc[(loc>=dti) & (loc<=dte)]
                            return self.data[loc]
                        else:
                            return None                                            
            return self.data[row_index][col_index]
            

                
        return None

            
                
                    