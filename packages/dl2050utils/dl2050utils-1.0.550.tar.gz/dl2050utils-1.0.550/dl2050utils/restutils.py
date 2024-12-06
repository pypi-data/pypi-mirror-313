import sys
import datetime
import random
import urllib
from pathlib import Path
import json
import hashlib
import orjson
import jwt
import asyncpg
import requests
import aiohttp
import starlette
from starlette.responses import JSONResponse
# from google.cloud import storage
from dl2050utils.core import oget, is_numeric_str
from dl2050utils.fs import read_json

# ####################################################################################################
# Utility functions
# ####################################################################################################

def mk_key(n=4):
    return ''.join([chr(48+i) if i<10 else chr(65-10+i) for i in [random.randint(0, 26+10-1) for _ in range(n)]])
    # return ''.join(random.choice(string.ascii_lowercase) for i in range(n))

def get_hash(o, secret):
    o1 = {**o}
    o1['secret']=secret
    return hashlib.sha224(json.dumps(o1).encode()).hexdigest()

def check_hash(o, h, secret):
    o1 = {**o}
    o1['secret']=secret
    return get_hash(o1,secret)==h

def mk_jwt_token(uid, email, secret):
    JWT_EXP_DELTA_SECONDS = 30*24*3600
    payload = {
        'uid':uid,
        'email':email,
        'username':'',
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_EXP_DELTA_SECONDS)
    }
    return jwt.encode(payload, secret, 'HS256') # .decode('utf-8')

# ####################################################################################################
# REST Responses and Exceptions
# ####################################################################################################
    
def orjson_serialize(obj):
    if isinstance(obj, asyncpg.pgproto.pgproto.UUID):
        return str(obj)
    raise TypeError

class OrjsonResponse(JSONResponse):
    def render(self, content):
        return orjson.dumps(content, option=orjson.OPT_SERIALIZE_NUMPY, default=orjson_serialize)

def rest_ok(d=None):
    if d is None: d = {}
    if type(d)!=dict: d = {'result':d}
    if 'status' not in d: d['status'] = 'OK'
    return OrjsonResponse(d)

class HTTPException(Exception):
    def __init__(self, status_code, detail, error_type='APP'):
        self.status_code,self.detail,self.error_type = status_code,detail or '',error_type
    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f'{class_name}(status_code={self.status_code!r}, detail={self.detail!r})'

def log_and_raise(LOG, error_type='APP', label='', label2='', msg='', status_code=500):
    """Generic function to log and error and raise an HTTPException that force the return of an error status and message."""
    if LOG is not None:
        LOG(4, 0, label=label, label2=label2, msg=msg)
    raise HTTPException(status_code, msg, error_type=error_type)

def log_and_raise_exception(LOG, label='', label2='', msg=''):
    """log_and_raise for Exceptions, enforcing status 500."""
    return log_and_raise(LOG, error_type='EXCEPTION', label=label, label2=label2, msg=msg, status_code=500)

def log_and_raise_service(LOG, label='', label2='', msg='', status_code=500):
    """log_and_raise for internal service functions, defaulting to status 500."""
    return log_and_raise(LOG, error_type='SERVICE', label=label, label2=label2, msg=msg, status_code=status_code)

def log_and_raise_rest(LOG, label='', label2='', msg='', status_code=500):
    """log_and_raise for REST application functions, defaulting to status 500."""
    return log_and_raise(LOG, error_type='REST', label=label, label2=label2, msg=msg, status_code=status_code)

# To be completed and tested
async def get_request_json(request, LOG=None, label=None, label2=None):
    try:
        data = await request.json()
    except json.JSONDecodeError as e:
        if LOG: log_and_raise_service(LOG, label=label, label2=label2, msg=f"Input JSON with errors", status_code=401)
        return None
    return data

# ####################################################################################################
# REST params
# ####################################################################################################

