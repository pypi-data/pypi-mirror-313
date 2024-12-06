import os
import threading
import time
import pandas as pd
import numpy as np
from pathlib import Path
from multiprocessing import shared_memory
import gzip
import io
import hashlib
from datetime import datetime
from tqdm import tqdm
import threading
import psutil


from SharedData.SharedNumpy import SharedNumpy
from SharedData.Table import Table

from SharedData.Utils import cpp


class TableMemory(Table):
    # TODO: create partitioning option yearly, monthly, daily

    def __init__(self, shareddata, database, period, source, tablename,
                records=None, names=None, formats=None, size=None,\
                overwrite=False, user='master',partitioning=None):
        self.type = 2
        self.shf_hdr = np.array([])
        self.shf_data = np.array([])
        super().__init__(shareddata, database, period, source, tablename,
                         records=records, names=names, formats=formats, size=size,
                         overwrite=overwrite, user=user, tabletype=self.type, partitioning=partitioning)
       
    ############### MALLOC ###############
    def malloc(self):
        if self.size is None:
            self.size = self.hdr['recordssize']
        nb_hdr = self.hdrdtype.itemsize  # number of header bytes
        # number of data bytes
        nb_records = int(self.hdr['recordssize']*self.hdr['itemsize'])
        total_size = int(nb_hdr+nb_records)

        [self.shm, ismalloc] = \
            self.shareddata.malloc(self.shm_name, create=True, size=total_size)
        if not ismalloc:
            raise Exception('Could not allocate shared memory!')

        # allocate header
        self.shm.buf[0:nb_hdr] = self.hdr.tobytes()
        self.hdr = np.ndarray((1,), dtype=self.hdrdtype,
                              buffer=self.shm.buf)[0]
        # allocate table data
        self.records = SharedNumpy('MEMORY',shape=(self.hdr['recordssize'],),
                                   dtype=self.recdtype, buffer=self.shm.buf, offset=nb_hdr)
        self.records.table = self
        self.records.preallocate()

    ############### FREE ###############
    def free(self):
        self.acquire()
        self.shareddata.free(self.shm_name)
        self.shareddata.free(self.shm_name+'#pkey')
        self.shareddata.free(self.shm_name+'#dateidx')
        self.shareddata.free(self.shm_name+'#symbolidx')
        self.shareddata.free(self.shm_name+'#portidx')
        self.shareddata.free(self.shm_name+'#dtportidx')
        self.release()
        self.shareddata.free(self.shm_name+'#mutex')  # release
        del self.shareddata.data[self.relpath]
   
    ############### WRITE ###############
    def write_head(self, mtime):
        nb_header = int(self.hdrdtype.itemsize)
        nb_head = int(self.hdr['headsize']*self.hdr['itemsize'])
        with open(self.filepath, 'wb') as f:
            f.write(self.shm.buf[0:nb_header])
            headsize_mb = nb_head / (1000000)
            blocksize = 1024*1024*100
            descr = 'Writing head:%iMB %s' % (headsize_mb, self.relpath)
            with tqdm(total=nb_head, unit='B', unit_scale=True, desc=descr) as pbar:
                written = 0
                while written < nb_head:
                    # write in chunks of max 100 MB size
                    chunk_size = min(blocksize, nb_head-written)
                    ib = nb_header+written
                    eb = nb_header+written+chunk_size
                    f.write(self.shm.buf[ib:eb])
                    written += chunk_size
                    pbar.update(chunk_size)
            f.flush()
        os.utime(self.filepath, (mtime, mtime))

    def write_tail(self, mtime):
        nb_header = int(self.hdrdtype.itemsize)
        nb_head = int(self.hdr['headsize']*self.hdr['itemsize'])
        nb_tail = int(self.tailhdr['tailsize']*self.hdr['itemsize'])

        with open(self.tailpath, 'wb') as f:
            f.write(self.tailhdr)
            tailsize_mb = nb_tail / (1000000)
            blocksize = 1024*1024*100  # 100 MB
            descr = 'Writing tail:%iMB %s' % (tailsize_mb, self.relpath)

            # Setup progress bar for tail
            with tqdm(total=nb_tail, unit='B', unit_scale=True, desc=descr) as pbar:
                written = 0
                while written < nb_tail:
                    # write in chunks of max 100 MB size
                    chunk_size = min(blocksize, nb_tail-written)
                    ib = nb_header+nb_head+written
                    eb = ib+chunk_size
                    f.write(self.shm.buf[ib:eb])
                    written += chunk_size
                    pbar.update(chunk_size)
            f.flush()
        os.utime(self.tailpath, (mtime, mtime))

