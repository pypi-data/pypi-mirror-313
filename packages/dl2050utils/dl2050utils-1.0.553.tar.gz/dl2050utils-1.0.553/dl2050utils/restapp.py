"""
restapp.py
App Class

Defines the logic for the REST App, including startup, shudown, Auth routes, downstream services routes and Custom Application routes.

The Auth routes are defined in the Auth module.

The downstream services routes include:
    /api/contact
    /api/get_meta
    /api/get_signed_urls
    /api/download_workfile/{fname}
    /api/upload_workfile
    /api/publish_job
    /api/get_jobs
    /api/get_job

The Custom Application are defined in the routes dict with the following structure:
    routes = {
        <route_path_string>: <route_defenition>,
        ...
    }
    <route_defenition> is a dict with keys 'f','args' and 'kwargs', with the function name implementing the route along with
    corresponding args and kwargs as lists of strings.

    For example:
        routes = {
            '/api/health': {'f': health, 'args':[], 'kwargs':[]},
            ...
        }

Every custom function implementing the route must observe the following:
    1) All inputs parsed from the Request as function parametes that must be defined in the lists args and kwargs above;
    2) All returns should be a dict with the format {status:<status>, ...}:
        - <status> should be either 'OK' or 'ERROR'
        - If 'status':'OK' extra attributes may be present and will be sent to the client
        - If 'status':'ERROR', attribute 'error_msg' should be present, optionally along with 'error_code'
        - If status is not present, 'status':'OK' is automatically inserted;
        - If the return is not a dict, a dict is created with {'status':'OK', 'result':<return>}
        - If None is returned, a dict is created with only {'status':'OK'}
        Examples:
            return {'status':'ERROR', 'error_msg':'Error message', 'error_code':'Error code'} # Client gets what is returned
            return {'data':[arg1, kwarg1]} # Client gets {'status':'OK', 'data':[arg1, kwarg1]}
            return [1,2,3] # Client gets {'status':'OK', 'result':[1, 2, 3]}
            return None # Client gets {'status':'OK'}
            return {'status':'ERROR', 'error_msg':'Error message', 'error_code':'Error code'} # Client gets what is returned
    3) All normal returns are converted into HTTP responses with HTTP status 200 and the return data as JSON
    4) It is possible to raise an exception through log_and_raise_rest(msg), that is converted into an HTTP response
       with HTTP status defaulting to 500 and the error data
    5) If the function has an uncatched exception (bug), the App catches it and converts in the following response:
       {'status':'ERROR', 'error_type':'EXCEPTION', 'error_msg': <exception_details>} and then sent as an HTTP response
       with HTTP status 400 and the error data as JSON

Regarding files upload/downloand, consider the following:
    1) The route /api/get_signed_urls provide signed URLs for downnload/upload.
       The signed URLs can be obtained from the File Server or Google Cloud Storage.
       They are intended to offload the REST server of dealing with files, proxying to external services.
       The user namespace is limited to <bucket>.
    2) The routes /api/download_workfile and /api/upload_workfile provides downnload/upload functionality for
       registered users.
       User have isolated namespace under the workfiles namespace.

The remaing methods deal with jobs lifecycle and there is a method to register contact requests.

"""
from datetime import datetime, timezone
from operator import itemgetter
from pathlib import Path
from starlette.responses import FileResponse
from starlette.routing import Route
from starlette.authentication import requires
from dl2050utils.core import oget, LexIdx, get_uid, get_id
from dl2050utils.gs import GS
from dl2050utils.restutils import HTTPException, log_and_raise_exception, log_and_raise_rest, log_and_raise_service
from dl2050utils.restutils import rest_ok,enforce_required_args, get_optional_args, form_files_upload

