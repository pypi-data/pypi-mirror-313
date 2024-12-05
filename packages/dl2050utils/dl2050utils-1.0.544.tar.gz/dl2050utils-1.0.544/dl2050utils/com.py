import re
import socket
import json
import base64
from multiprocessing import Process
import mimetypes
mimetypes.init()
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (Mail, Attachment, FileContent, FileName, FileType, Disposition)
from twilio.rest import Client
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dl2050utils.core import *

# ####################################################################################################
# com Module
#
# Send email notifications with Sendgrid and phone text notifications with Twillio
#
# Main parts:
#     1) read_address_books: very basic address book management
#     2) Notify: class to manage all communication features
#     3) send_otp: send OTP codes by email or phone (helper function for auth Module)
#
# ####################################################################################################

# ####################################################################################################
# Address book
# ####################################################################################################

default_address_book = {
    'jneto': {'email': 'joao.filipe.neto@gmail.com', 'phone': '+351966221506'},
    'pneto': {'email': 'pneto.98@gmail.com', 'phone': '+351910528813'},
    'jranito': {'email': 'joao.vasco.ranito@gmail.com', 'phone': '+351966221505'},
    'rassuncao': {'email': 'rui.assuncao@ndrive.com ', 'phone': '+351933339307'}
}

def read_address_book():
    try:
        with open('./.addressbook') as f: d = json.loads(f.read())
    except IOError:
        return None
    return d

# ####################################################################################################
# Notify
# ####################################################################################################

def send_email_sendgrid(api_key, to, subject=None, msg=None, html=None, files=[]):
    """ Send email by SendGrid service, optionaly with files. """
    if api_key is None: return 'send_email_sendgrid: email api_key not defined'
    to = listify(to)
    if not len(to): return 'send_email_sendgrid: no destination addresses'
    try:
        msg = msg or '   '
        html2 = html or msg
        subject = subject or '  '
        msg = Mail(from_email='ops@dl2050.com', to_emails=to, subject=subject, html_content=html2)
        if len(files):
            attachments = []
            for file in files:
                with open(str(file), 'rb') as f: data=f.read()
                data = base64.b64encode(data).decode()
                attachedFile = Attachment(
                    FileContent(data),
                    FileName(file.name),
                    FileType(mimetypes.types_map[file.suffix]),
                    Disposition('attachment')
                )
                attachments.append(attachedFile)
            msg.attachment = attachments
        sg = SendGridAPIClient(api_key)
        res = sg.send(msg)
    except Exception as e:
        return f'send_email_sendgrid EXCEPTION: {str(e)}'
    if res.status_code!=202: return f'SendGrid ERROR: status code={res.status_code}'
    return None

def send_email_async_sendgrid(api_key, to, subject=None, msg=None, html=None, files=[]):
    """ Asyncronous version send_email_sendgrid implmented with subprocesses. """
    if api_key is None: return 'send_email_async_sendgrid: email api_key not defined'
    to = listify(to)
    if not len(to): return 'send_email_async_sendgrid: no destination addresses'
    p = Process(target=send_email_sendgrid, args=(api_key, to, subject, msg, html, files), daemon=True)
    p.start()

def send_sms_twilio(account_sid, auth_token, service_name, to, msg):
    """ Send email by Twilio service, optionaly with files. """
    if account_sid is None: return 'send_sms_twilio: account_sid not defined'
    if auth_token is None: return 'send_sms_twilio: auth_token not defined'
    if not len(to): return 'send_sms_twilio: no destination addresses'
    to = listify(to)
    try:
        client = Client(account_sid, auth_token)
        for e in to:
            res = client.messages.create(body=msg, from_=service_name, to=e)
        return None
    except Exception as e:
        return f'send_sms_twilio: EXCEPTION: {str(e)}'


def send_slack(token, channel, msg, files=None):
    """
        Send slack messages, optionally with files.
        Files require files_upload_v2 that currently depends on channel_id insteas of channel_name
        (Channel ID is displayed on the bottom of the Panel configuration (needed for v2)
        The Slack APP is identified by the tokem.
        The Slack APP must have the follwing scopes:
            app_mentions:read,chat:write,channels:history,channels:join,channels:read,chat:write.public,
            incoming-webhook,files:write'
    """
    slack_channel_name_to_id = {
        'priceware-devops':'C05ATJLRBSQ',
        'report-offers':'C060HFE1894',
        'report-deco': 'C061SPKDKDK',
        'report-system': 'C061Y51J8BW'
    }
    if token is None: return 'send_slack: token key not defined'
    if not channel: return 'send_slack: missing channel'
    if files==[]: files = None
    if files is not None:
        files = listify(files)
        files = [{'file': str(e)} for e in files]
    try:
        client = WebClient(token=token)
        if files is None:
            res = client.chat_postMessage(channel=channel, text=msg)
        else:
            channel = slack_channel_name_to_id[channel]
            res = client.files_upload_v2(channel=channel, file_uploads=files, initial_comment=msg)
        if res['ok']:
            return None
        else:
            return f'send_slack: send error'
    except Exception as exc:
        return f'send_slack EXCEPTION: {exc}'