def enforce_required_args(LOG, payload, args, label='', label2='', as_list=False):
    """ Returns dict (or list is as_list is True) with args present in payload. Raises REST exception if any arg is missing """
    args2,miss = {},[]
    if payload is None: return args2
    for e in args:
        if e not in payload:
            miss.append(e)
        else:
            args2[e] = payload[e]
    if len(miss):
        msg = f'Missing required args for {label2}: {", ".join(miss)}'
        log_and_raise_rest(LOG, label=label, label2=label2, msg=msg, status_code=400)
    if as_list:
        return [args2[e] for e in args2]
    return args2

def get_optional_args(payload, args, as_list=False):
    """ Returns dict (or list is as_list is True) with args present in payload """
    if as_list:
        return [payload[e] for e in args if e in payload] if payload is not None else []
    return {e:payload[e] for e in args if e in payload} if payload is not None else {}

# ####################################################################################################
# Meta
# ####################################################################################################

# async def get_meta(path, db, model):
#     meta = read_json(f'{path}/{model}/{model}.json')
#     if meta is not None: return meta
#     row = await db.select_one('models', {'model': model})
#     if row is not None: return json.loads(row['meta'])
#     return None

def sync_get_meta(path, db, model):
    meta = read_json(f'{path}/{model}/{model}.json')
    if meta is not None: return meta
    row = db.sync_select_one('models', {'model': model})
    if row is not None: return json.loads(row['meta'])
    return None

# ####################################################################################################
# Requests
# ####################################################################################################

def sync_request(url, method='GET', headers=None, payload=None, LOG=None):
    """
    Performs a GET or POST request.
    Always returns a dict with attrs status, message and optionally result.
    """
    if headers is None: headers = {}
    try:
        if method.upper() == 'GET':
            res = requests.get(url, headers=headers, params=payload)
            # print(res.url)
        elif method.upper() == 'POST':
            headers['Content-Type'] = 'application/json'
            res = requests.post(url, headers=headers, json=payload)
        else:
            return {'status':400, 'message':f'Unsupported method: {method}'}
        # Raises HTTPError for bad responses (4xx or 5xx)
        res.raise_for_status()
        if 'application/json' in res.headers.get('Content-Type', ''): return res.json()
        return res.text
    except requests.exceptions.HTTPError as exc:
        if res.content:
            try:
                return res.json()
            except ValueError as exc:
                if LOG: LOG(4, 0, label='sync_request', label2='HTTPError', msg=f'{res.text}')
                return {'status':500, 'message':f'{res.text}'}
        else:
            if LOG: LOG(4, 0, label='sync_request', label2='HTTPError', msg=f'{exc}')
            return {'status':500, 'message':'HTTPError'}
    except requests.exceptions.ConnectionError as exc:
        if LOG:  LOG(4, 0, label='sync_request', label2='ConnectionError', msg=f'Connection error: {exc}')
        return {'status': 500, 'message':'ConnectionError', 'details': str(exc)}
    except Exception as exc:
        if LOG: LOG(4, 0, label='sync_request', label2='EXCEPTION', msg=f'{exc}')
        return {'status':500, 'message': f'Server Error'}

# To review
async def post_request(url, payload, headers={}):
    async with aiohttp.ClientSession(headers=headers) as session:
        response = await session.post(url, json=payload)
        print(await response.json())

async def post_request_sync(url, payload, headers={}):
    res = requests.post(url, json=payload, headers=headers)

# To review
async def rest_request(session, url, headers, host, port, payload=None, method='POST', json=True):
    print(f'{method} url: http://{host}:{port}{url}')
    if method not in ['POST', 'GET']:
        print('Invalid HTTP method')
        return
    if method=='POST':
        payload = payload or {}
        r = await session.post(f'http://{host}:{port}{url}', headers=headers, json=payload)
    else:
        r = await session.get(f'http://{host}:{port}{url}', headers=headers)
    print(f'HTTP response status: {r.status}')
    if r.status==500:
        trace = await r.text()
        print('Server EXCEPTION trace: :', trace)
        return None
    else:
        if r.status==403:
            print(r)
            return None
        if r.status>=400:
            text = await r.text()
            print(text)
        if json:
            res = await r.json()
            return res
        else:
            return None