class App():

    def __init__(self, cfg, LOG, NOTIFY, db, mq, auth, path, routes=[], appstartup=None, perm=None):
        self.service = cfg['service']
        self.path = path
        self.cfg,self.LOG,self.NOTIFY,self.db,self.mq,self.auth = cfg,LOG,NOTIFY,db,mq,auth
        self.routes,self.appstartup,self.perm = routes,appstartup,perm
        self.d = {'cfg':cfg, 'LOG':LOG, 'path':path, 'db':db, 'mq':mq}
        self.fs = GS(self.service) if oget(cfg,['gcloud','gs_key']) is not None else None
        # self.fs_url,self.fs_secret = oget(self.cfg,['fs','url']),oget(self.cfg,['fs','secret'])

    # ####################################################################################################
    # Helper methods
    # ####################################################################################################

    async def db_increase(self, tbl, k, kv, c, prefix=''):
        row = await self.db.select_one(tbl, {k:kv})
        if row is None or len(row)==0:
            log_and_raise_service(self.LOG, label='AUTH', label2=prefix, msg='DB increase error: select')
        row[c] += row[c]+1
        res = await self.db.update(tbl, k, row)
        if res:
            log_and_raise_service(self.LOG, label='AUTH', label2=prefix, msg='DB increase error: update')

    # ####################################################################################################
    # Internal methods: startup, shutdown, get_routes
    # ####################################################################################################

    async def startup(self):
        model,meta = oget(self.cfg,['app','model']),None
        # if model is not None: meta = await get_meta(self.path, self.db, model)
        # self.d['model'] = model
        # self.d['meta'] = meta
        self.d['meta'] = None
        if self.appstartup is None: return False
        return await self.appstartup(self.d)

    def shutdown(self):
        self.LOG(2, 0, label='APP', label2='shutdown', msg='OK')
        return False   

    def get_routes(self):
        BASE_ROUTES = [
            Route('/api/contact', endpoint=self.contact, methods=['POST']),
            Route('/api/get_meta', endpoint=self.get_meta, methods=['GET']),
            Route('/api/get_signed_urls', endpoint=self.get_signed_urls, methods=['POST']),
            Route('/api/download_workfile/{fname:path}', endpoint=self.download_workfile, methods=['GET']),
            Route('/api/upload_workfile/{fname:path}', endpoint=self.upload_workfile, methods=['POST']),
            Route('/api/publish_job', endpoint=self.publish_job, methods=['POST']),
            Route('/api/get_jobs', endpoint=self.get_jobs, methods=['POST']),
            Route('/api/get_job', endpoint=self.get_job, methods=['POST']),
            Route('/api/ulists_get', endpoint=self.ulists_get, methods=['POST']),
            Route('/api/ulists_insert', endpoint=self.ulists_insert, methods=['POST']),
            Route('/api/ulists_update', endpoint=self.ulists_update, methods=['POST']),
            Route('/api/ulists_delete', endpoint=self.ulists_delete, methods=['POST']),
        ]
        APP_ROUTES = [Route(e, endpoint=self.app_route, methods=['POST']) for e in self.routes]
        return BASE_ROUTES + APP_ROUTES
    
    # ####################################################################################################
    # REST methods for Apps
    # ####################################################################################################

    async def contact(self, request):
        """
        """
        data = await request.json()
        d = enforce_required_args(self.LOG, data, ['email','name','msg'], label='AUTH', label2='check_user')
        d['ts'] = datetime.now(timezone.utc)
        err = await self.db.insert('contacts', d)
        if err:
            log_and_raise_service(self.LOG, label='REST', label2='contact', msg='DB access error')
        html = '<h1>Name</h1><p>{d["email"]</p><h1>Email</h1><p>{d["email"]</p><h1>Message</h1><p>{d["msg"]</p>}'
        self.notify.send_mail_async(d['email'], subject='Contact from Website (cardiolife.global)', html=html)
        return rest_ok()

    @requires('authenticated')
    async def get_meta(self, request):
        """Returns the meta information."""
        return rest_ok(self.d['meta'])
    
    @requires('authenticated')
    async def get_signed_urls(self, request):
        """
        Provides signed urls for every path defined in the files parameter.
        Keep the files tree structure on the File Server.
        All paths will have the same uid prefix. A new uid is allways generated on this request.
        Returns dict with two lists, the upload_urls and download_urls.
        """
        if self.fs is None:
            log_and_raise_service(self.LOG, label='REST', label2='download_req', msg='Signed urls not available')
        data = await request.json()
        # files = get_param(request, 'files', list, data=data, LOG=self.LOG)
        args = enforce_required_args(self.LOG, data, ['files'], label='REST', label2='get_signed_urls')
        files = args['files']
        uid = get_uid()
        upload_urls,download_urls = [],[]
        bucket = f'{self.service}-apiserver'
        for file in files:
            upload_url,download_url = self.fs.urls(bucket, f'{uid}/{file}')
            if upload_url is None or download_url is None:
                log_and_raise_service(self.LOG, label='REST', label2='get_signed_urls', msg='Signed urls not available')
            upload_urls.append(upload_url),download_urls.append(download_url)
        return rest_ok({'upload_urls':upload_urls, 'download_urls':download_urls})

    @requires('authenticated')
    async def download_workfile(self, request):
        """
            Downloads a workfile file fname belonging to a registered user.
            Workfiles are usually results produced by workers (throught MQ).
            Workfiles are stored in the folder '$DATAPATH/workfiles/<service>.
        """
        u = await self.auth.check_auth(request)
        uid = u['uid']
        fname = request.path_params['fname']
        p = Path(f'/data/{self.service}/workfiles/{fname}')
        if not p.is_file():
            log_and_raise_service(self.LOG, label='REST', label2='download_workfile', msg=f'File not found: {str(p)}')
        return FileResponse(str(p), media_type='application/vnd.ms-excel', filename=str(p))

    @requires('authenticated')
    async def upload_workfile(self, request):
        """
            Uploads a workfile file fname belonging to a registered user.
            Workfiles for upload are usually content produced by the users.
            Workfiles are stored in the folder '$DATAPATH/workfiles/<service>'.
        """
        u = await self.auth.check_auth(request)
        uid = u['uid']
        fname = request.path_params['fname']
        p = Path(f'/data/{self.service}/workfiles/{fname}')
        max_size = int(1e9)
        form = await request.form()
        if form is None:
            log_and_raise_service(self.LOG, label='REST', label2='upload_workfile', msg=f'Upload form error')
        await form_files_upload(self.LOG, form.items(), p, max_size=max_size)
        return rest_ok()

    @requires('authenticated')
    async def publish_job(self, request):
        """
            Publishes a new job, calling mq.publish after checking permissions.
            Jobs require the user email as an attribute.
        """
        u = await self.auth.check_auth(request)
        uid = u['uid']
        email = await self.auth.get_email_from_uid(uid)
        data = await request.json()
        args = enforce_required_args(self.LOG, data, ['q','payload'], label='REST', label2='publish_job')
        q,payload = args['q'],args['payload']
        self.perm(self.d, u, request.url.path, args)
        jid = await self.mq.publish(q, email, payload)
        if jid is None :
            log_and_raise_service(self.LOG, label='REST', label2='publish_job', msg='MQ publish error')
        self.LOG(2, 0, label='APP', label2='publish_job')
        return rest_ok({'jid': jid})

    @requires('authenticated')
    async def get_jobs(self, request):
        """Gets all jobs from a user, optionaly filtered by qname, pending or jobs not done."""
        u = await self.auth.check_auth(request)
        uid = u['uid']
        email = await self.auth.get_email_from_uid(uid)
        data = await request.json()
        kwargs = get_optional_args(data, ['qname','pending','not_done'])
        jobs = await self.mq.get_jobs(email, **kwargs)
        return rest_ok(jobs)

    @requires('authenticated')
    async def get_job(self, request):
        """Gets a job details, identified by jid."""
        u = await self.auth.check_auth(request)
        data = await request.json()
        args = enforce_required_args(self.LOG, data, ['jid'], label='REST', label2='get_job')
        job = await self.mq.get_job(args['jid'])
        return rest_ok(job)
    
    @requires('authenticated')
    async def ulists_get(self, request):
        """Gets the whole ulist, with 1024 limit."""
        label2 = 'ulists_get'
        u = await self.auth.check_auth(request)
        email = await self.auth.get_email_from_uid(u['uid'])
        data = await request.json()
        args = enforce_required_args(self.LOG, data, ['ulist'], label='REST', label2=label2)
        ulist = itemgetter('ulist')(args)
        res = await self.db.select('ulists', filters={'email':email,'ulist':ulist}, sort='lexseq', limit=1024)
        data = oget(res,['data'])
        return rest_ok(data)
    
    @requires('authenticated')
    async def ulists_insert(self, request):
        """Inserts new ulists record the whole ulist"""
        label2 = 'ulist_insert'
        u = await self.auth.check_auth(request)
        email = await self.auth.get_email_from_uid(u['uid'])
        data = await request.json()
        args = enforce_required_args(self.LOG, data, ['ulist'], label='REST', label2=label2)
        kwargs = get_optional_args(data, ['id', 'tag', 'val', 'id1', 'id2'])
        ulist = itemgetter('ulist')(args)
        id_ = oget(kwargs,['id']) or get_id()
        d = {'email':email, 'ulist':ulist, 'id':id_, 'tag':oget(kwargs,['tag']), 'val':oget(kwargs,['val'])}
        id1,id2 = oget(kwargs,['id1']),oget(kwargs,['id2'])
        # If being inserted in the last position, checks db and set a new max
        l = LexIdx()
        if id2 is None:
            seq = await self.db.query(f"select max(lexseq) from ulists where email='{email}' and ulist='{ulist}'")
            lseq = l.next(oget(seq,[0,'max']))
        # Otherwise interpolates
        else:
            lseq = l.interpolate(id1, id2)
        d['lexseq'] = lseq
        await self.db.insert('ulists', d)
        return rest_ok()

    @requires('authenticated')
    async def ulists_update(self, request):
        """Gets the whole ulist, with 1024 limit."""
        label2 = 'ulist_update'
        u = await self.auth.check_auth(request)
        email = await self.auth.get_email_from_uid(u['uid'])
        data = await request.json()
        args = enforce_required_args(self.LOG, data, ['ulist', 'id'], label='REST', label2=label2)
        kwargs = get_optional_args(data, ['tag', 'val', 'id1', 'id2'])
        ulist,id_ = itemgetter('ulist','id')(args)
        d = {'email':email, 'ulist':ulist, 'id':id_, 'tag':oget(kwargs,['tag']), 'val':oget(kwargs,['val'])}
        id1,id2 = oget(kwargs,['id1']),oget(kwargs,['id2'])
        if id1 is not None or id2 is not None:
            l = LexIdx()
            if id2 is None:
                seq = await self.db.query(f"select max(lexseq) from ulists where email='{email}' and ulist='{ulist}'")
                lseq = l.next(oget(seq,[0,'max']))
            else:
                lseq = l.interpolate(id1, id2)
            d['lexseq'] = lseq
        await self.db.update('ulists', ['email', 'ulist', 'id'], d)
        return rest_ok()
    
    @requires('authenticated')
    async def ulists_delete(self, request):
        """Gets the whole ulist, with 1024 limit."""
        label2 = 'ulist_delete'
        u = await self.auth.check_auth(request)
        email = await self.auth.get_email_from_uid(u['uid'])
        data = await request.json()
        args = enforce_required_args(self.LOG, data, ['ulist', 'id'], label='REST', label2=label2)
        ulist,id_ = itemgetter('ulist','id')(args)
        await self.db.query(f"delete from ulists where email={email} and ulist='{ulist}' and id='{id_}'")
        return rest_ok()

    @requires('authenticated')
    async def app_route(self, request):
        """Implements all the custom app routes."""
        label2 = f'app_route {request.url.path}'
        if request.url.path not in self.routes:
            log_and_raise_rest(self.LOG, label='REST', label2=label2, msg='url path not found', status_code=400)
        d = self.routes[request.url.path]
        cb,args,kwargs = d['f'],d['args'],d['kwargs']
        u = await self.auth.check_auth(request)
        data = await request.json()
        args2 = enforce_required_args(self.LOG, data, args, label='REST', label2=label2)
        kwargs2 = get_optional_args(data, kwargs)
        self.perm(self.d, u, request.url.path, {**args2, **kwargs2})
        try:
            res = await cb(self.d, u, *[args2[e] for e in args2], **kwargs2)
        except HTTPException as exc:
            raise
        except Exception as exc:
            log_and_raise_exception(self.LOG, label='REST', label2=label2, msg=str(exc))
        return rest_ok(res)
