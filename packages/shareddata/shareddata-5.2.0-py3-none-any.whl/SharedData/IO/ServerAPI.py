from flask import Flask, Response
from flask import request
from flask import jsonify
from flasgger import Swagger, swag_from

import os
import datetime
import gzip
import json
import time
import lz4.frame as lz4f
import pandas as pd
import numpy as np

app = Flask(__name__)
app.config['APP_NAME'] = 'SharedData API'
app.config['FLASK_ENV'] = 'production'
app.config['FLASK_DEBUG'] = '0'
if not 'SHAREDDATA_SECRET_KEY' in os.environ:
    raise Exception('SHAREDDATA_SECRET_KEY environment variable not set')
if not 'SHAREDDATA_TOKEN' in os.environ:
    raise Exception('SHAREDDATA_TOKEN environment variable not set')

app.config['SECRET_KEY'] = os.environ['SHAREDDATA_SECRET_KEY']
app.config['SWAGGER'] = {
    'title': 'SharedData API',
    'uiversion': 3
}
docspath = 'ServerAPIDocs.yml'
swagger = Swagger(app, template_file=docspath)


@app.route('/api/heartbeat', methods=['GET', 'POST'])
def heartbeat():
    time.sleep(3)
    return jsonify({'heartbeat':True}), 200