class Notify():
    """
        Agregator of all notification machanisms, dispatches to different services.
        Available services are:
            email: thought sendgrid
            email_async: thought sendgrid executed on a subprocess
            sms: thought twilio
            slack
    """
    def __init__(self, cfg, address_book=None):
        if cfg is None: raise Exception('Notify: cfg not defined')
        self.address_book = address_book if address_book is not None else default_address_book
        self.email_key = oget(cfg,['email','sendgrid_api_key'])
        self.sms_id = oget(cfg,['twilio','account_sid'])
        self.sms_passwd = oget(cfg,['twilio','auth_token'])
        self.sms_service_name = oget(cfg,['twilio','service_name'])
        self.slack_token = oget(cfg,['slack','token'])
        
    def __call__(self, how, to=None, subject=None, channel=None, msg=None, html=None, files=[]):
        if how == 'email':
            return self.send_email(to, subject=subject, msg=msg, html=html, files=files)
        elif how == 'email_async':
            return self.send_email_async(to, subject=subject, msg=msg, html=html, files=files)
        elif how=='sms':
            return self.send_sms(to, msg)
        elif how=='slack':
            return self.send_slack(channel, msg, files=files)
        else:
            raise Exception('Invalid method, options are email, email_async, sms or slack')
        
    def send_email(self, to, subject=None, msg=None, html=None, files=[]):
        to = listify(to)
        to = [self.address_book[e]['email'] if e in self.address_book else e for e in to]
        return send_email_sendgrid(self.email_key, to, subject=subject, msg=msg, html=html, files=files)
    
    def send_email_async(self, to, subject=None, msg=None, html=None, files=[]):
        to = listify(to)
        to = [self.address_book[e]['email'] if e in self.address_book else e for e in to]
        send_email_async_sendgrid(self.email_key, to, subject=subject, msg=msg, html=html, files=files)
    
    def send_sms(self, to, msg):
        return send_sms_twilio(self.sms_id, self.sms_passwd, self.sms_service_name, to, msg)
    
    def send_slack(self, channel, msg, files=None):
        return send_slack(self.slack_token, channel, msg, files=files)

# ####################################################################################################
# Send OTP
# ####################################################################################################

EMAIL_TEMPLATE = \
"""
<html>
<head>
    <link href="https://fonts.googleapis.com/css?family=Muli::100,200,300,400,500,600,700,800" rel="stylesheet">
</head>
    <body style="position: relative; float: left; width: 100%; height: 100%;  text-align: center; font-family: 'Muli', sans-serif;">
        <h2 style="float: left; width: 100%; margin: 40px 0px 10px 0px; font-size: 16px; text-align: center; color: #555555;">{msg}</h2>
        <h2 style="float: left; width: 100%; margin: 0px 0px 40px 0px; font-size: 24px; text-align: center; color: #61C0DF; font-weight: bold;">{otp}</h2>
    </body>
</html>
"""

def send_otp_by_email(notify, product, email, otp):
    """ Sends One Time Password (OTP) by email. Relies on simpleEMAIL_TEMPLATE. """
    try:
        subject = f'{product} OTP'
        msg = f'{product} OTP: '
        html = EMAIL_TEMPLATE
        html = re.sub(r'{msg}', msg, html)
        html = re.sub(r'{otp}', f'{otp}', html)
        notify.send_email_async(email, subject=subject, html=html)
    except Exception as e:
        return str(e)
    return None

def send_otp_by_phone(notify, product, phone, otp):
    """ Sends One Time Password (OTP) by sms. """
    msg = f'{product} OTP: {otp}'
    try:
        notify.send_sms(phone, msg)
    except Exception as e:
        return str(e)
    return None

def send_otp(notify, mode, product, email, phone, otp):
    """ Dispatches One Time Password (OTP) to the service defined in mode. """
    if mode=='phone': return send_otp_by_phone(notify, product, phone, otp)
    return send_otp_by_email(notify, product, email, otp)

# ####################################################################################################
# etc
# ####################################################################################################

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

