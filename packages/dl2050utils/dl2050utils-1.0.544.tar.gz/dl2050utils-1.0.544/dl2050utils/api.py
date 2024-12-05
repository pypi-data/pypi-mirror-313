# #################################################################################################################
# api.py
#
# APIServer, APIWorker, APISyncWorker
#
# This version assumes that input data (payloads) and output data (responses) are very short.
# Large inputs/outputs must be implemented with urls pointing to payloads/results. The runner callback must
# download the inputs from a payload url, upload the results and return the result url.
#
# Both API Server and Worker Server requires configuration defined by the cfg dict of this form:
# cfg = {
#   'apiserver': {'servive':<service>, 'wkey':<wkey>}
#   'gcloud': {'gs_key':<gs_key_struct>}}
#   }
# If cfg is passed as argument it is used, otherwise cfg is loaded from the yaml file (secret)
# trough config_load(<service>).
#
# Responses are allwways JSON, both for GET/POST of the form {status_code:<int>, message:<str>, result:<dict>}
#
# Example APIServer:
#   apis = APIServer('kardio')
#   api.run()
#
# Example APIWorker:
#   def proc(task, start_cb, done_cb, error_cb):
#       eta = 3
#       start_cb(task['req_uid'], eta)
#       time.sleep(eta)
#       done_cb(task['req_uid'], {'ml':42}, used_credits=1.)
#       return 0
#   ws = APIWorker('kardio', url='http://ju:9000')
#   ws.run(proc)
#
# Example APIClient:
#   api_cli = APIClient(key=key, url='http://ju:9000')
#   res = api_cli.req({'url':'www.xxx.com'})
#   req_uid = res['result']['req_uid']
#   api_cli.check(req_uid)
#
# #################################################################################################################
import sys
import time
import datetime
import secrets
import string
from urllib.parse import parse_qs
from pathlib import Path
import orjson
import sqlite3
import uvicorn
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException
from dl2050utils.core import oget, now, date_to_srt, str_to_date, is_numeric_str, get_uid, listify, base64_encode
from dl2050utils.env import config_load
from dl2050utils.log import AppLog
from dl2050utils.fs import json_dumps
from dl2050utils.sqlite import Sqlite
from dl2050utils.restutils import sync_request
from dl2050utils.gs import GS

TASK_STATUS = ['REQUESTED', 'DISPATCHED', 'START', 'DONE', 'ERROR']
MAX_SIZE = int(10e6)

# #################################################################################################################
# REST
# #################################################################################################################

class ORJSONResponse(JSONResponse):
    """Custom JSONResponse using orjson with numpy serialization support."""
    def render(self, content) -> bytes:
        return orjson.dumps(content, option=orjson.OPT_SERIALIZE_NUMPY)
    
def rest_ok(content=None, message=None):
    content = content if type(content)==dict else {}
    if 'status' not in content: content['status'] = 'OK'
    if message: content['message'] = message
    return ORJSONResponse(status_code=200, content=content)

def raise_error(status_code=500, msg='', LOG=None):
    """Generic function to raise HTTPException and optionally log the error (used in the API)"""
    if LOG is not None: LOG(4, 0, label='HTTPException', msg=msg)
    raise HTTPException(status_code=status_code, detail=msg)

async def http_exception(request, exc):
    return ORJSONResponse(status_code=exc.status_code,
                        content={'status':exc.status_code, 'message': exc.detail or 'HTTP error'})
    # 'error_code': exc.__class__.__name__

async def server_error_exception(request, exc):
    return ORJSONResponse(status_code=500, content={'status':500, 'message':'Internal server error'})

def extract_key(request, LOG=None):
    # Retrieve API key from Authorization header
    authorization = request.headers.get('Authorization')
    if not authorization or not authorization.startswith('Bearer '):
        raise_error(403, 'Missing or malformed Authorization header', LOG)
    # Extract the key from the Authorization header
    key = authorization.split(' ')[1]
    return key

