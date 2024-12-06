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
import traceback
import asyncio

from SharedData.Logger import Logger
from SharedData.IO.AWSS3 import S3Upload, S3Download, S3ListFolder, S3GetMtime
from SharedData.TableIndex import TableIndex
from SharedData.SharedNumpy import SharedNumpy
from SharedData.IO.ClientSocket import ClientSocket
from SharedData.IO.ClientWebSocket import ClientWebSocket
from SharedData.IO.ClientAPI import ClientAPI
from SharedData.Database import STRING_FIELDS


class Table:

    # TODO: create partitioning option yearly, monthly, daily
    def __init__(self, shareddata, database, period, source, tablename,
                 records=None, names=None, formats=None, size=None, hasindex=True,
                 overwrite=False, user='master', tabletype=1, partitioning=None):
        # tabletype 1: DISK, 2: MEMORY
        self.type = tabletype

        self.shareddata = shareddata
        self.user = user
        self.database = database
        self.period = period
        self.source = source
        self.tablename = tablename
        self.subscription_thread = None
        self.publish_thread = None

        self.names = names
        self.formats = formats
        self.size = size
        if not size is None:
            if size == 0:
                self.hasindex = False
        self.hasindex = hasindex
        self.overwrite = overwrite
        self.partitioning = partitioning
        # header
        self.hdr = None
        # records
        self.recnames = []
        self.recformats = []
        self.recdtype = None
        self.records = np.ndarray([])        
        # index
        self.index = TableIndex(self)
        
        errmsg = ''
        try:            
            
            self.init_schema()

            if not records is None:
                records = self.parse_records(records)

            if (not self.exists) | (self.overwrite):

                self.create_table(records)

            elif self.exists:

                self.load_table(records)

            # set the modify time of the file
            self.hdr['isloaded'] = 1
            self.mutex['isloaded'] = 1
            mtime = max(self.hdr['mtime'],self.hdr['mtimehead'], self.hdr['mtimetail'])
            self.hdr['mtime'] = mtime
            os.utime(self.filepath, (mtime, mtime))
            
        except Exception as e:
            tb = traceback.format_exc()
            errmsg = '%s error initializing\n %s\n%s!' % (
                self.relpath, str(tb), str(e))
            # errmsg = '%s error initalizing \n%s!' % (self.relpath,str(e))
            Logger.log.error(errmsg)
        finally:
            self.release()
            if errmsg != '':
                self.free()
                raise Exception(errmsg)
    
    def init_schema(self):
        self.header_changed = False
        # head header
        self._hdrnames = ['headersize', 'headerdescr', 'md5hashhead', 'md5hashtail',
                          'mtime', 'mtimehead', 'mtimetail',
                          'itemsize', 'recordssize', 'count',
                          'headsize', 'tailsize', 'minchgid',
                          'hastail', 'isloaded', 'hasindex', 'isidxcreated',
                          'descr']
        self._hdrformats = ['<i8', '|S250', '|S16', '|S16',
                            '<f8', '<f8', '<f8',
                            '<i8', '<i8', '<i8',
                            '<i8', '<i8', '<i8',
                            '<u1', '<u1', '<u1', '<u1',
                            '|SXXX']
        # tail header
        self._tailhdrnames = ['headersize', 'headerdescr',
                              'md5hash', 'mtime', 'tailsize']
        self._tailhdrformats = ['<i8', '|S80', '|S16', '<f8', '<i8']
    
        self.exists_remote = False
        self.exists_local = False
        
        # path        
        self.shm_name = f'{self.user}/{self.database}/{self.period}/{self.source}/table/{self.tablename}'
        self.relpath = str(self.shm_name.replace('/', '\\'))
        if os.name == 'posix':
            self.shm_name = self.shm_name.replace('/', '\\')

        # mutex
        self.pid = os.getpid()
        [self.shm_mutex, self.mutex, self.ismalloc] = \
            self.shareddata.mutex(self.shm_name, self.pid)
        if (self.mutex['type']==0): # type not initialized
            self.mutex['type'] = self.type

        elif self.mutex['type'] != self.type:
            if self.mutex['type'] == 1:
                errmsg = f'Table {self.relpath} is loaded as DISK!'
                Logger.log.error(errmsg)
                raise Exception(errmsg)
            elif self.mutex['type'] == 2:
                errmsg = f'Tabel {self.relpath} is loaded as MEMORY!'
                Logger.log.error(errmsg)
                raise Exception(errmsg)
            else:
                errmsg = f'Table {self.relpath} is loaded with unknown type!'
                Logger.log.error(errmsg)
                raise Exception(errmsg)        

        # schema
        self.database_folder = self.shareddata.dbfolders[0]
        self.schema = None
        if not self.shareddata.schema is None:
            errmsg=''
            try:
                self.shareddata.schema.table.acquire()
                buff = np.full((1,),np.nan,dtype=self.shareddata.schema.dtype)
                buff['symbol'] = self.shm_name.replace('\\', '/')
                loc = self.shareddata.schema.get_loc(buff,acquire=False)
                if loc[0] != -1: # table exists
                    self.schema = self.shareddata.schema[loc[0]]
                    folder_local = self.schema['folder_local']
                    self.database_folder = folder_local.decode('utf-8')
                else: # table does not exist
                    self.shareddata.schema.upsert(buff,acquire=False)
                    loc = self.shareddata.schema.get_loc(buff,acquire=False)
                    if loc[0] == -1: # check if table was added
                        errmsg = '%s error updating schema' % self.relpath
                        Logger.log.error(errmsg)
                        raise Exception(errmsg)
                    
                    self.schema = self.shareddata.schema[loc[0]]
                    self.database_folder = ''
                
                if (self.database_folder == '') | (self.database_folder == 'nan'):
                    # select the first disk with less percent_used
                    if len(self.shareddata.dbfolders) > 1:
                        # scan folders to check if table is already initialized
                        for f in self.shareddata.dbfolders:
                            tmppath = Path(f) / self.shm_name
                            tmppath = Path(str(tmppath).replace('\\', '/'))
                            tmppath = tmppath / 'data.bin'
                            if tmppath.is_file():
                                self.database_folder = f
                                break
                        
                        # if table not initialized get the disk with less percent_used
                        if (self.database_folder == '') | (self.database_folder == 'nan'):
                            dfdisks = self.shareddata.list_disks()
                            self.database_folder = dfdisks.index[0]
                    else:                    
                        self.database_folder = self.shareddata.dbfolders[0]

                    self.schema['folder_local'] = self.database_folder.encode('utf-8')
                    
            except Exception as e:
                errmsg = '%s error getting database folder\n%s!' % (self.relpath,str(e))
                Logger.log.error(errmsg)
            finally:
                self.shareddata.schema.table.release()
                if errmsg != '':
                    raise Exception(errmsg)
                            
        self.path = Path(self.database_folder)
        self.path = self.path / self.shm_name
        self.path = Path(str(self.path).replace('\\', '/'))
        os.makedirs(self.path, exist_ok=True)
        self.filepath = self.path / 'data.bin'
        self.headpath = self.path / 'head.bin'
        self.tailpath = self.path / 'tail.bin'

        self.exists_local = self.filepath.is_file()
        if self.exists_local:            
            self.exists = True
        else:                                
            self.exists = self.get_exists_remote()
                
    def get_exists_remote(self):
        searchpath = self.shm_name.replace('\\', '/').replace(self.user,'').lstrip('/')
        dftables = self.shareddata.list_all(searchpath, user=self.user)
        if not dftables.empty:
            # TODO: fill schema
            pass 
        return not dftables.empty    

    def parse_records(self, records):
        if (not records is None):                
            if isinstance(records, pd.DataFrame):
                records = self.df2records(records)
            descr = records.__array_interface__['descr']
            self.names = [item[0] for item in descr]
            self.formats = [item[1] for item in descr]
            if self.size is None:
                self.size = int(records.size)
        
        return records

    ############### CREATE ###############    
    def create_table(self, records):
        # create new table or overwrite existing table
        if (not self.names is None) \
            & (not self.formats is None)\
                & (not self.size is None):
            self.create_header()
            self.create_file()
            self.malloc()

        elif (not self.exists) | (self.overwrite):
            raise Exception('%s not found create first!' % (self.relpath))

        if not records is None:
            self.records.insert(records, acquire=False)

        if self.hasindex:
            self.index.initialize()
            if self.records.count>0:
                # check if index is coherent
                loc = self.records.get_loc(self.records[0:1], acquire=False)
                if loc[0]!=0: 
                    # index is not coherent
                    self.hdr['isidxcreated']=0
                    self.index.initialize()
                    loc = self.records.get_loc(self.records[0:1], acquire=False)
                    if loc[0]!=0:
                        raise Exception('Cannot create index!')

    def create_header(self):

        check_pkey = True
        npkeys = len(self.index.pkeycolumns)
        if len(self.names) >= npkeys:
            for k in range(npkeys):
                check_pkey = (check_pkey) & (
                    self.names[k] == self.index.pkeycolumns[k])
        else:
            check_pkey = False
        if not check_pkey:
            raise Exception('First columns must be %s!' %
                            (self.index.pkeycolumns))
        else:
            if 'date' in self.names:
                if self.formats[self.names.index('date')] != '<M8[ns]':
                    raise Exception('date must be <M8[ns]!')
            
            if self.hasindex:
                for field in STRING_FIELDS:
                    if field in self.names:
                        fielddtype = self.formats[self.names.index(field)]
                        if not '|S' in fielddtype:
                            raise Exception('symbol must be a string |S!')

            if not 'mtime' in self.names:
                self.names.insert(npkeys, 'mtime')
                self.formats.insert(npkeys, '<M8[ns]')
            elif self.formats[self.names.index('mtime')] != '<M8[ns]':
                raise Exception('mtime must be <M8[ns]!')
            
            if len(self.names) != len(self.formats):
                raise Exception('names and formats must have same length!')
            
            # malloc recarray
            self.recnames = self.names
            self.rectypes = self.formats
            self.recdtype = np.dtype(
                {'names': self.recnames, 'formats': self.rectypes})
            descr_str = ','.join(self.recnames)+';'+','.join(self.rectypes)
            descr_str_b = str.encode(
                descr_str, encoding='UTF-8', errors='ignore')
            len_descr = len(descr_str_b)

            # build header
            self.hdrnames = self._hdrnames
            hdrformats = self._hdrformats.copy()
            hdrformats[-1] = hdrformats[-1].replace('XXX', str(len_descr))
            self.hdrformats = hdrformats
            hdrnames = ','.join(self.hdrnames)
            hdrdtypes = ','.join(self.hdrformats)
            hdrdescr_str = hdrnames+';'+hdrdtypes
            hdrdescr_str_b = str.encode(
                hdrdescr_str, encoding='UTF-8', errors='ignore')

            self.hdrdtype = np.dtype(
                {'names': self.hdrnames, 'formats': self.hdrformats})
            self.hdr = np.recarray(shape=(1,), dtype=self.hdrdtype)[0]
            self.hdr['headersize'] = 250
            self.hdr['headerdescr'] = hdrdescr_str_b
            self.hdr['mtime'] = datetime.now().timestamp()
            self.hdr['mtimehead'] = self.hdr['mtime']
            self.hdr['mtimetail'] = self.hdr['mtime']
            self.hdr['count'] = 0
            self.hdr['minchgid'] = self.hdr['count']
            self.hdr['itemsize'] = int(self.recdtype.itemsize)
            self.hdr['recordssize'] = int(self.size)
            self.hdr['headsize'] = 0
            self.hdr['descr'] = descr_str_b
            self.hdr['isloaded'] = 0
            if self.hasindex:
                self.hdr['hasindex'] = 1
            else:
                self.hdr['hasindex'] = 0
            self.hdr['isloaded'] = 0
            self.hdr['isidxcreated'] = 0

    def create_file(self):
        totalbytes = int(self.hdrdtype.itemsize
                         + self.recdtype.itemsize*self.size)
        if not Path(self.filepath).is_file():
            os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
            with open(self.filepath, 'wb') as f:
                # Seek to the end of the file
                f.seek(totalbytes-1)
                # Write a single null byte to the end of the file
                f.write(b'\x00')
                if os.name == 'posix':
                    os.posix_fallocate(f.fileno(), 0, totalbytes)
                elif os.name == 'nt':
                    pass  # TODO: implement preallocation for windows in pyd
        elif (Path(self.filepath).stat().st_size < totalbytes):
            with open(self.filepath, 'ab') as f:
                # Seek to the end of the file
                f.seek(totalbytes-1)
                # Write a single null byte to the end of the file
                f.write(b'\x00')
                if os.name == 'posix':
                    os.posix_fallocate(f.fileno(), 0, totalbytes)
                elif os.name == 'nt':
                    pass  # TODO: implement preallocation for windows in pyd

    def copy_file(self):
        """
        Copies the file to a temporary file, writes a new header, and extends the file if needed.
        Then, it renames the temporary file to the original file name and deletes the original file.
        """
        if self.size is None:
            self.size = self.hdr['recordssize']
        totalbytes = int(self.hdrdtype.itemsize
                         + self.recdtype.itemsize*self.size)

        orig_size = int(self.orig_hdr.dtype.itemsize
                        + self.orig_hdr['recordssize']*self.orig_hdr['itemsize'])

        self.filepathtmp = str(self.filepath)+'.tmp'
        with open(self.filepath, 'rb') as f:
            with open(self.filepathtmp, 'wb') as ftmp:
                # write new header
                ftmp.seek(0)
                ftmp.write(self.hdr.tobytes())
                # copy data
                f.seek(self.orig_hdr.dtype.itemsize)
                bwritten = self.orig_hdr.dtype.itemsize
                message = 'Copying file :%iMB %s' % (
                    orig_size / (1024*1024), self.relpath)
                buffersize = int(1024**2*250)
                with tqdm(total=orig_size, unit='B', unit_scale=True, desc=message) as pbar:
                    while bwritten < orig_size:
                        nwrite = int(min(buffersize, orig_size-bwritten))
                        ftmp.write(f.read(nwrite))
                        pbar.update(nwrite)
                        bwritten += nwrite
                    # extend file if needed
                    if totalbytes > orig_size:
                        ftmp.write(b'\x00'*(totalbytes-orig_size))
                    ftmp.flush()

        # rename file        
        os.remove(self.filepath)        
        os.rename(self.filepathtmp, self.filepath)

    ############### DOWNLOAD ###############
    def download(self):
        head_io = None
        tail_io = None
        mtimetail = None

        tini = time.time()
        remote_path = str(self.headpath)+'.gzip'
        if not self.hdr is None:
            mtimetail = self.hdr['mtimetail']
            [head_io_gzip, head_local_mtime, head_remote_mtime] = \
                S3Download(remote_path, local_mtime=self.hdr['mtimehead']
                        ,database_folder=self.database_folder)            
        else:
            [head_io_gzip, head_local_mtime, head_remote_mtime] = \
                S3Download(remote_path,database_folder=self.database_folder)

        if not head_io_gzip is None:
            # remote file is newer than local
            # unzip head and read
            te = time.time()-tini+0.000001
            datasize = head_io_gzip.getbuffer().nbytes/1000000
            Logger.log.debug('download head %s %.2fMB in %.2fs %.2fMBps ' %
                             (self.relpath, datasize, te, datasize/te))
            head_io_gzip.seek(0)
            head_io = gzip.GzipFile(fileobj=head_io_gzip, mode='rb')
            self.read_header(head_io)
            self.hdr['mtimehead'] = head_remote_mtime # update the head mtime            
            mtimetail = self.hdr['mtimetail'] - 1  # force tail download

        if self.hdr['hastail'] == 1:
            remote_path = str(self.tailpath)+'.gzip'
            [tail_io_gzip, tail_local_mtime, tail_remote_mtime] = \
                S3Download(remote_path, local_mtime=mtimetail,
                           database_folder=self.database_folder)
            if not tail_io_gzip is None:
                tail_io_gzip.seek(0)
                tail_io = gzip.GzipFile(fileobj=tail_io_gzip, mode='rb')
                self.read_tailheader(tail_io)
                self.hdr['mtimetail'] = tail_remote_mtime # update the tail mtime

        self.create_file()

        if not head_io is None:
            self.read_head(head_io)
            self.hdr['isloaded'] = 0
            self.hdr['isidxcreated'] = 0

        if not tail_io is None:
            self.read_tail(tail_io)
            self.hdr['isloaded'] = 0
            self.hdr['isidxcreated'] = 0

    ############### READ ###############
    def load_table(self, records):
        # open existing table
        if self.exists_local:
            with open(self.filepath, 'rb') as io_obj:
                self.read_header(io_obj)

        if ((self.mutex['isloaded']==0) | (not self.exists_local)):
            self.download()

        self.malloc()

        if self.hasindex:
            self.index.initialize()
            if self.records.count>0:
                # check if index is coherent
                loc = self.records.get_loc(self.records[0:1], acquire=False)
                if loc[0]!=0: 
                    # index is not coherent
                    self.hdr['isidxcreated']=0
                    self.index.initialize()
                    loc = self.records.get_loc(self.records[0:1], acquire=False)
                    if loc[0]!=0:
                        raise Exception('Cannot create index!')
                    
        if not records is None:
            self.records.upsert(records, acquire=False)

    def read_header(self, io_obj):
        io_obj.seek(0)
        # load header dtype
        nbhdrdescr = int.from_bytes(io_obj.read(8), byteorder='little')
        if nbhdrdescr == 0:
            raise Exception('Empty header description!')
        hdrdescr_b = io_obj.read(nbhdrdescr)
        hdrdescr = hdrdescr_b.decode(encoding='UTF-8', errors='ignore')
        hdrdescr = hdrdescr.replace('\x00', '')
        self.hdrnames = hdrdescr.split(';')[0].split(',')
        self.hdrformats = hdrdescr.split(';')[1].split(',')
        self.hdrdtype = np.dtype(
            {'names': self.hdrnames, 'formats': self.hdrformats})
        # read header
        io_obj.seek(0)
        self.hdr = np.ndarray((1,), dtype=self.hdrdtype,
                              buffer=io_obj.read(self.hdrdtype.itemsize))[0]
        self.hdr = self.hdr.copy()
        # load data dtype
        descr = self.hdr['descr'].decode(encoding='UTF-8', errors='ignore')
        self.recnames = descr.split(';')[0].split(',')
        self.recformats = descr.split(';')[1].split(',')
        if 'hasindex' in self.hdrnames:
            if self.hdr['hasindex']==1:
                for field in STRING_FIELDS:
                    if field in self.recnames:
                        fielddtype = self.recformats[self.recnames.index(field)]
                        # check if field is a string
                        if not (('S' in fielddtype) or ('|S' in fielddtype)):
                            warnmsg = f'{field} is not a string in {self.relpath}!'
                            Logger.log.warning(warnmsg)
                            self.hdr['hasindex']=0

        self.recdtype = np.dtype(
            {'names': self.recnames, 'formats': self.recformats})

        if self.hdr['count'] > self.hdr['recordssize']:
            self.hdr['recordssize'] = self.hdr['count']

        if self.size is None:
            self.size = self.hdr['recordssize']
        elif self.size < self.hdr['recordssize']:
            self.size = self.hdr['recordssize']                

        if self.hdrnames == self._hdrnames:            
            self.hasindex = self.hdr['hasindex']==1
            self.orig_hdr = self.hdr
        else:
            # convert header
            self.header_changed = True
            self.orig_hdr = self.hdr.copy()

            self.hdrnames = self._hdrnames
            len_descr = len(self.hdr['descr'])
            hdrformats = self._hdrformats.copy()
            hdrformats[-1] = hdrformats[-1].replace('XXX', str(len_descr))
            self.hdrformats = hdrformats
            hdrnames = ','.join(self.hdrnames)
            hdrdtypes = ','.join(self.hdrformats)
            hdrdescr_str = hdrnames+';'+hdrdtypes
            hdrdescr_str_b = str.encode(
                hdrdescr_str, encoding='UTF-8', errors='ignore')
            self.hdrdtype = np.dtype(
                {'names': self.hdrnames, 'formats': self.hdrformats})
            self.hdr = np.ndarray((1,), dtype=self.hdrdtype)[0]
            for name in self.orig_hdr.dtype.names:
                if name in self.hdr.dtype.names:
                    self.hdr[name] = self.orig_hdr[name]
            self.hdr['headerdescr'] = hdrdescr_str_b
            if not 'mtimehead' in self.orig_hdr.dtype.names:
                self.hdr['mtimehead'] = self.hdr['mtime']
            if not 'mtimetail' in self.orig_hdr.dtype.names:
                self.hdr['mtimetail'] = self.hdr['mtime']            
            
            if 'hasindex' in self.orig_hdr.dtype.names:
                self.hasindex = self.orig_hdr['hasindex']==1
                self.hdr['hasindex'] = self.orig_hdr['hasindex']
            else:                
                if self.hasindex:
                    self.hdr['hasindex'] = 1
                else:
                    self.hdr['hasindex'] = 0

            self.hdr['isloaded'] = 0
            self.hdr['isidxcreated'] = 0

            if self.exists_local:
                if isinstance(io_obj, io.BufferedReader):                    
                    io_obj.close()
                self.copy_file()

    def read_tailheader(self, tail_io):
        tail_io.seek(0)
        tailnbhdrdescr = int.from_bytes(tail_io.read(8), byteorder='little')
        tailhdrdescr_b = tail_io.read(tailnbhdrdescr)
        tailhdrdescr = tailhdrdescr_b.decode(encoding='UTF-8', errors='ignore')
        tailhdrdescr = tailhdrdescr.replace('\x00', '')
        self.tailhdrnames = tailhdrdescr.split(';')[0].split(',')
        self.tailhdrformats = tailhdrdescr.split(';')[1].split(',')
        self.tailhdrdtype = np.dtype(
            {'names': self.tailhdrnames, 'formats': self.tailhdrformats})

        nbtailhdr = self.tailhdrdtype.itemsize
        tail_io.seek(0)
        tailheader_buf = tail_io.read(nbtailhdr)
        self.tailhdr = np.ndarray((1,),
                                  dtype=self.tailhdrdtype, buffer=tailheader_buf)[0]
        self.tailhdr = self.tailhdr.copy()
        self.tailhdr['headersize'] = tailnbhdrdescr
        # update header
        self.hdr['md5hashtail'] = self.tailhdr['md5hash']
        self.hdr['mtimetail'] = self.tailhdr['mtime']
        self.hdr['tailsize'] = self.tailhdr['tailsize']
        self.hdr['count'] = self.hdr['headsize']+self.tailhdr['tailsize']

    def read_head(self, head_io):
        buffer_size = 250 * 1024 * 1024  # 250 MB buffer size
        head_io.seek(0)
        with open(self.filepath, 'rb+') as f:
            # write header
            f.seek(0)
            f.write(self.hdr.tobytes())
            # seek start of head data
            head_io.seek(self.orig_hdr.dtype.itemsize)
            # read head data
            nb_head = (self.hdr['headsize']*self.hdr['itemsize'])
            message = 'Unzipping:%iMB %s' % (
                nb_head / (1024*1024), self.relpath)
            with tqdm(total=nb_head, unit='B', unit_scale=True, desc=message) as pbar:
                while True:
                    buffer = head_io.read(buffer_size)
                    if not buffer:
                        break
                    f.write(buffer)
                    pbar.update(len(buffer))
            f.flush()

    def read_tail(self, tail_io):
        tail_io.seek(0)
        nbhdr = self.hdr.dtype.itemsize
        nbhead = self.hdr['headsize']*self.hdr['itemsize']
        with open(self.filepath, 'rb+') as f:
            f.seek(nbhdr+nbhead)
            tail_io.seek(self.tailhdr.dtype.itemsize)
            f.write(tail_io.read())
            f.flush()

    def compare_hash(self, h1, h2):
        l1 = len(h1)
        l2 = len(h2)
        l = min(l1, l2)
        return h1[:l] == h2[:l]

    ############### WRITE ###############
    def write(self, force_write=False):
        errmsg = ''
        try:
            self.acquire()

            tini = time.time()
            # create header
            mtime = self.hdr['mtime']
            write_head = False            
            write_head = self.fill_header(force_write)                

            thread_s3 = threading.Thread(
                target=self.upload, args=(write_head, mtime, force_write))
            thread_s3.start()

            thread_flush = threading.Thread(target=self.write_file)
            thread_flush.start()

            # join threads
            thread_s3.join()
            thread_flush.join()

            te = time.time() - tini
            datasize = self.hdr['count'] * self.hdr['itemsize'] / 1000000
            Logger.log.debug('write %s %.2fMB in %.2fs %.2fMBps ' %
                             (self.relpath, datasize, te, datasize / te))
        except Exception as e:
            errmsg = 'Could not write %s\n%s!' % (self.relpath, e)
            Logger.log.error(errmsg)
        finally:
            self.release()
            if errmsg != '':
                raise Exception(errmsg)

    def partition_head_tail(self):
        
        if not 'date' in self.records.dtype.names:
            tailsize = 0
            headsize = self.hdr['count']
            self.hdr['hastail'] = 0
        else:
            # partition data by current year
            partdate = pd.Timestamp(datetime(datetime.now().year, 1, 1))        
            idx = self.records['date'] >= partdate
            if np.any(idx):  # there is data for the current year
                if np.all(idx):  # all data for the current year
                    headsize = self.hdr['count']
                    tailsize = 0
                    self.hdr['hastail'] = 0
                else:  # some data for the current year
                    partid = np.where(idx)[0][0]
                    headsize = partid
                    tailsize = self.hdr['count'] - partid
                    self.hdr['hastail'] = 1
            else:  # there is not data for the current year
                tailsize = 0
                headsize = self.hdr['count']
                self.hdr['hastail'] = 0

        headsize_chg = (headsize != self.hdr['headsize'])
        self.hdr['headsize'] = headsize        
        self.hdr['tailsize'] = tailsize

        head_modified = (self.hdr['minchgid'] <= self.hdr['headsize'])
        self.hdr['minchgid'] = self.hdr['count']+1 # reset the minchgid
        
        write_head = (head_modified) | (headsize_chg) 
        
        self.hdr['mtimetail'] = self.hdr['mtime']
        if write_head:
            self.hdr['mtimehead'] = self.hdr['mtime']

        return write_head, headsize, tailsize

    def fill_header(self, force_write=False):

        write_head, headsize, tailsize = self.partition_head_tail()

        nb_header = int(self.hdrdtype.itemsize)
        nb_head = int(self.hdr['headsize']*self.hdr['itemsize'])
        nb_tail = int(tailsize*self.hdr['itemsize'])

        self.tailhdrdtype = np.dtype(
            {'names': self._tailhdrnames, 'formats': self._tailhdrformats})
        self.tailhdr = np.recarray(shape=(1,), dtype=self.tailhdrdtype)[0]
        self.tailhdr['headersize'] = 80
        _headerdescr = ','.join(self._tailhdrnames) + \
            ';'+','.join(self._tailhdrformats)
        _headerdescr_b = str.encode(
            _headerdescr, encoding='UTF-8', errors='ignore')
        self.tailhdr['headerdescr'] = _headerdescr_b
        self.tailhdr['mtime'] = self.hdr['mtime']
        self.tailhdr['tailsize'] = tailsize

        if (write_head) | (force_write):
            self.hdr['md5hashhead'] = 0  # reset the hash value
            nb_records_mb = (nb_header+nb_head)/(1024*1024)
            if nb_records_mb <= 100:
                m = hashlib.md5(self.records[0:self.hdr['headsize']].tobytes())
            else:
                message = 'Creating md5 hash:%iMB %s' % (
                    nb_records_mb, self.relpath)
                block_size = 100 * 1024 * 1024  # or any other block size that you prefer
                chunklines = int(block_size/self.hdr['itemsize'])
                total_lines = self.hdr['headsize']
                read_lines = 0
                nb_total = self.hdr['headsize']*self.hdr['itemsize']
                m = hashlib.md5()
                # Use a with block to manage the progress bar
                with tqdm(total=nb_total, unit='B', unit_scale=True, desc=message) as pbar:
                    # Loop until we have read all the data
                    while read_lines < total_lines:
                        # Read a block of data
                        chunk_size = min(chunklines, total_lines-read_lines)
                        # Update the shared memory buffer with the newly read data
                        m.update(
                            self.records[read_lines:read_lines+chunk_size].tobytes())
                        read_lines += chunk_size  # update the total number of bytes read so far
                        # Update the progress bar
                        pbar.update(chunk_size*self.hdr['itemsize'])
            self.hdr['md5hashhead'] = m.digest()

        if self.hdr['hastail'] == 1:
            self.tailhdr['md5hash'] = 0  # reset the hash value
            self.hdr['md5hashtail'] = 0  # reset the hash value
            nb_records_mb = (nb_tail)/(1024*1024)
            startbyte = nb_header+nb_head
            if nb_records_mb <= 100:
                m = hashlib.md5(
                    self.records[self.hdr['headsize']:self.hdr['count']].tobytes())
            else:
                message = 'Creating md5 hash:%iMB %s' % (
                    nb_records_mb, self.relpath)
                block_size = 100 * 1024 * 1024  # or any other block size that you prefer
                chunklines = int(block_size/self.hdr['itemsize'])
                total_lines = self.tailhdr['tailsize']
                read_lines = 0
                tailstart = self.hdr['headsize']
                nb_total = self.tailhdr['tailsize']*self.hdr['itemsize']
                m = hashlib.md5()
                # Use a with block to manage the progress bar
                with tqdm(total=nb_total, unit='B', unit_scale=True, desc=message) as pbar:
                    # Loop until we have read all the data
                    while read_lines < total_lines:
                        # Read a block of data
                        chunk_size = min(chunklines, total_lines-read_lines)
                        # Update the shared memory buffer with the newly read data
                        m.update(
                            self.records[tailstart+read_lines:tailstart+read_lines+chunk_size].tobytes())
                        read_lines += chunk_size  # update the total number of bytes read so far
                        # Update the progress bar
                        pbar.update(chunk_size*self.hdr['itemsize'])

            self.tailhdr['md5hash'] = m.digest()
            self.hdr['md5hashtail'] = self.tailhdr['md5hash']

        return write_head

    ############### UPLOAD ###############
    def upload(self, write_head, mtime, force_write=False):        
        remote_head_mtime = S3GetMtime(str(self.headpath)+'.gzip')
        remote_head_is_updated = False
        if not remote_head_mtime is None:
            remote_head_is_updated = remote_head_mtime >= self.hdr['mtimehead']

        if (write_head) | (not remote_head_is_updated) | (force_write):
            self.upload_head(mtime)

        if self.hdr['hastail'] == 1:
            remote_tail_mtime = S3GetMtime(str(self.tailpath)+'.gzip')
            remote_tail_is_updated = False
            if not remote_tail_mtime is None:
                remote_tail_is_updated = remote_tail_mtime >= self.hdr['mtimetail']
            if not remote_tail_is_updated:
                self.upload_tail(mtime)

    def upload_head(self, mtime):
        # zip head        
        gzip_io = io.BytesIO()
        with gzip.GzipFile(fileobj=gzip_io, mode='wb', compresslevel=1) as gz:
            gz.write(self.hdr.tobytes())
            headsize_mb = (self.hdr['headsize'] *
                           self.hdr['itemsize']) / (1024*1024)
            blocksize = 1024*1024*100
            chunklines = int(blocksize/self.hdr['itemsize'])
            descr = 'Zipping:%iMB %s' % (headsize_mb, self.relpath)
            with tqdm(total=headsize_mb, unit='B', unit_scale=True, desc=descr) as pbar:
                written = 0
                while written < self.hdr['headsize']:
                    # write in chunks of max 100 MB size
                    chunk_size = min(chunklines, self.hdr['headsize']-written)
                    gz.write(
                        self.records[written:written+chunk_size].tobytes())
                    written += chunk_size
                    pbar.update(chunk_size*self.hdr['itemsize'])
        S3Upload(gzip_io, str(self.headpath)+'.gzip', mtime,
                 database_folder=self.database_folder)

    def upload_tail(self, mtime):
        gzip_io = io.BytesIO()
        with gzip.GzipFile(fileobj=gzip_io, mode='wb', compresslevel=1) as gz:
            gz.write(self.tailhdr.tobytes())
            gz.write(self.records[self.hdr['headsize']
                     :self.hdr['count']].tobytes())
        S3Upload(gzip_io, str(self.tailpath)+'.gzip', mtime,
                 database_folder=self.database_folder)

    ############### CONVERT ###############
    def records2df(self, records):
        df = pd.DataFrame(records, copy=False)
        dtypes = df.dtypes.reset_index()
        dtypes.columns = ['tag', 'dtype']
        # convert object to string
        string_idx = pd.Index(['|S' in str(dt) for dt in dtypes['dtype']])
        string_idx = (string_idx) | pd.Index(dtypes['dtype'] == 'object')
        tags_obj = dtypes['tag'][string_idx].values
        for tag in tags_obj:
            try:
                df[tag] = df[tag].str.decode(encoding='utf-8', errors='ignore')
            except:
                pass
        df = df.set_index(self.index.pkeycolumns)
        return df

    def df2records(self, df):
        check_pkey = True
        if len(self.index.pkeycolumns) == len(df.index.names):
            for k in range(len(self.index.pkeycolumns)):
                check_pkey = (check_pkey) & (
                    df.index.names[k] == self.index.pkeycolumns[k])
        else:
            check_pkey = False
        if not check_pkey:
            raise Exception('First columns must be %s!' %
                            (self.index.pkeycolumns))
        else:
            if self.recdtype is None:
                df = df.reset_index()
                dtypes = df.dtypes.reset_index()
                dtypes.columns = ['tag', 'dtype']
            
                # Convert datetime columns with timezone to UTC naive datetime
                for col in df.columns:
                    if pd.api.types.is_datetime64_any_dtype(df[col]):
                        if df[col].dt.tz is not None:
                            df[col] = df[col].dt.tz_convert('UTC').dt.tz_localize(None)
                
                # convert object to string
                tags_obj = dtypes['tag'][dtypes['dtype'] == 'object'].values
                for tag in tags_obj:
                    try:
                        df[tag] = df[tag].astype(str)
                        df[tag] = df[tag].str.encode(encoding='utf-8', errors='ignore')
                    except Exception as e:
                        Logger.log.error(f'df2records(): Could not convert {tag} : {e}!')
                    df[tag] = df[tag].astype('|S')
                    
                rec = np.ascontiguousarray(df.to_records(index=False))
                type_descriptors = [field[1] for field in rec]
                if '|O' in type_descriptors:
                    errmsg = 'df2records(): Could not convert type to binary'
                    Logger.log.error(errmsg)
                    raise Exception(errmsg)
                        
                return rec
            else:
                df = df.reset_index()
                # Convert datetime columns with timezone to UTC naive datetime
                for col in df.columns:
                    if pd.api.types.is_datetime64_any_dtype(df[col]):
                        if df[col].dt.tz is not None:
                            df[col] = df[col].dt.tz_convert('UTC').dt.tz_localize(None)
                
                dtypes = self.recdtype
                
                rec = np.full((df.shape[0],), fill_value=np.nan, dtype=dtypes)
                for col in dtypes.names:
                    try:
                        if col in df.columns:
                            rec[col] = df[col].astype(dtypes[col])
                    except Exception as e:
                        Logger.log.error('df2records(): Could not convert %s!\n%s' % (col, e))

                return rec

    ############### LOCK ###############
    def acquire(self):
        self.shareddata.acquire(self.mutex, self.pid, self.relpath)

    def release(self):
        self.shareddata.release(self.mutex, self.pid, self.relpath)

    ############### SUBSCRIBE ###############

    def subscribe(self, host, port, lookbacklines=1000, 
                  lookbackdate=None, method='websocket', snapshot=False, bandwidth=1e6, protocol='http'):
        if self.subscription_thread is None:
            if method == 'socket':
                self.subscription_thread = threading.Thread(
                    target=ClientSocket.table_subscribe_thread,
                    args=(self, host, port, lookbacklines, lookbackdate, snapshot, bandwidth),
                )
                self.subscription_thread.start()
                Logger.log.info('Socket to %s:%s -> %s started...' % (host,str(port),self.relpath))
            elif method == 'websocket':
                def websocket_thread():
                    asyncio.run(ClientWebSocket.table_subscribe_thread(
                        self, host, port, lookbacklines, lookbackdate, snapshot, bandwidth))
                
                self.subscription_thread = threading.Thread(
                    target=websocket_thread,                    
                )
                self.subscription_thread.start()                    
                Logger.log.info('Websocket to %s:%s -> %s started...' % (host,str(port),self.relpath))
            elif method == 'api':
                self.subscription_thread = threading.Thread(
                    target=ClientAPI.table_subscribe_thread,
                    args=(self, host, port, lookbacklines, lookbackdate, snapshot, bandwidth, protocol),
                )
                self.subscription_thread.start()
                Logger.log.info('API to %s:%s -> %s started...' % (host,str(port),self.relpath))
            else:
                Logger.log.error('Invalid method %s to %s:%s -> %s !!!' % (method,host,str(port),self.relpath))
        else:
            Logger.log.error('Subscription to %s:%s -> %s already running!' % (host,str(port),self.relpath))

    def publish(self, host, port=None, lookbacklines=1000, 
                  lookbackdate=None, method='websocket', snapshot=False, bandwidth=1e6, protocol='http'):
        if self.publish_thread is None:
            if method == 'socket':
                self.publish_thread = threading.Thread(
                    target=ClientSocket.table_publish_thread,
                    args=(self, host, port, lookbacklines, lookbackdate, snapshot,bandwidth),
                )
                self.publish_thread.start()
                Logger.log.info('Socket to %s:%s -> %s started...' % (host,str(port),self.relpath))
            elif method == 'websocket':
                def websocket_thread():
                    asyncio.run(ClientWebSocket.table_publish_thread(
                        self, host, port, lookbacklines, lookbackdate, snapshot, bandwidth))
                
                self.publish_thread = threading.Thread(
                    target=websocket_thread,                    
                )
                self.publish_thread.start()                    
                Logger.log.info('Websocket to %s:%s -> %s started...' % (host,str(port),self.relpath))
            elif method == 'api':
                self.publish_thread = threading.Thread(
                    target=ClientAPI.table_publish_thread,
                    args=(self, host, port, lookbacklines, lookbackdate, snapshot,bandwidth, protocol),
                )
                self.publish_thread.start()
                Logger.log.info('API to %s:%s -> %s started...' % (host,str(port),self.relpath))
            else:
                Logger.log.error('Invalid method %s to %s:%s -> %s !!!' % (method,host,str(port),self.relpath))
        else:
            Logger.log.error('Subscription to %s:%s -> %s already running!' % (host,str(port),self.relpath))
