import os
from dotenv import load_dotenv
from pathlib import Path
import pandas as pd
import numpy as np
import time
import subprocess
from datetime import datetime, timedelta
import gzip
import io
import shutil
import hashlib


import SharedData.Defaults as Defaults
from SharedData.Logger import Logger
from SharedData.IO.AWSS3 import S3Upload, S3ListFolder, S3Download, UpdateModTime, S3DeleteFolder

# TODO: CREATE CSV MODE
class Metadata():

    def __init__(self, name, mode='rw', user='master'):

        self.user = user

        self.s3read = False
        self.s3write = False
        if mode == 'r':
            self.s3read = True
            self.s3write = False
        elif mode == 'w':
            self.s3read = False
            self.s3write = True
        elif mode == 'rw':
            self.s3read = True
            self.s3write = True

        self.mode = mode
        self.save_local = True
        if os.environ['SAVE_LOCAL'] != 'True':
            self.save_local = False

        self.name = name

        self._records = np.array([])
        self.records_chg = False

        self._index_columns = np.array([])
        self._static = pd.DataFrame([])
        self.static_chg = False

        self.load()

    @property
    def static(self):
        if self.records_chg:
            self.records_chg = False
            self._static = self.records2df(self._records)
        self.static_chg = True
        return self._static

    @static.setter
    def static(self, df):
        self.static_chg = True
        self.records_chg = False
        self._index_columns = np.array(df.index.names)
        self._static = df

    @property
    def records(self):
        if self.static_chg:
            self.static_chg = False
            self._records = self.df2records(self._static)
        self.records_chg = True
        return self._records

    @records.setter
    def records(self, value):
        self.records_chg = True
        self._records = value

    def hasindex(self):
        if self._index_columns.size > 0:
            if not self._index_columns[0] is None:
                if self._index_columns[0] != '':
                    return True
        return False

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
        if self.hasindex():
            df = df.set_index(self._index_columns.tolist())
        return df

    def df2records(self, df):
        self._index_columns = np.array(df.index.names)
        if self.hasindex():
            df = df.reset_index().copy()
        else:
            df = df.copy()
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

    def __setitem__(self, tag, value):
        self.static_chg = True
        self.static[tag] = value

    def __getitem__(self, tag):
        return self.static[tag]

    @staticmethod
    def list(keyword, user='master'):
        mdprefix = user+'/Metadata/'
        keys = S3ListFolder(mdprefix+keyword)
        keys = keys[['.bin' in k for k in keys]]
        keys = [k.replace(mdprefix, '').split('.')[0] for k in keys]
        return keys

    # READ
    def load(self):
        t = time.time()
        self.fpath = Path(os.environ['DATABASE_FOLDER']) / self.user
        self.pathxls = self.fpath / ('Metadata/'+self.name+'.xlsx')
        self.path = self.fpath / ('Metadata/'+self.name+'.bin')

        if not self.path.parent.exists():
            if self.save_local:
                self.path.parent.mkdir(parents=True, exist_ok=True)

        md_io_gzip = None
        if (self.s3read):
            # update bin before comparing dates
            force_download = (not self.save_local)
            [md_io_gzip, local_mtime, remote_mtime] = \
                S3Download(str(self.path)+'.gzip', str(self.path), force_download)

        readbin = True
        readxlsx = False
        if self.save_local:
            # prefer read bin
            # but read excel if newer

            readbin = self.path.is_file()
            readxlsx = self.pathxls.is_file()
            if (readbin) & (readxlsx):
                readxlsx = os.path.getmtime(
                    self.pathxls) > os.path.getmtime(self.path)
                readbin = not readxlsx

        if (not readxlsx) | (not self.save_local):
            # read bin
            md_io = None
            if (not md_io_gzip is None):
                md_io = io.BytesIO()
                md_io_gzip.seek(0)
                with gzip.GzipFile(fileobj=md_io_gzip, mode='rb') as gz:
                    shutil.copyfileobj(gz, md_io)
                self.read_metadata_io(md_io)
                if (self.save_local):
                    # save local
                    Metadata.write_file(md_io, self.path, remote_mtime)
                    UpdateModTime(self.path, remote_mtime)

            if (md_io is None) & (self.path.is_file()):
                with open(str(self.path), 'rb') as md_io:
                    self.read_metadata_io(md_io)

        elif readxlsx:
            tini = time.time()

            xls = pd.read_excel(self.pathxls, sheet_name=None)
            if 'static' in xls:
                self.static = xls['static']

            if not self.static.empty:
                self.static = self.static.set_index(self.static.columns[0])

            if os.environ['LOG_LEVEL'] == 'DEBUG':
                Logger.log.debug('Loading metadata xlsx %s %.2f done!' % (
                    self.name, time.time()-tini))

        if os.environ['LOG_LEVEL'] == 'DEBUG':
            Logger.log.debug('Initializing Metadata %s,%s DONE!' %
                             (self.name, self.mode))

    def read_metadata_io(self, bin_io):
        bin_io.seek(0)
        header = np.frombuffer(bin_io.read(32), dtype=np.int64)
        descr_str_b = bin_io.read(int(header[0]))
        data = bin_io.read(int(header[3]))
        md5hash_b = bin_io.read(16)

        m = hashlib.md5(descr_str_b)
        m.update(data)
        _md5hash_b = m.digest()
        #TODO: CHANGE THE COMPARE METHOD!
        if not md5hash_b == _md5hash_b:
            raise Exception('Metadata file corrupted!\n%s' % (self.path))

        descr_str = descr_str_b.decode(encoding='UTF-8', errors='ignore')
        descr = descr_str.split(';')
        names = descr[0].split(',')
        formats = descr[1].split(',')
        self._index_columns = np.array(descr[2].split(','))
        dtype = np.dtype({'names': names, 'formats': formats})
        self.records = np.ndarray((header[2],), dtype=dtype, buffer=data)

    # WRITE
    def save(self, save_excel=False):
        fpath = Path(os.environ['DATABASE_FOLDER']) / self.user
        self.pathxls = fpath / ('Metadata/'+self.name+'.xlsx')
        self.path = fpath / ('Metadata/'+self.name+'.bin')

        tini = time.time()
        mtime = datetime.now().timestamp()
        if not os.path.isdir(self.path.parents[0]):
            os.makedirs(self.path.parents[0])
        # save excel first so that last modified
        # timestamp is older
        if save_excel:
            with open(self.pathxls, 'wb') as f:
                writer = pd.ExcelWriter(f, engine='xlsxwriter')
                if self.hasindex():
                    self.static.to_excel(
                        writer, sheet_name='static', index=True)
                else:
                    self.static.to_excel(
                        writer, sheet_name='static', index=False)
                writer.close()
                f.flush()
            os.utime(self.pathxls, (mtime, mtime))

        io_obj = None
        if self.save_local:
            io_obj = self.create_metadata_io()
            Metadata.write_file(io_obj, self.path, mtime)

        if self.s3write:
            if io_obj is None:
                io_obj = self.create_metadata_io()
            io_obj.seek(0)
            gzip_io = io.BytesIO()
            with gzip.GzipFile(fileobj=gzip_io, mode='wb', compresslevel=1) as gz:
                shutil.copyfileobj(io_obj, gz)
            S3Upload(gzip_io, str(self.path)+'.gzip', mtime)

        if os.environ['LOG_LEVEL'] == 'DEBUG':
            Logger.log.debug('Saving metadata ' + self.name +
                             ' %.2f done!' % (time.time()-tini))

    def create_metadata_io(self):
        data = self.records
        descr = data.__array_interface__['descr']
        names = ','.join([item[0] for item in descr])
        dt = ','.join([item[1] for item in descr])
        if self.hasindex():
            index = ','.join([col for col in self._index_columns])
            descr_str = names+';'+dt+';'+index
        else:
            descr_str = names+';'+dt+';'
        descr_str_b = str.encode(descr_str, encoding='UTF-8', errors='ignore')
        header = [len(descr_str_b), data.itemsize,
                  data.size, data.itemsize*data.size]
        header = np.array(header).astype(np.int64)
        m = hashlib.md5(descr_str_b)
        m.update(data)
        md5hash_b = m.digest()
        io_obj = io.BytesIO()
        io_obj.write(header)
        io_obj.write(descr_str_b)
        io_obj.write(data)
        io_obj.write(md5hash_b)
        return io_obj

    @staticmethod
    def write_file(io_obj, path, mtime):
        with open(path, 'wb') as f:
            f.write(io_obj.getbuffer())
            f.flush()
        os.utime(path, (mtime, mtime))


    @staticmethod
    def delete(name, user='master'):
        try:            
            fpath = Path(os.environ['DATABASE_FOLDER']) / user
            pathxls = fpath / ('Metadata/'+name+'.xlsx')
            if pathxls.exists():
                os.remove(pathxls)
            path = fpath / ('Metadata/'+name+'.bin')
            if path.exists():
                os.remove(path)
            s3path = str(path)+'.gzip'
            s3path = s3path.replace(os.environ['DATABASE_FOLDER'],'')
            s3path = s3path.replace('\\','/')
            s3path = s3path.lstrip('/')
            S3DeleteFolder(s3path)
            return True
        except Exception as e:
            Logger.log.error(f'Delete {path} Error: {e}')
            return False

    # UTILS
    def mergeUpdate(self, newdf):
        for i in range(len(newdf.index.names)):
            idxname = newdf.index.names[i]
            if idxname == None:
                Logger.log.error(
                    '%s metadata mergeUpdate newdf index is None!' % self.name)
                raise Exception(
                    '%s metadata mergeUpdate newdf index is None!' % self.name)
            elif idxname != self.static.index.names[i]:
                Logger.log.error(
                    '%s metadata mergeUpdate newdf index does not match!' % self.name)
                raise Exception(
                    '%s metadata mergeUpdate newdf index does not match!' % self.name)

        newidx = ~newdf.index.isin(self.static.index)
        if newidx.any():
            self.static = self.static.reindex(
                index=self.static.index.union(newdf.index))

        newcolsidx = ~newdf.columns.isin(self.static.columns)
        if newcolsidx.any():
            newcols = newdf.columns[newcolsidx]
            self.static = pd.concat([self.static, newdf[newcols]], axis=1)

        self.static.update(newdf)
        self.static_chg = True


def isnan(value):
    if isinstance(value, str):
        return ((value == 'nan') | (value == ''))
    elif isinstance(value, float):
        return np.isnan(value)