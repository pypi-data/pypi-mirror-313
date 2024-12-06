import pandas as pd
import numpy as np
import os
import time
from multiprocessing import shared_memory


import SharedData.TableIndexJit as TableIndexJit
from SharedData.TableIndexJit import *
from SharedData.Logger import Logger
from SharedData.Database import DATABASE_PKEYS

class TableIndex:        

    def __init__(self, table):
        self.table = table
        self.shareddata = self.table.shareddata

        self.initialized = False

        # primary key hash table
        self.pkeycolumns = TableIndex.get_pkeycolumns(self.table.database)
        self.pkeystr = '_'.join(self.pkeycolumns)
        self.pkey = np.ndarray([],dtype=np.int64)
        # date index
        self.dateiniidx = np.ndarray([],dtype=np.int64)
        self.dateendidx = np.ndarray([],dtype=np.int64)
        self.dateunit = 1
        # symbol index
        self.symbollastidx = np.ndarray([],dtype=np.int64)
        self.symbolprevidx = np.ndarray([],dtype=np.int64)
        # portfolio index
        self.portlastidx = np.ndarray([],dtype=np.int64)
        self.portprevidx = np.ndarray([],dtype=np.int64)

    def initialize(self):
        errmsg = ''
        try:

            self.get_functions()

            self.malloc()

            # check if index was created            
            if self.table.hdr['isidxcreated'] == 0:
                self.create_index()
                self.table.hdr['isidxcreated'] = 1
                if self.table.type==1:
                    self.table.shf_hdr.flush()
                    self.flush()
            
            self.table.hdr['hasindex'] = 1
            self.initialized = True
        except Exception as e:
            errmsg = 'Failed to intialize index for %s!\n%s' % (self.table.relpath, str(e))            
            self.initialized = False
        finally:            
            if not self.initialized:
                Logger.log.error(errmsg)
                raise Exception(errmsg)

    def get_functions(self):
        # primary key & index functions
        self.create_index_func = None
        self.upsert_func = None
        self.get_loc_func = None

        create_pkey_fname = 'create_pkey_' + self.pkeystr + '_jit'
        if hasattr(TableIndexJit, create_pkey_fname):
            self.create_index_func = getattr(TableIndexJit, create_pkey_fname)
        else:
            raise Exception('create_pkey function not found for database %s!'
                            % (self.table.database))

        upsert_fname = 'upsert_' + self.pkeystr + '_jit'
        if hasattr(TableIndexJit, upsert_fname):
            self.upsert_func = getattr(TableIndexJit, upsert_fname)
        else:
            raise Exception('upsert function not found for database %s!'
                            % (self.table.database))

        get_loc_fname = 'get_loc_' + self.pkeystr + '_jit'
        if hasattr(TableIndexJit, get_loc_fname):
            self.get_loc_func = getattr(TableIndexJit, get_loc_fname)
        else:
            raise Exception('get_loc function not found for database %s!'
                            % (self.table.database))        

    def malloc(self):
        shm_name = self.table.shm_name
        self.malloc_pkey(shm_name)
        if 'date' in self.pkeystr:
            self.malloc_dateidx(shm_name)
        if ('symbol' in self.pkeystr) & (len(self.pkeycolumns) > 1):
            self.malloc_symbolidx(shm_name)
        if ('portfolio' in self.pkeystr) | ('tag' in self.pkeystr):
            self.malloc_portfolioidx(shm_name)        

    def malloc_pkey(self, shm_name):
        # TODO: bug when records.size is 0
        keysize = int(self.table.records.size*3)
        keysize_bytes = int(keysize * 8)
                
        if self.table.type==2:
            [self.pkeyshm, ismalloc] = self.shareddata.malloc(shm_name+'#pkey')
            if not ismalloc:
                [self.pkeyshm, ismalloc] = self.shareddata.malloc(shm_name+'#pkey',
                    create=True, size=keysize_bytes)
                self.table.hdr['isidxcreated'] = 0
            self.pkey = np.ndarray((keysize,), dtype=np.int64,
                               buffer=self.pkeyshm.buf)
        elif self.table.type==1:
            self.pkeypath = str(self.table.filepath)\
                .replace('data.bin', 'pkey.bin')
            
            resetfile = False
            if (not os.path.exists(self.pkeypath)):
                resetfile = True
            elif os.path.getsize(self.pkeypath) != keysize_bytes:
                resetfile = True            

            if resetfile:
                self.create_file(self.pkeypath,keysize_bytes)
                self.table.hdr['isidxcreated'] = 0
                        
            self.pkey = np.memmap(self.pkeypath, np.int64, 'r+', 0, (keysize,))

        if self.table.hdr['isidxcreated'] == 0:
            self.pkey[:] = -1

    def malloc_dateidx(self, shm_name):
        # date index
        dtunit = str(self.table.records.dtype[0]).split('[')[-1].split(']')[0]
        if dtunit == 'ns':
            self.dateunit = 24*60*60*1000*1000*1000
        else:
            raise Exception('Only dates with ns precision are supported!')
        maxdate = np.datetime64('2070-01-01', 'D')
        dateidxsize = maxdate.astype(np.int64)
        dateidxsize_bytes = int(dateidxsize * 8)

        
        if self.table.type==2:
            [self.dateidxshm, ismalloc] = self.shareddata.malloc(shm_name+'#dateidx')
            if not ismalloc:
                [self.dateidxshm, ismalloc] = self.shareddata.malloc(shm_name+'#dateidx',
                                                                    create=True, size=int(dateidxsize_bytes*2))
                self.table.hdr['isidxcreated'] = 0

            self.dateiniidx = np.ndarray(
                (dateidxsize,), dtype=np.int64, buffer=self.dateidxshm.buf)
            self.dateendidx = np.ndarray((dateidxsize,), dtype=np.int64, buffer=self.dateidxshm.buf,
                                        offset=dateidxsize_bytes)
        elif self.table.type==1:
            self.dateidxpath = str(self.table.filepath).replace('data.bin', 'dateidx.bin')
            if not os.path.exists(self.dateidxpath):
                self.create_file(self.dateidxpath,dateidxsize_bytes)
                self.table.hdr['isidxcreated'] = 0
                        
            self.dateiniidx = np.memmap(self.dateidxpath, np.int64, 'r+', 0, (dateidxsize,))
            self.dateendidx = np.memmap(self.dateidxpath, np.int64, 'r+', dateidxsize_bytes, (dateidxsize,))            

        if self.table.hdr['isidxcreated'] == 0:            
            self.dateiniidx[:] = -1
            self.dateendidx[:] = -1

    def malloc_symbolidx(self, shm_name):
        hashtblsize = int(self.table.records.size*3)
        hashtblsize_bytes = int(hashtblsize * 8)
        listsize = self.table.records.size
        listsize_bytes = int(listsize * 8)
        size_bytes = int(hashtblsize_bytes+listsize_bytes)

        # symbol index
        
        if self.table.type==2:
            [self.symbolidxshm, ismalloc] = self.shareddata.malloc(
                shm_name+'#symbolidx')
            if not ismalloc:
                [self.symbolidxshm, ismalloc] = self.shareddata.malloc(shm_name+'#symbolidx',
                    create=True, size=size_bytes)
                self.table.hdr['isidxcreated'] = 0

            self.symbollastidx = np.ndarray(
                (hashtblsize,), dtype=np.int64, buffer=self.symbolidxshm.buf)
            self.symbolprevidx = np.ndarray((listsize,), dtype=np.int64, buffer=self.symbolidxshm.buf,
                                            offset=hashtblsize_bytes)
        elif self.table.type==1:
            self.symbolidxpath = str(self.table.filepath).replace('data.bin', 'symbolidx.bin')            
            
            resetfile = False
            if (not os.path.exists(self.symbolidxpath)):
                resetfile = True                
            elif os.path.getsize(self.symbolidxpath) != size_bytes:
                resetfile = True

            if resetfile:
                self.create_file(self.symbolidxpath,size_bytes)
                self.table.hdr['isidxcreated'] = 0

            
            self.symbollastidx = np.memmap(self.symbolidxpath, np.int64, 'r+', 0, (hashtblsize,))
            self.symbolprevidx = np.memmap(self.symbolidxpath, np.int64, 'r+', hashtblsize_bytes, (listsize,))            

        if self.table.hdr['isidxcreated'] == 0:
            self.symbollastidx[:] = -1
            self.symbolprevidx[:] = -1

    def malloc_portfolioidx(self, shm_name):
        hashtblsize = int(self.table.records.size*3)
        hashtblsize_bytes = int(hashtblsize * 8)
        listsize = self.table.records.size
        listsize_bytes = int(listsize * 8)
        size_bytes = int(hashtblsize_bytes+listsize_bytes)

        # portfolio index
        
        if self.table.type==2:
            [self.portidxshm, ismalloc] = self.shareddata.malloc(
                shm_name+'#portidx')
            if not ismalloc:
                [self.portidxshm, ismalloc] = self.shareddata.malloc(shm_name+'#portidx',
                    create=True, size=size_bytes)
                self.table.hdr['isidxcreated'] = 0

            self.portlastidx = np.ndarray(
                (hashtblsize,), dtype=np.int64, buffer=self.portidxshm.buf)
            self.portprevidx = np.ndarray((listsize,), dtype=np.int64, buffer=self.portidxshm.buf,
                                        offset=hashtblsize_bytes)
        elif self.table.type==1:
            self.portidxpath = str(self.table.filepath).replace('data.bin', 'portidx.bin')
            
            resetfile = False
            if (not os.path.exists(self.portidxpath)):
                resetfile = True                
            elif os.path.getsize(self.portidxpath) != size_bytes:
                resetfile = True
            if resetfile:
                self.create_file(self.portidxpath,size_bytes)
                self.table.hdr['isidxcreated'] = 0
            
            self.portlastidx = np.memmap(self.portidxpath, np.int64, 'r+', 0, (hashtblsize,))
            self.portprevidx = np.memmap(self.portidxpath, np.int64, 'r+', hashtblsize_bytes, (listsize,))            

        if self.table.hdr['isidxcreated'] == 0:
            self.portlastidx[:] = -1
            self.portprevidx[:] = -1    

    def create_index(self,start=0,update=False):
        ti = time.time()
        if self.table.records.count > 0:
            if not update:
                print('Creating index %s %i lines...' %
                    (self.table.relpath, self.table.records.count))                
            else:
                print('Updating index %s %i lines...' %
                    (self.table.relpath, self.table.records.count))
            time.sleep(0.001)
    
            # TODO: CREATE AN UPDATE METHOD
            start = 0
            self.pkey[:] = -1
            if 'date' in self.pkeystr:
                self.dateiniidx[:] = -1
                self.dateendidx[:] = -1
            arr = self.table.records.records
            rec = self.table.records[:]
            # deduplicate array
            if len(self.pkeycolumns)==1:
                unique, indices, inverse = np.unique(
                    rec[self.pkeycolumns],
                    return_index=True, return_inverse=True
                    )
            else:
                unique, indices, inverse = np.unique(
                    rec[self.pkeycolumns], axis=0, 
                    return_index=True, return_inverse=True
                    )
            # get the indices of the not duplicated rows 
            # while keeping the first element of the duplicated rows
            if len(unique) < len(rec):
                Logger.log.warning('Duplicated records found in %s!' %
                                   self.table.relpath)
                ndids = np.concatenate((indices, np.where(inverse == np.arange(len(unique)))[0]))
                ndids = np.unique(ndids)
                self.table.records[:len(ndids)] = arr[ndids]
                self.table.hdr['count'] = len(ndids)
                
            
            success=False
            if ('date_portfolio_symbol' in self.pkeystr) | ('date_tag_symbol' in self.pkeystr):
                self.symbollastidx[:] = -1
                self.symbolprevidx[:] = -1
                self.portlastidx[:] = -1
                self.portprevidx[:] = -1
                success = self.create_index_func(arr, self.table.records.count, self.pkey,
                                                self.dateiniidx, self.dateendidx, self.dateunit, \
                                                self.portlastidx, self.portprevidx, \
                                                self.symbollastidx, self.symbolprevidx,  start)
            elif 'date_symbol' in self.pkeystr:
                self.symbollastidx[:] = -1
                self.symbolprevidx[:] = -1
                success = self.create_index_func(arr, self.table.records.count, self.pkey,
                                                 self.dateiniidx, self.dateendidx, self.dateunit, \
                                                self.symbollastidx, self.symbolprevidx, start)
            elif 'date_portfolio' in self.pkeystr:
                self.portlastidx[:] = -1
                self.portprevidx[:] = -1
                success = self.create_index_func(arr, self.table.records.count, self.pkey,
                                                self.dateiniidx, self.dateendidx, self.dateunit, \
                                                self.portlastidx, self.portprevidx, start)
            elif 'symbol' in self.pkeystr:                
                success = self.create_index_func(arr, self.table.records.count, self.pkey, start)
            else:
                errmsg = 'TableIndex.create_index(): create_index_func not enabled!'
                Logger.log.error(errmsg)
                raise Exception(errmsg)
            
            if not success:
                errmsg = ('Error creating index %s!!!' % (self.table.relpath))
                Logger.log.error(errmsg)
                raise Exception(errmsg)
                                    
            print('Creating index %s %i lines/s DONE!' %
                  (self.table.relpath, self.table.records.count/(time.time()-ti)))

    def update_index(self, start):                
        self.create_index(start,update=True)        

    def sort_index(self, shnumpy, start=0):
        
        try:
            self.table.acquire()
            
            keys = tuple(shnumpy[column][start:]
                         for column in self.pkeycolumns[::-1])
            idx = np.lexsort(keys)

            shift_idx = np.roll(idx, 1)
            if len(shift_idx) > 0:
                shift_idx[0] = -1
                idx_diff = idx - shift_idx
                unsortered_idx = np.where(idx_diff != 1)[0]
                if np.where(idx_diff != 1)[0].any():
                    _minchgid = np.min(unsortered_idx) + start
                    shnumpy.minchgid = _minchgid
                    shnumpy[start:] = shnumpy[start:][idx]
                    self.table.hdr['isidxcreated'] = 0
                    self.update_index(_minchgid)
                    self.table.hdr['isidxcreated'] = 1

        except Exception as e:
            Logger.log.error('Error sorting index!\n%s' % (e))
        finally:
            self.table.release()

    def create_file(self,fpath,size):
        with open(fpath, 'wb') as f:
            # Seek to the end of the file
            f.seek(size-1)
            # Write a single null byte to the end of the file
            f.write(b'\x00')
            if os.name == 'posix':
                os.posix_fallocate(f.fileno(), 0, size)
            elif os.name == 'nt':
                pass # TODO: implement windows file allocation

    def flush(self):        
        if self.pkey.size>1:
            mtime = self.table.hdr['mtime']
            self.pkey.flush()
            os.utime(self.pkeypath, (mtime, mtime))
            if 'date' in self.pkeystr:
                self.dateiniidx.flush()
                self.dateendidx.flush()
                os.utime(self.dateidxpath, (mtime, mtime))
            if 'date_symbol' in self.pkeystr:
                self.symbollastidx.flush()
                self.symbolprevidx.flush()
                os.utime(self.symbolidxpath, (mtime, mtime))
            if 'portfolio' in self.pkeystr:
                self.portlastidx.flush()
                self.portprevidx.flush()
                os.utime(self.portidxpath, (mtime, mtime))
        
    def free(self):        
        try:
            self.flush()
            if self.pkey.size>0:
                self.pkey = None      
                if 'date' in self.pkeystr:      
                    self.dateiniidx = None
                    self.dateendidx = None
                if 'date_symbol' in self.pkeystr:
                    self.symbollastidx = None                
                    self.symbolprevidx = None            
                if 'portfolio' in self.pkeystr:
                    self.portlastidx = None                
                    self.portprevidx = None
        except Exception as e:
            Logger.log.error(f"TableIndex.free() {self.table.relpath}: {e}")

    @staticmethod
    def get_pkeycolumns(database):    
        if database in DATABASE_PKEYS:
            return DATABASE_PKEYS[database]
        else:
            raise Exception('Database not implemented!')