def get_param(request, param_name, param_type, max_length=None, required=True, data=None, LOG=None):
    """Get and sanitize param, from query_params for GET or from json data for POST requests"""
    param = request.query_params.get(param_name) if request.method=='GET' else oget(data,[param_name])
    if required and param is None:
        raise_error(400, f'Missing required param {param_name} on {request.url.path}', LOG)
    if param is None: return None
    if param_type==str:
        if max_length and len(param)>max_length:
            raise_error(400, f'Invalid param {param_name} on {request.url.path}', LOG)
        return param.strip()
    elif param_type==int or param_type==float:
        if type(param)==int or type(param)==float: return param_type(param)
        if type(param)==str and is_numeric_str(param): return param_type(param)
        raise_error(400, f'Invalid number format for param {param_name} on {request.url.path}', LOG)
    elif param_type==dict or param_type==bytes:
        if max_length is not None and sys.getsizeof(param)>max_length:
            raise_error(400, f'Invalid param {param_name} on {request.url.path}', LOG)
        return param
    elif param_type==list:
        # TODO: check for list size and list elements types ans syses
        return param
    raise_error(400, f'Invalid param type: {param_name} on {request.url.path}', LOG)

# #################################################################################################################
# Utility functions
# #################################################################################################################

def db_create(db):
    Q1 = '''
        CREATE TABLE IF NOT EXISTS api_keys (
            key CHAR(256) PRIMARY KEY,
            email VARCHAR(128),
            name VARCHAR(128),
            created_at DATETIME,
            reset_calls_at DATETIME,
            active BOOLEAN,
            rate_limit INTEGER,
            calls INTEGER DEFAULT 0,
            calls_total INTEGER DEFAULT 0,
            credits REAL DEFAULT 0 -- current credits total
        )
    '''
    Q2 = '''
        CREATE TABLE IF NOT EXISTS api_tasks (
            req_uid CHAR(32) PRIMARY KEY,
            created_at DATETIME,
            key CHAR(256),
            kind CHAR(32),
            status CHAR(32),
            urls TEXT, -- json stringyfied list of dicts with url and file name
            results_url TEXT,
            eta DATETIME,
            credits REAL DEFAULT 0 -- credits used by task
        );
    '''
    db.execute(Q1)
    db.execute(Q2)

def get_new_key(n=256): return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(n))
def get_reset_time(): return date_to_srt(now()+datetime.timedelta(hours=1))

# #################################################################################################################
# Transactions
# #################################################################################################################

def grab_task(db):
    """
    Gets the oldest task with status REQUESTED and updates the status to PROCESSING with atomiticity.
    TODO: replace with Sqlite driver method dequeu
    """
    tbl = 'api_tasks'
    d = None
    try:
        # Begin a transaction to lock the row and ensure atomicity
        db.conn.execute('BEGIN IMMEDIATE')
        cursor = db.conn.cursor()
        Q = f"SELECT * FROM {tbl} WHERE status == 'REQUESTED' ORDER BY req_uid LIMIT 1"
        cursor.execute(Q)
        task = cursor.fetchone()
        if not task:
            db.conn.rollback()
            return None
        # Fetch the column names and convert the row to a dictionary
        column_names = [description[0] for description in cursor.description]
        d = dict(zip(column_names, task))
        cursor.execute(f"UPDATE {tbl} SET status = ? WHERE req_uid = ?", ('PROCESSING', d['req_uid']))
        db.conn.commit()
        return d
    except sqlite3.DatabaseError as exc:
        print(f'grab_task EXCEPTION: {exc}')
        db.conn.rollback()
    
def update_credits(db, key, value, LOG):
    """DB transaction to update key credits value"""
    if type(value)!=int and type(value)!=float:
        LOG(4, 0, label='update_credits', msg=f'ERROR: invalid type for value')
        return
    try:
        value = float(value)
        db.conn.execute('BEGIN IMMEDIATE')
        cursor = db.conn.cursor()
        cursor.execute("""UPDATE api_keys SET credits = credits + ? WHERE key = ?""", (value, key))
        db.conn.commit()
    except Exception as exc:
        LOG(4, 0, label='update_credits', msg=f'ERROR: EXCEPTION: {exc}')
        db.conn.rollback()
        raise exc

# #################################################################################################################
# APIServer
# #################################################################################################################

