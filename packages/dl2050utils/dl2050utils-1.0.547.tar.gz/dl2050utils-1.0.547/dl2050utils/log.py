import datetime
import logging
from dl2050utils.core import oget

# LOG_FORMAT = '\
# %(name)s  %(levelname)s - %(asctime)s - %(product)s:%(client)s:%(instance)s:%(service)s - \
# %(label)s - %(label2)s - %(duration).3f - %(message)s'
LOG_FORMAT = '%(service)s  %(levelname)s - %(asctime)s - %(duration).3f - %(label)s - %(label2)s - %(message)s'

# ################################################################################
# AppLog class
# ################################################################################

def parse_msg(d):
    if d is None: return 'null'
    if type(d) in [int, float]: return str(d)
    if isinstance(d, str): return d.replace('\n', ' ')
    if isinstance(d, datetime.datetime): return d.strftime("%Y-%m-%Y %H:%M:%S")
    if type(d) is list: return f'[#{len(d)}]'
    if type(d) is not dict: return f'OBJECT-{type(d)}'
    s = '{'
    for key, val in d.items():
        if isinstance(d[key], dict):
            s += f'{key}:'+'{...}'
        elif type(d[key]) is list:
            s += f'{key}:[#{len(d)}]'
        else:
            s += f'{key}:{val}'
        s += ', '
    return s[:-2]+'}'

class AppLog():
    """
        Logs server messages.
        Includes attributs Product, Client, Instance and Service.
        Assumes 5 different log levels: Debug, Info, Warning, Error, Critical.
        Accepts any message and diggests lists/dicts to show only their lenght/keys.
    """
    def __init__(self, cfg, service='rest'):
        global loggers
        self.msg_prefix = {
            # 'product': oget(cfg, ['app','product'], '_PRODUCT_'),
            # 'client': oget(cfg, ['app','client'], '_CLIENT_'),
            # 'instance': oget(cfg, ['app','instance'], '_INSTANCE_'),
            'service': service,
        }
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger('APPLOG')
        logger.propagate = False
        while len(logger.handlers):
            logger.removeHandler(logger.handlers[0])
        streamHandler = logging.StreamHandler()
        streamHandler.setLevel(logging.INFO)
        formatter = logging.Formatter(LOG_FORMAT)
        streamHandler.setFormatter(formatter)
        logger.addHandler(streamHandler)
        self.LOG_LEVELS = {
            1: logger.debug,
            2: logger.info,
            3: logger.warning,
            4: logger.error,
            5: logger.critical
        }
        
    def __call__(self, level=3, t=None, label=None, label2=None, msg=''):
        if not isinstance(level, int) or level<1 or level>5: return
        log_f = self.LOG_LEVELS[level]
        log_msg = self.msg_prefix
        log_msg['label'],log_msg['label2'],log_msg['duration'] = label or '',label2 or '',t or 0
        s = parse_msg(msg)
        log_f(s, extra=log_msg)

# ################################################################################
# BaseLog class
# ################################################################################

class BaseLog():
    """ Basic log class that just prints to screen or file"""
    def __init__(self, p=None, service=''):
        self.p,self.service = p,service
    def __call__(self, level, t, label='', label2='', msg=''):
        dt = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S')
        if level<1 or level>4: return
        LEVELS = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        msg = f'{dt} {LEVELS[level-1]} {t} {self.service} {label} {label2} {msg}'
        print(msg)
        msg += '\n'
        if self.p:
            with open(self.p, 'a') as f:
                f.write(msg)
                f.flush()