# To review      
async def do_login(session, host, port, url, email, passwd):
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    payload = {'email': email, 'passwd': passwd}
    res = await rest_request(session, url, headers, host, port, payload=payload, method='POST', json=True)
    jwt_token = oget(res,['jwt_token'])
    if jwt_token is None:
        print('ERROR: ', res)
        return None
    return {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization':f"Bearer {jwt_token}"}

# ##############################################################################################################
# File download from url:
#   async_upload, async_download
# ##############################################################################################################

async def async_upload(url, ps):
    """Uploads files ps to url."""
    async with aiohttp.ClientSession() as session:
        data = aiohttp.FormData()
        for i,p in enumerate(ps):
            data.add_field(f'file-{i}', open(p,'rb'), filename=p)
        async with session.post(url, data=data) as r:
            if(r.status!=200):
                print(f'Error: status=={r.status}, msg={await r.text()}')
                return True
            print(await r.text())
            return False
        
async def async_download(url):
    """Downloads file from url and returns the file data."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            if(r.status!=200):
                print(f'Error: status=={r.status}, msg={await r.text()}')
                return None
            return await r.text()

# Draft
# def download_url(url, dest, overwrite=False, pbar=None, show_progress=True, chunk_size=1024*1024, timeout=4, retries=5):
#     """Downloads file from url to dest unless it exists and not overwrite."""
#     if os.path.exists(dest) and not overwrite: return
#     s = requests.Session()
#     s.mount('http://',requests.adapters.HTTPAdapter(max_retries=retries))
#     u = s.get(url, stream=True, timeout=timeout)
#     try:
#         file_size = int(u.headers["Content-Length"])
#     except:
#         show_progress = False
#     with open(dest, 'wb') as f:
#         nbytes = 0
#         # if show_progress: pbar = progress_bar(range(file_size), auto_update=False, leave=False, parent=pbar)
#         try:
#             for chunk in u.iter_content(chunk_size=chunk_size):
#                 nbytes += len(chunk)
#                 if show_progress: pbar.update(nbytes)
#                 f.write(chunk)
#         except requests.exceptions.ConnectionError as exc:
#             print(f'EXCEPTION: Download of {url} has failed after {retries} retries: {str(exc)}')
#             return False
#     return True

# Draft
# def download_file(url, fname=None, ext='.tgz'):
#     """Downloads file from url to destination fname."""
#     p = Path(fname or f"{url.split('/')[-1]}{ext}")
#     (p.parent).mkdir(parents=True, exist_ok=True )
#     if not p.exists():
#         print(f'Downloading {url}')
#         if not download_url(f'{url}{ext}', p):
#             return None
#     return p

# ################################################################################
# form_files_upload
# ################################################################################

async def form_files_upload(LOG, items, p, max_size=int(1e9)):
    """ Uploads all files in file items to p with relatives paths. Returns number of filez and total size."""
    n,sz = 0,0
    for k,f in items:
        if type(f)==starlette.datastructures.UploadFile:
            sz += f.size
            if sz>max_size:
                log_and_raise_service(LOG, label='FS', label2='/upload', msg=f'Files size exceded {max_size} limit')
            fname = urllib.parse.unquote(f.filename)
            # Keep just name and suffix, exclude absolute path, create new path inside p
            p1 = Path(fname)
            p1 = p / f'{p1.stem}{p1.suffix}'
            p1.parent.mkdir(parents=True, exist_ok=True)
            data = await f.read()
            with open(str(p1), 'wb') as f2:
                f2.write(data)
            n += 1
    return n,sz

# ################################################################################
# Signed URLs for File Server download/upload: 
#   fs_download_signed_url, fs_upload_signed_url
# ################################################################################

def fs_download_signed_url(secret, base_url, bucket, key, timeout=7*24*3600):
    """
        baseurl must specify the protocol, example: http://fs:4000
    """
    payload = {
        'bucket': bucket,
        'key': key,
        'ts': datetime.datetime.now().isoformat(),
        'timeout': timeout
    }
    payload['h'] = get_hash(payload, secret)
    url = f'{base_url}/download?{urllib.parse.urlencode(payload)}'
    return url

def fs_upload_signed_url(secret, base_url, bucket, key, size, timeout=7*24*3600):
    """
        baseurl must specify the protocol, example: http://fs:4000
    """
    payload = {
        'bucket': bucket,
        'key': key,
        'size': size,
        'ts': datetime.datetime.now().isoformat(),
        'timeout': timeout
    }
    payload['h'] = get_hash(payload, secret)
    url = f'{base_url}/upload?{urllib.parse.urlencode(payload)}'
    return url

# ################################################################################
# Signed URLs for Google Cloud Storage download/upload: 
#   gcs_download_signed_url, gcs_upload_signed_url
# TODO: Deprecate and replace by GS Class from fs.py
# ################################################################################


# def gcs_download_signed_url(bucket_name, blob_name, timeout=15*60):
#     """
#         Generates a v4 signed URL on GCS for downloading a blob.
#         Signed url expires according to timeout (in seconds).
#         Requires a service account key json file (obtained in IAM).
#         Requires the ENV variable GOOGLE_APPLICATION_CREDENTIALS with this file path:
#             os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path_to_file
#         https://cloud.google.com/storage/docs/samples/storage-generate-signed-url-v4#storage_generate_signed_url_v4-python
#     """
#     try:
#         sc = storage.Client()
#         bucket = sc.bucket(bucket_name)
#         blob = bucket.blob(blob_name)
#         url = blob.generate_signed_url(version="v4", expiration=datetime.timedelta(seconds=timeout), method="GET")
#         return url
#     except Exception as exc:
#         print(f'EXCEPTION: {str(exc)}')
#         return None

# def gcs_upload_signed_url(bucket_name, blob_name, timeout=15*60, size=None):
#     """
#         Generates a v4 signed URL on GCS for uploading a blob using HTTP PUT.
#         Signed url expires according to timeout (in seconds).
#         Requires a service account key json file (obtained in IAM).
#         Requires the ENV variable GOOGLE_APPLICATION_CREDENTIALS with this file path:
#             os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path_to_file
#         https://cloud.google.com/storage/docs/samples/storage-generate-upload-signed-url-v4
#     """
#     try:
#         sc = storage.Client()
#         bucket = sc.bucket(bucket_name)
#         blob = bucket.blob(blob_name)
#         expiration = datetime.timedelta(seconds=timeout)
#         url = blob.generate_signed_url(version="v4", expiration=expiration, method="PUT", content_type="application/octet-stream")
#     except Exception as exc:
#         print(f'EXCEPTION: {str(exc)}')
#         return None
#     return url

# ####################################################################################################
# Etc - to review
# ####################################################################################################

# def mk_weeks(ds1='2018-01-01', ds2=None, weekday=6):
#     d1 = datetime.datetime.strptime(ds1, '%Y-%m-%d').date()
#     delta = 5 - d1.weekday()
#     if delta<0: delta+=7
#     d1 += datetime.timedelta(days=delta)
#     d2 = datetime.datetime.now().date() if ds2 is None else datetime.datetime.strptime(ds2, '%Y-%m-%d').date()
#     ds = [d.strftime("%Y-%m-%d") for d in rrule.rrule(rrule.WEEKLY, dtstart=d1, until=d2)]
#     return ds[::-1]

# def get_week2(weeks, week): return weeks[weeks.index(week)+1] if weeks.index(week)+1<len(weeks) else None

# def s3_urls(s3, bucket_name, prefix):
#     response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix, MaxKeys=1024)['Contents']
#     return [f'http://{bucket_name}.s3-eu-west-1.amazonaws.com/{e["Key"]}' for e in response]