class APIServer:
    def __init__(self, service, sync_worker_url=None, cfg=None):
        if service is None: raise Exception('service must be defined')
        if cfg is None: cfg = config_load(service)
        p0 = Path(f'/data/{service}/apiserver')
        (p0/'workfiles').mkdir(parents=True, exist_ok=True)
        if not (p0/'api-db').is_file(): print(f'Database not found')
        self.db = Sqlite(p0/'api-db')
        self.skey,self.wkey = oget(cfg,['apiserver','skey']),oget(cfg,['apiserver','wkey'])
        if self.wkey is None: raise Exception('Worker key not defined')
        self.fs = GS(service) if oget(cfg,['gcloud','gs_key']) is not None else None
        self.bucket = f'{service}-apiserver'
        self.sync_worker_url = sync_worker_url
        self.port = 9000
        self.LOG = AppLog(cfg, service=f'{service}-apis')
        self.LOG(2, 0, label='READY')
    
    # #################################################################################################################
    # Admin
    # #################################################################################################################

    def db_create(self): db_create(self.db)
    def new_key(self, email, rate_limit=100):
        key = get_new_key()
        self.add_key(key, email, rate_limit=rate_limit)
        return key
    def add_key(self, key, email, rate_limit=100):
        self.db.insert('api_keys',{'key':key, 'email':email, 'active':True, 'rate_limit':rate_limit,
                                   'reset_calls_at':get_reset_time()})
    def revoke_key(self, key): return self.select_and_update('api_keys', 'key', {'key':key, 'active':False})
    def get_key(self, key): return self.db.select_one('api_keys', 'key', key)
    def get_keys(self): return self.db.select('api_keys')
    def get_tasks(self): return self.db.select('api_tasks')
    def get_task(self, req_uid): return self.db.select_one('api_tasks', 'req_uid', req_uid)
    def remove_all_tasks(self): self.db.delete_all('api_tasks')
    def reset_rate_limit(self, key): self.db.update('api_keys', 'key', {'key':key, 'calls':0})
    def add_credits(self, key, value): update_credits(self.db, key, value, self.LOG)
    def remove_credits(self, key, value):
        if value is not None: update_credits(self.db, key, -value, self.LOG)
    
    # #################################################################################################################
    # Access control
    # #################################################################################################################

    def check_access(self, request, enforce_credits=True):
        """Enforces valid client key for access. Returns 0 if valid, raises HTTP error otherwise."""
        key = extract_key(request, self.LOG)
        # Service key skey has inconditional access
        if key==self.skey: return 0
        # Check key existance and status
        d = self.db.select_one('api_keys', 'key', key)
        if d is None: raise_error(403, 'Invalid API key', self.LOG)
        if d['active']==0: raise_error(403, 'Inactive API key', self.LOG)
        # Check rate limits and credits
        if d['calls'] > d['rate_limit']: raise_error(403, 'Rate limit exceded', self.LOG)
        if enforce_credits and d['credits'] < 0: raise_error(403, 'Out of credits', self.LOG)
        # Update statistics and time window limit
        for c in ['calls','calls_total']: d[c] += 1
        ts1,ts2 = now(),str_to_date(d['reset_calls_at'])
        if ts1 > ts2: d['calls'],d['reset_calls_at'] = 0,ts2+datetime.timedelta(hours=1)
        self.db.update( 'api_keys', 'key', d)
        return key
    
    def check_worker_access(self, request):
        """Enforces valid worker key for access."""
        key = extract_key(request, self.LOG)
        if key!=self.wkey: raise_error(403, 'Unauthorized Worker key', self.LOG)
        return key
    
    def reset_rate_limit(self, key):
        ts = now()+datetime.timedelta(hours=1)
        return self.db.select_and_update('api_keys', 'key', {'key':key, 'calls':0, 'reset_calls_at':ts})
    
    # #################################################################################################################
    # API Entrypoints
    # #################################################################################################################

    async def get_signed_urls(self, request):
        """
        Provides signed urls for every file name defined in the fnames parameter.
        Keep the files tree structure on the File Server.
        All file names will have the same uid prefix or root. A new uid is allways generated on this request.
        Returns dict with two lists, the upload_urls and download_urls.
        """
        self.check_access(request)
        if self.fs is None: raise_error(400, 'Signed urls not available', self.LOG)
        data = await request.json()
        fnames = get_param(request, 'fnames', list, data=data, LOG=self.LOG)
        uid = get_uid()
        upload_urls,download_urls = [],[]
        for fname in fnames:
            key = f'{uid}/{fname}'
            upload_url,download_url = self.fs.urls(self.bucket, key)
            upload_urls.append(upload_url),download_urls.append(download_url)
        self.LOG(2, 0, label='APIServer', label2='/apiserver/get_signed_urls', msg=f"#{len(fnames)} urls issued")
        return rest_ok({'upload_urls':upload_urls, 'download_urls':download_urls})
    
    async def proc(self, request):
        """Request for sync processing. payload has data blob. response has the proc output."""
        key = self.check_access(request)
        if self.sync_worker_url is None: raise_error(400, 'Sync Worker not found', self.LOG)
        data = await request.json()
        base64 = get_param(request, 'base64', str, max_length=MAX_SIZE, data=data, LOG=self.LOG)
        # Call sync worker
        url = f'{self.sync_worker_url}/proc'
        headers = {'Authorization': f'Bearer {self.wkey}'}
        # Calls the Sync Worker. If there is an error, an HTTP exeception is automatically raised and returned
        result = sync_request(url, method='POST', headers=headers, payload={'base64':base64}, LOG=self.LOG)
        # Set status
        status = 'Error' if result is None else 'OK'
        if result is None: result = {}
        result['status'] = status
        # Set an uid for the task
        uid = get_uid()
        result['req_uid'] = uid
        # Extract used credicts
        used_credits = oget(result,['used_credits'])
        # Register the task
        task = {'req_uid':uid, 'created_at':now(), 'key':key, 'kind':'SYNC', 'status':'DONE', 'credits':used_credits}
        self.db.insert('api_tasks', task)
        self.remove_credits(task['key'], used_credits)
        self.LOG(2, 0, label='API', label2='/apiserver/proc', msg=f"OK")
        return ORJSONResponse(status_code=200, content=result)
    
    async def req(self, request):
        """Request for async proc. Expects param urls with list of dicts with {url:<url>, name:<name>}."""
        key = self.check_access(request)
        data = await request.json()
        urls = get_param(request, 'urls', list, data=data, LOG=self.LOG)
        req_uid = get_uid()
        task = {'req_uid':req_uid, 'created_at':now(), 'key':key, 'kind':'ASYNC', 'status':'REQUESTED',
                'urls': json_dumps(urls)}
        self.db.insert('api_tasks', task)
        self.LOG(2, 0, label='APIServer', label2='/apiserver/req', msg=f"req_uid={req_uid}")
        return rest_ok({'req_uid':req_uid})
    
    async def check(self, request):  # GET request
        """Check async proc. response has task status on attribute req_status and if DONE has also the results url."""
        self.check_access(request, enforce_credits=False)
        req_uid = get_param(request, 'req_uid', str, max_length=32, LOG=self.LOG)
        task = self.db.select_one('api_tasks', 'req_uid', req_uid)
        if task is None: raise_error(400, 'Request not found', self.LOG)
        res = {'req_status':task['status']}
        if res['req_status']=='DONE':
            res['results_url'] = task['results_url']
            res['credits'] = task['credits']
        else:
            res['eta'] = task['eta']
        return rest_ok(res)
    
    # #################################################################################################################
    # Worker Entrypoints
    # #################################################################################################################
    
    async def grab(self, request):
        self.check_worker_access(request)
        task = grab_task(self.db)
        req_uid = oget(task,['req_uid'])
        if req_uid is not None:
            self.db.select_and_update('api_tasks', 'req_uid',{'req_uid':req_uid,'status':'DISPATCHED'})
            self.LOG(2, 0, label='APIServer', label2='/worker/grab', msg=f'req_uid={req_uid}')
        return rest_ok(task)

    async def start(self, request):
        self.check_worker_access(request)
        data = await request.json()
        req_uid = get_param(request, 'req_uid', str, max_length=32, data=data, LOG=self.LOG)
        eta = get_param(request, 'eta', int, data=data, required=False, LOG=self.LOG)
        self.db.select_and_update('api_tasks', 'req_uid', {'req_uid':req_uid, 'status':'START', 'eta':eta})
        self.LOG(2, 0, label='APIServer', label2='/worker/start', msg=f'req_uid={req_uid}')
        return rest_ok()

    async def done(self, request):
        self.check_worker_access(request)
        data = await request.json()
        req_uid = get_param(request, 'req_uid', str, max_length=32, data=data, LOG=self.LOG)
        results_url = get_param(request, 'results_url', str, data=data, LOG=self.LOG)
        used_credits = get_param(request, 'credits', float, data=data, LOG=self.LOG)
        self.db.select_and_update('api_tasks', 'req_uid',
            {'req_uid':req_uid, 'status':'DONE', 'results_url':results_url, 'credits':used_credits, 'eta':None})
        task = self.get_task(req_uid)
        self.remove_credits(task['key'], used_credits)
        self.LOG(2, 0, label='APIServer', label2='/worker/done', msg=f'req_uid={req_uid}')
        return rest_ok()

    async def error(self, request):
        self.check_worker_access(request)
        data = await request.json()
        req_uid = get_param(request, 'req_uid', str, max_length=32, data=data, LOG=self.LOG)
        message = get_param(request, 'message', str, required=False, data=data, LOG=self.LOG)
        self.db.select_and_update('api_tasks', 'req_uid', {'req_uid':req_uid, 'status':'ERROR', 'eta':None})
        msg = f'req_uid={req_uid}'
        if message is not None: msg += f' , message={message}'
        self.LOG(3, 0, label='APIServer', label2='/worker/error', msg=msg)
        return rest_ok()

    # #################################################################################################################
    # Run
    # #################################################################################################################
    
    def run(self, port=None):
        if self.db is None:
            print('Databse not found - aborting.')
            return
        port = port or self.port
        self.LOG(2, 0, label='RUN', msg=f'Listening in port {port}')
        routes = [
            # Client async routes
            Route('/apiserver/get_signed_urls', endpoint=self.get_signed_urls, methods=['POST']),
            Route('/apiserver/req', endpoint=self.req, methods=['POST']),
            Route('/apiserver/check', endpoint=self.check, methods=['GET']),
            # Client sync routes
            Route('/apiserver/proc', endpoint=self.proc, methods=['POST']),
            # Worker routes
            Route('/worker/grab', endpoint=self.grab, methods=['POST']),
            Route('/worker/start', endpoint=self.start, methods=['POST']),
            Route('/worker/done', endpoint=self.done, methods=['POST']),
            Route('/worker/error', endpoint=self.error, methods=['POST']),
        ]
        exception_handlers = {
            HTTPException: http_exception,
            Exception: server_error_exception,
        }
        app = Starlette(
            debug=True,
            routes=routes,
            exception_handlers=exception_handlers,
            # middleware=self.middleware,
        )
        uvicorn.run(app, port=port, host='0.0.0.0', log_level='critical')

