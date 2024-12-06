"""
    mq.py

    Class MQ to manage jobs.
    Jobs are used to coordinate cooperation between services through message queues, with client and server roles.
    MQ can be run as a server or used as client to request jobs.

    The server() method waits for incoming job request on the Queue qname forever.
    For every request for that Queue a callback is called.
    The call back ha 3 parameters: the mq object, the job id and the received payload.

    The publish method requests a new job, passing the qname, email and payload.

    Jobs lifecycle are stored on in the jobs db tables. All jobs have an id (jid) a owner (email).
    The lifecycle can be managed both by the MQ server and the callback.
    Lifecycle methods include: job_start, job_update_eta, job_done, job_error.
"""
import asyncio
import logging
import time
from datetime import datetime
import uuid
import json
import pika
from aio_pika import connect_robust, Message, DeliveryMode
from dl2050utils.core import oget, listify

JOB_CREATE = 0
JOB_START = 1
JOB_DONE = 2
JOB_ERROR = 99

# ########################################################################################################################
# Helper functions
# ########################################################################################################################

async def async_job_select(LOG, db, jid=None, qname=None, email=None, pending=False, not_done=False,):
    if jid is None and email is None:
        return None
    if jid is not None:
        return await db.select_one('jobs', {'jid':jid})
    d = [{'col':'email', 'val':email}]
    if qname is not None:
        d.append({'col':'qname', 'val':qname})
    if pending:
        d.append({'col':'jstatus', 'val':2, 'op':'<'})
    elif not_done:
        d.append({'col':'jstatus', 'val':JOB_DONE, 'op':'!='})
    res = await db.select('jobs', filters=d, sort='ts_create', ascending=False)
    return listify(oget(res,['data']))

def get_job_d(jid, status=None, eta=None, result=None):
    d = {'jid':jid}
    if status is not None:
        d['jstatus'] = status
        if status==JOB_START: d['ts_start'] = datetime.now()
        if status==JOB_DONE: d['ts_done'] = datetime.now()
    if eta is not None: d['eta']=eta
    if result is not None and type(result)==dict: d['result']=result
    return d

async def async_job_update(LOG, db, jid, status=None, eta=None, result=None):
    d = get_job_d(jid, status=status, eta=eta, result=result)
    LOG(1, 0, label='MQ', label2='job_update', msg=d)
    return await db.update('jobs', 'jid', d)

def sync_job_update(LOG, db, jid, status=None, eta=None, result=None):
    d = get_job_d(jid, status=status, eta=eta, result=result)
    LOG(1, 0, label='MQ', label2='job_update', msg=d)
    return db.sync_update('jobs', 'jid', d)

# ########################################################################################################################
# MQ Client
# ########################################################################################################################

