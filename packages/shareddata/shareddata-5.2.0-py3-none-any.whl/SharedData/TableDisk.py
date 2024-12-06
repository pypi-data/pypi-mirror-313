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

from SharedData.Logger import Logger
from SharedData.IO.AWSS3 import S3DeleteFolder
from SharedData.TableIndex import TableIndex
from SharedData.SharedNumpy import SharedNumpy
from SharedData.IO.ClientSocket import ClientSocket
from SharedData.Table import Table

from SharedData.Utils import cpp


class TableDisk(Table):
    # TODO: create partitioning option yearly, monthly, daily

    def __init__(self, shareddata, database, period, source, tablename,
                 records=None, names=None, formats=None, size=None,hasindex=True,
                 overwrite=False, user='master', partitioning=None):
        self.type = 1
        self.shf_hdr = np.array([])
        self.shf_data = np.array([])
        super().__init__(shareddata, database, period, source, tablename,
                         records=records, names=names, formats=formats, size=size,hasindex=hasindex,
                         overwrite=overwrite, user=user, tabletype=self.type, partitioning=partitioning)

    ############### MALLOC ###############
    def malloc(self):     
        # create or extend currrent file
        self.create_file()
        
        # memory map header        
        self.shf_hdr = np.memmap(self.filepath,self.hdrdtype,'r+',0,(1,))
        self.shf_hdr[0] = self.hdr
        self.hdr = self.shf_hdr[0]
        self.hdr['recordssize'] = int(self.size)
        self.shf_hdr.flush()

        # memory map data
        offset = self.hdr.dtype.itemsize
        self.shf_data = np.memmap(self.filepath,self.recdtype,'r+',offset,(self.hdr['recordssize'],))
        self.records = SharedNumpy('DISK', self.shf_data)
        self.records.table = self
    
    ############### FREE ###############
    def free(self, acquire=True):        
        try:
            if acquire:
                self.acquire()
            # flush & free header
            if (not self.shf_hdr is None):
                if (len(self.shf_hdr)>0):
                    self.shf_hdr.flush()
            self.shf_hdr = None
            # flush & free data
            if (not self.shf_data is None):
                if (len(self.shf_data)>0):
                    self.shf_data.flush()
            self.shf_data = None
            # flush & free index
            if self.hasindex:
                self.index.free()
            if self.relpath in self.shareddata.data:
                del self.shareddata.data[self.relpath]            
        except Exception as e:
            Logger.log.error(f"TableDisk.free() {self.relpath}: {e}")
        finally:
            self.mutex['isloaded'] = 0
            if acquire:
                self.release()

    ############### WRITE ###############
    def write_file(self):
        # flush header
        self.shf_hdr.flush()
        # flush data
        self.shf_data.flush()
        # set the modify time of the file
        mtime = max(self.hdr['mtime'],
                    self.hdr['mtimehead'], self.hdr['mtimetail'])
        self.hdr['mtime'] = mtime
        os.utime(self.filepath, (mtime, mtime))
        # flush index
        if self.hdr['hasindex']==1:
            self.index.flush()

    ############### TRIM ###############
    def trim(self):        

        if self.hdr['recordssize'] > self.hdr['count']:
            if self.hdr['count']==0:
                self.hdr['recordssize'] = 2
            else:
                self.hdr['recordssize'] = self.hdr['count']
            self.hdr['isloaded'] = 0
            self.mutex['isloaded'] = 0
            self.hdr['isidxcreated'] = 0
            self.size = self.hdr['count']
            self.write_file()

            totalbytes = int(self.hdrdtype.itemsize
                    + self.recdtype.itemsize*self.size)

            self.filepathtmp = str(self.filepath)+'.tmp'
            if Path(self.filepathtmp).is_file():
                os.remove(self.filepathtmp)

            with open(self.filepathtmp, 'wb') as f:
                # Seek to the end of the file
                f.seek(totalbytes-1)
                # Write a single null byte to the end of the file
                f.write(b'\x00')
                if os.name == 'posix':
                    os.posix_fallocate(f.fileno(), 0, totalbytes)
                elif os.name == 'nt':
                    pass  # TODO: implement preallocation for windows in pyd
                
                f.seek(0)
                f.write(self.hdr.tobytes())
                f.write(self.records[:self.records.count].tobytes())
                f.flush()

            self.free()
            os.remove(self.filepath)
            os.rename(self.filepathtmp, self.filepath)
            tbl = self.shareddata.table(self.database, self.period, self.source, self.tablename)
            tbl.write()
            return tbl
        else:
            return self

    ############### RELOAD ###############
    def reload(self):
        try:
            self.acquire()
            self.free(acquire=False)
            self.download()
            self.malloc()
            if self.hasindex:
                self.hdr['isidxcreated'] = 0
                self.index.initialize()
            self.shareddata.data[self.relpath] = self
            self.hdr['isloaded'] = 1
            self.mutex['isloaded'] = 1
        except Exception as e:
            errmsg = f"TableDisk.reload() {self.relpath}: {e}"
            Logger.log.error(errmsg)
            raise Exception(errmsg)
        finally:
            self.release()
        
        return self.records
    
    ############### DELETE ###############
    def delete_local(self):
        if os.path.exists(self.filepath):
            os.remove(self.filepath)        
                
    def delete_remote(self):        
        s3_path = f"{self.database}/{self.period}/{self.source}/{self.tablename}"
        S3DeleteFolder(s3_path)
            
    def delete(self):
        try:
            self.acquire()
            self.delete_local()            
            self.delete_remote()
            self.free(acquire=False)
        except Exception as e:
            errmsg = f"TableDisk.delete() {self.relpath}: {e}"
            Logger.log.error(errmsg)
            raise Exception(errmsg)
        finally:
            self.release()