# #################################################################################################################
# APIClient
# #################################################################################################################

class APIClient:
    def __init__(self, key, url):
        self.key,self.url = key,url
    def do_request(self, route, payload):
        headers = {'Authorization': f'Bearer {self.key}'}
        method = 'GET' if route in ['/apiserver/check'] else 'POST'
        return sync_request(f'{self.url}{route}', method=method, headers=headers, payload=payload)
    def get_signed_urls(self, fnames): return self.do_request('/apiserver/get_signed_urls', {'fnames':fnames})
    def proc(self, data): return self.do_request('/apiserver/proc', {'base64':base64_encode(data)})
    def req(self, urls): return self.do_request('/apiserver/req', {'urls':listify(urls)})
    def check(self, req_uid): return self.do_request('/apiserver/check', {'req_uid':req_uid})

# #################################################################################################################
# APISyncWorker
# #################################################################################################################

class APISyncWorker:

    def __init__(self, service, cb, cfg=None):
        if service is None: raise Exception('service must be defined')
        if cfg is None: cfg = config_load('kardio')
        self.wkey = oget(cfg,['apiserver','wkey'])
        if self.wkey is None: raise Exception('worker key not defined')
        self.cb = cb
        self.port = 9500
        self.LOG = AppLog(cfg, service=f'{service}-apiws')
        self.LOG(2, 0, label='READY', label2='START')

    def check_worker_access(self, request):
        """Enforces valid worker key for access."""
        key = extract_key(request, self.LOG)
        if key!=self.wkey: raise_error(403, 'Unauthorized Worker key', self.LOG)
        return key

    async def proc(self, request):
        """"""
        data = await request.json()
        base64 = get_param(request, 'base64', dict, max_length=MAX_SIZE, data=data, LOG=self.LOG)
        self.check_worker_access(request)
        result = self.cb(base64)
        status,ecgs = oget(result,['status']) or 'Error',oget(result,['ecgs'])
        msg = status
        if status=='OK' and type(ecgs)==list: msg += f' #ECGs: {len(ecgs)}'
        self.LOG(2, 0, label='APISyncWorker', label2='/apiserver/proc', msg=msg)
        return ORJSONResponse(status_code=200, content=result)

    def run(self, port=None):
        port = port or self.port
        self.LOG(2, 0, label='RUN', msg=f'Listening in port {port}')
        routes = [
            Route('/proc', endpoint=self.proc, methods=['POST']),
        ]
        exception_handlers = {
            HTTPException: http_exception,
            Exception: server_error_exception,
        }
        app = Starlette(
            debug=True,
            routes=routes,
            exception_handlers=exception_handlers,
            # middleware=self.middleware,
        )
        uvicorn.run(app, port=port, host='0.0.0.0', log_level='critical')