class MQ():
    def __init__(self, log, db, qnames, cfg):
        self.LOG,self.db,self.qnames = log,db,listify(qnames)
        user = oget(cfg, ['mq','user'], 'admin')
        passwd = oget(cfg, ['mq','passwd'], 'password')
        self.url = f'amqp://{user}:{passwd}@mq:5672?heartbeat=1800'

    async def startup(self, loop=None):
        try:
            con = await connect_robust(self.url, loop=loop)
            ch = await con.channel()
            for qname in self.qnames:
                await ch.declare_queue(qname, durable=True, auto_delete=False)
            await con.close()
        except Exception as exc:
            self.LOG(4, 0, label='MQ', label2='connect', msg=str(exc))
            return True
        self.LOG(2, 0, label='MQ', label2='STARTUP', msg='OK')
        return False
    
    # def sync_startup(self, *args, **kwargs):
    #     return asyncio.get_event_loop().run_until_complete(self.startup(*args, **kwargs))
    
    async def publish(self, qname, email, payload):
        """
            Publishes a new message to the queue qname.
            Returns the qid or None if error
        """
        jid = str(uuid.uuid4())
        d = {
            'jid':jid,
            'email':email,
            'qname':qname,
            'payload':payload,
            'jstatus':JOB_CREATE,
            'eta':0,
            'ts_create':datetime.now()
        }
        err = await self.db.insert('jobs', d)
        if err:
            self.LOG(4, 0, label='MQ', label2='publish', msg=f'DB: failed to insert job: {err}')
            return None
        payload['email'],payload['jid'] = email,str(jid)
        msg = Message(body=json.dumps(payload).encode(), delivery_mode=DeliveryMode.PERSISTENT)
        try:
            loop = asyncio.get_event_loop()
            con = await connect_robust(self.url, loop=loop)
            ch = await con.channel()
            await ch.default_exchange.publish(msg, routing_key=qname)
            await con.close()
        except Exception as e:
            self.LOG(4, 0, label='MQ', label2='publish', msg=str(e))
            return None
        return str(jid)

    async def get_jobs(self, email, qname=None, pending=False, not_done=False):
        return await async_job_select(self.LOG, self.db, email=email, qname=qname, pending=pending, not_done=not_done)
    async def get_job(self, jid):
        return await async_job_select(self.LOG, self.db, jid=jid)
    async def job_start(self, jid, eta=None):
        return await async_job_update(self.LOG, self.db, jid, status=JOB_START, eta=eta)
    async def job_update_eta(self, jid, eta):
        return await async_job_update(self.LOG, self.db, jid, eta=eta)
    async def job_done(self, jid, result=None):
        return await async_job_update(self.LOG, self.db, jid, status=JOB_DONE, result=result)
    async def job_error(self, jid):
        return await async_job_update(self.LOG, self.db, jid, status=JOB_ERROR, eta=0)

# ########################################################################################################################
# MQServer
# ########################################################################################################################

class MQServer():
    def __init__(self, log, db, cfg):
        self.LOG,self.db,self.cfg = log,db,cfg
        user,passwd = oget(self.cfg, ['mq','user'], 'admin'),oget(self.cfg, ['mq','passwd'], 'password')
        self.url = f'amqp://{user}:{passwd}@mq:5672?heartbeat=1800'
        logging.getLogger('pika').setLevel(logging.CRITICAL)

    def run(self, qname, cb):
        def callback(ch, method, properties, body):
            payload = json.loads(body.decode())
            jid = payload['jid']
            # ch.basic_ack(delivery_tag=method.delivery_tag)
            self.job_start(jid)
            if cb(self, jid, payload):
                self.job_error(jid)
                return
            self.job_done(jid)
        self.LOG(2, 0, label='MQServer', label2='STARTUP', msg=f'Starting')
        # Wait for MQ to start before trying to connect
        time.sleep(5)
        con = pika.BlockingConnection(pika.connection.URLParameters(self.url))  # log_level='critical'
        ch = con.channel()
        ch.queue_declare(queue=qname, durable=True, exclusive=False, auto_delete=False)
        ch.basic_qos(prefetch_count=1)
        ch.basic_consume(queue=qname, auto_ack=True, on_message_callback=callback)
        self.LOG(2, 0, label='MQServer', label2='RUN', msg=f'Running')
        try:
            ch.start_consuming()
        except Exception as exc:
            self.LOG(4, 0, label='MQServer', label2='STARTUP EXCEPTION', msg=str(exc))
        ch.stop_consuming()
        con.close()
        exit(1)

    def job_start(self, jid, eta=None): return sync_job_update(self.LOG, self.db, jid, status=JOB_START, eta=eta)
    def job_update_eta(self, jid, eta): return sync_job_update(self.LOG, self.db, jid, eta=eta)
    def job_done(self, jid, result=None): return sync_job_update(self.LOG, self.db, jid, status=JOB_DONE, result=result)
    def job_error(self, jid): return sync_job_update(self.LOG, self.db, jid, status=JOB_ERROR)