@app.route('/api/auth', methods=['GET', 'POST'])
def auth():
    try:
        # check for the token in the header
        clienttoken = request.headers.get('X-Custom-Authorization', '')
        if clienttoken == '':
            clienttoken = request.args.get('token','') # Not Optional
        if clienttoken != os.environ['SHAREDDATA_TOKEN']:
            return jsonify({'error':'unauthorized'}), 401
        else:
            return jsonify({'authenticated':True}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/subscribe/<database>/<period>/<source>/<tablename>', methods=['GET'])
def subcribe(database, period, source, tablename):
    try:        
        clienttoken = request.args.get('token') # Not Optional
        if clienttoken != os.environ['SHAREDDATA_TOKEN']:
            return jsonify({'error':'unauthorized'}), 401
                
        tablesubfolder = request.args.get('tablesubfolder')  # Optional
        if tablesubfolder is not None:
            table = shdata.table(database, period, source, tablename+'/'+tablesubfolder)
        else:
            table = shdata.table(database, period, source, tablename)

        if table.table.hasindex:
            lookbacklines = request.args.get('lookbacklines', default=1000, type=int)  # Optional
            lookbackid = table.count - lookbacklines
            if 'lookbackdate' in request.args:
                lookbackdate = pd.Timestamp(request.args.get('lookbackdate'))
                lookbackid, _ = table.get_date_loc(lookbackdate)            
            if lookbackid < 0:
                lookbackid = 0

            ids2send = np.arange(lookbackid, table.count)
            if 'mtime' in request.args:
                mtime = pd.Timestamp(request.args.get('mtime'))
                newids = lookbackid + np.where(table['mtime'][ids2send] >= mtime)[0]
                ids2send = np.intersect1d(ids2send, newids)

        else:
            clientcount = request.args.get('count', default=0, type=int)  # Optional
            if clientcount<table.count:
                ids2send = np.arange(clientcount, table.count-1)
            else:
                ids2send = np.array([])
        
        rows2send = len(ids2send)
        if rows2send == 0:
            return Response(status=204)
        
        # Compress & paginate the response        
        maxrows = np.floor(int(5*1024*1024)/table.itemsize)
        if rows2send>maxrows:
            # paginate
            page = request.args.get('page', default=1, type=int)
            ids2send = ids2send[int((page-1)*maxrows):int(page*maxrows)]

        compressed = lz4f.compress(table[ids2send].tobytes())
        responsebytes = len(compressed)
        response = Response(compressed, mimetype='application/octet-stream')
        response.headers['Content-Encoding'] = 'lz4'
        response.headers['Content-Length'] = responsebytes        
        response.headers['Content-Pages'] = int(np.ceil(rows2send/maxrows))
        return response                                
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@app.route('/api/publish/<database>/<period>/<source>/<tablename>', methods=['GET'])
def publish_get(database, period, source, tablename):
    try:        
        clienttoken = request.args.get('token') # Not Optional
        if clienttoken != os.environ['SHAREDDATA_TOKEN']:
            return jsonify({'error':'unauthorized'}), 401
                
        tablesubfolder = request.args.get('tablesubfolder')  # Optional
        if tablesubfolder is not None:
            table = shdata.table(database, period, source, tablename+'/'+tablesubfolder)
        else:
            table = shdata.table(database, period, source, tablename)

        msg = {'count': int(table.count)}

        if table.table.hasindex:
            lookbacklines = request.args.get('lookbacklines', default=1000, type=int)  # Optional
            lookbackid = table.count - lookbacklines
            if 'lookbackdate' in request.args:
                lookbackdate = pd.Timestamp(request.args.get('lookbackdate'))
                lookbackid, _ = table.get_date_loc(lookbackdate)            
            if lookbackid < 0:
                lookbackid = 0

            ids2send = np.arange(lookbackid, table.count)            
            msg['mtime'] = pd.Timestamp(np.datetime64(np.max(table['mtime'][ids2send])))

        return jsonify(msg)

        
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/publish/<database>/<period>/<source>/<tablename>', methods=['POST'])
def publish_post(database, period, source, tablename):
    try:        
        clienttoken = request.args.get('token') # Not Optional
        if clienttoken != os.environ['SHAREDDATA_TOKEN']:
            return jsonify({'error':'unauthorized'}), 401
                
        tablesubfolder = request.args.get('tablesubfolder')  # Optional
        if tablesubfolder is not None:
            table = shdata.table(database, period, source, tablename+'/'+tablesubfolder)
        else:
            table = shdata.table(database, period, source, tablename)
        
        data = lz4f.decompress(request.data)
        buffer = bytearray()
        buffer.extend(data)
        if len(buffer) >= table.itemsize:
            # Determine how many complete records are in the buffer
            num_records = len(buffer) // table.itemsize
            # Take the first num_records worth of bytes
            record_data = buffer[:num_records *
                                        table.itemsize]
            # And remove them from the buffer
            del buffer[:num_records *
                                table.itemsize]
            # Convert the bytes to a NumPy array of records
            rec = np.frombuffer(
                record_data, dtype=table.dtype)
                
            if table.table.hasindex:
                # Upsert all records at once
                table.upsert(rec)
            else:
                # Extend all records at once
                table.extend(rec)
            
            return Response(status=200)        
        
        return Response(status=204)

    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/table/<database>/<period>/<source>/<tablename>', methods=['GET'])
@swag_from(docspath)
def table(database, period, source, tablename):
    try:
        clienttoken = request.args.get('token') # Not Optional
        if clienttoken != os.environ['SHAREDDATA_TOKEN']:
            return jsonify({'error':'unauthorized'}), 401
        
        tablesubfolder = request.args.get('tablesubfolder')  # Optional
        startdate = request.args.get('startdate')  # Optional
        enddate = request.args.get('enddate')  # Optional
        symbols = request.args.get('symbols')  # Optional
        portfolios = request.args.get('portfolios')  # Optional
        page = request.args.get('page', default=1, type=int)
        per_page = min(request.args.get(
            'per_page', default=1000000, type=int), 1000000)

        if period == 'M1':
            if startdate is not None:
                startdate = pd.Timestamp(startdate).normalize()
                tablename = tablename + '/' + startdate.strftime('%Y%m')
        elif period == 'M15':
            if startdate is not None:
                startdate = pd.Timestamp(startdate).normalize()
                tablename = tablename + '/' + startdate.strftime('%Y')

        if tablesubfolder is not None:
            tbl = shdata.table(database, period, source, tablename+'/'+tablesubfolder)
        else:
            tbl = shdata.table(database, period, source, tablename)
        
        if startdate is not None:
            startdate = pd.Timestamp(startdate).normalize()
            dti, _ = tbl.get_date_loc(startdate)
        else:
            dti = 0

        if enddate is not None:
            enddate = pd.Timestamp(enddate).normalize()
            _, dte = tbl.get_date_loc(enddate)
        else:
            dte = tbl.count

        # Calculate start and end for slicing the DataFrame
        startpage = (page - 1) * per_page
        endpage = startpage + per_page

        loc = np.arange(dti, dte)
        if symbols is not None:
            symbols = symbols.split(',')
            symbolloc = []
            for symbol in symbols:
                symbolloc.extend(tbl.get_symbol_loc(symbol))
            symbolloc = np.array(symbolloc)
            if len(symbolloc) > 0:
                loc = np.intersect1d(loc, symbolloc)

        if portfolios is not None:
            portfolios = portfolios.split(',')
            portloc = []
            for port in portfolios:
                portloc.extend(tbl.get_portfolio_loc(port))
            portloc = np.array(portloc)
            if len(portloc) > 0:
                loc = np.intersect1d(loc, portloc)

        # Apply pagination
        df = tbl.records2df(tbl[loc[startpage:endpage]])
        pkey = df.index.names
        df = df.reset_index()
        df = df.applymap(lambda x: x.isoformat() if isinstance(x, datetime.datetime) else x)
        
        response = {
            'page': page,
            'per_page': per_page,
            'total': len(loc),
            'pkey': pkey,
            'data': df.to_dict(orient='records')
        }

        if 'gzip' in request.headers.get('Accept-Encoding', ''):            
            response_json = json.dumps(response).encode('utf-8')            
            response_compressed = gzip.compress(response_json, compresslevel=1)            
            response = Response(response_compressed, mimetype='application/json')
            response.headers['Content-Encoding'] = 'gzip'
            return response
        else:
            return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    from waitress import serve
    import threading
    import sys

    from SharedData.SharedData import SharedData    
    shdata = SharedData('SharedData.IO.ServerAPI', user='master')
    from SharedData.Logger import Logger

    Logger.log.info('Starting API Server...')

    if len(sys.argv) >= 2:
        _argv = sys.argv[1:]
    else:
        errmsg = 'Please specify IP and port to bind!'
        Logger.log.error(errmsg)
        raise Exception(errmsg)
        
    args = _argv[0].split(',')
    host = args[0]
    port = int(args[1])
        
    
    def send_heartbeat():
        while (True):
            Logger.log.debug('#heartbeat#host:%s,port:%i' % (host, port))
            time.sleep(15)

    t = threading.Thread(target=send_heartbeat, args=())
    t.start()

    Logger.log.info('ROUTINE STARTED!')
    serve(app, host=host, port=port, _quiet=True)