# #################################################################################################################
# class APIWorker:
# #################################################################################################################

class APIWorker:

    def __init__(self, service, cfg=None, api_server_url=None):
        if service is None: raise Exception('service must be defined')
        if cfg is None: cfg = config_load('kardio')
        self.wkey = oget(cfg,['apiserver','wkey'])
        if self.wkey is None: raise Exception('worker key not defined')
        self.api_server_url = api_server_url or 'http://localhost:9000'
        self.LOG = AppLog(cfg, service=f'{service}-apiw')
        self.LOG(2, 0, label='APIWorker', label2='START', msg=f'API Server at {self.api_server_url}')

    def do_request(self, path, payload=None):
        url = f'{self.api_server_url}/{path}'
        headers = {'Authorization': f'Bearer {self.wkey}'}
        res = sync_request(url, method='POST', headers=headers, payload=payload, LOG=self.LOG)
        if oget(res,['status']!=200):
            self.LOG(4, 0, label='APIWorker', label2=path)
            return None
        return res

    def grab(self):
        return self.do_request('worker/grab')

    def start_cb(self, req_uid, eta=None):
        return self.do_request('worker/start', {'req_uid':req_uid, 'eta':eta})

    def done_cb(self, req_uid, results_url, used_credits=0.):
        return self.do_request('worker/done', {'req_uid':req_uid, 'results_url':results_url, 'credits':used_credits})

    def error_cb(self, req_uid, message=None):
        payload = {'req_uid':req_uid}
        if message is not None: payload['message'] = message
        return self.do_request('worker/error', payload)
    
    def run(self, cb):
        self.LOG(2, 0, label='RUN', msg=f'Fetching tasks from {self.api_server_url}')
        try:
            while True:
                task = self.grab()
                req_uid = oget(task,['req_uid'])
                if req_uid is None:
                    time.sleep(1)
                    continue
                self.LOG(2, 0, label='APIWorker', label2='GRAB', msg=f"{req_uid}")
                try:
                    res = cb(task, self.start_cb, self.done_cb, self.error_cb)
                    if res==0:
                        self.LOG(2, 0, label='APIWorker', label2='DONE', msg=f"{req_uid}")
                        continue
                    self.LOG(3, 0, label='APIWorker', label2='ABORTED', msg=f"{req_uid}")
                    self.error_cb(req_uid)
                except Exception as exc:
                    self.error_cb(req_uid)
                    self.LOG(4, 0, label='APIWorker', label2='Callback EXCEPTION', msg=f"{req_uid}, exc={exc}")
        except KeyboardInterrupt:
            self.LOG(2, 0, label='APIWorker', label2='SHUTDOWN')
        except Exception as exc:
            self.LOG(4, 0, label='APIWorker', label2='Server EXCEPTION', msg=f'exc={exc}')
