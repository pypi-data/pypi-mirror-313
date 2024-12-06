from typing import *
import traceback
import re
import random
import string
import datetime
from zoneinfo import ZoneInfo
import base64
from collections import OrderedDict
from collections.abc import Iterable, Generator
from concurrent.futures import ProcessPoolExecutor, as_completed
import numpy as np
from tqdm.notebook import tqdm

# ################################################################################
# Basic functions
# ################################################################################

def A(a=None):
    if a is None: return np.array([]).astype(np.int32)
    a = np.array(a)
    if a.dtype=='int64': return a.astype(np.int32)
    if a.dtype=='flot64': return a.astype(np.float32)
    return a

def Z(n): return np.zeros(n).astype(np.int32)
def W(a): return np.where(a)[0]

def is_numeric_str(e):
    if type(e)!=str: return False
    return e.lstrip('-+').replace('.','',1).isdigit()

def is_iter(o):
    return isinstance(o, (Iterable,Generator)) and getattr(o,'ndim',1)

def is_array(x):
    return hasattr(x,'__array__') or hasattr(x,'iloc')

def lol_to_l(lol):
    return [e for l in lol for e in l]

def try_call(f, args=[], kwargs={}, LOG=None, label='', label2='', debug=False):
    try:
        return f(*args, **kwargs)
    except Exception as exc:
        if LOG is not None:
            if debug:
                LOG(4, 0, label=label, label2='EXCEPTION',
                    msg={'EXCEPTION':str(exc),'TRACEBACK':traceback.format_exc()})
            else:
                LOG(4, 0, label=label, label2=f'{label2} EXCEPTION', msg=str(exc))
        return -1
    
# ################################################################################
# Dates
# ################################################################################
    
def now(s=False):
    d = datetime.datetime.now(datetime.timezone.utc)
    if s: d = d.strftime('%Y%m%d%H%M%S%f')
    return d

def date_to_srt(dt):
    """Converts timezone-aware datetime to ISO-8601 string"""
    if dt is None: return None
    return dt.isoformat()

def str_to_date(s):
    """Converts ISO-8601 string to a timezone-aware datetime object"""
    if s is None: return None
    if isinstance(s, bytes): s = s.decode('utf-8')
    dt = datetime.datetime.fromisoformat(s)
    # Assign the UTC timezone if it's naive datetime object
    if dt.tzinfo is None: dt = dt.replace(tzinfo=ZoneInfo('UTC'))
    return dt

# def str_to_date_2(s):
#     if s is None: return None
#     dt = datetime.datetime.fromisoformat(s)
#     return dt.replace(tzinfo=ZoneInfo('UTC'))

# ################################################################################
# Strings
# ################################################################################

def strip_string(s):
    """Returns input string striped of all the leading/trailing/repeated spacing chars including \t and \n."""
    return re.sub(r'\s+', ' ', s).strip()

# ################################################################################
# base64
# base64_chars = string.ascii_uppercase + string.ascii_lowercase + string.digits + "+/"
# base64padding_char = "="
# data = 'content'
# enc = base64_encode(data)
# dec = base64_decode(enc, return_as_text=True)
# data2 = base64_decode(enc, return_as_text=False)
# assert data2==data
# ################################################################################

def base64_encode(data):
    """
    Base64 encode data, that can be either a binary blob (bytes) or a string.
    Returns the base64-encoded string of the input data.
    """
    # If data is a string, convert it to bytes
    if isinstance(data, str): data = data.encode('utf-8')
    # Base64 encode the bytes
    return base64.b64encode(data).decode('utf-8')

def base64_decode(encoded_data, return_as_text=True):
    """
    Base64 decode the base64-encoded encoded_data back to its original form.
    If return_as_text is True, tryis to decode as a UTF-8 string.
    Otherwise, return as bytes.
    """
    # Decode the base64 string back to bytes
    try:
        decoded_data = base64.b64decode(encoded_data)
    except:
        return None
    # If return_as_text is True, convert bytes back to string
    if return_as_text:
        try:
            return decoded_data.decode('utf-8')
        except UnicodeDecodeError:
            pass
    # Return bytes
    return decoded_data

# ################################################################################
# get_uid, get_id
# ################################################################################

def get_uid():
    """
    Format is YYYYMMDDHHMMSSUUUUUURRRRRRRRRRRR. U is microsecond. R is random letter.
    There are 26^12 different possible values per microsecond (~95 trillion).
    """
    now = datetime.datetime.now(datetime.timezone.utc)
    timestamp = now.strftime('%Y%m%d%H%M%S%f')
    suffix = ''.join(random.choices(string.ascii_uppercase, k=12))
    return f'{timestamp}{suffix}'

def get_id(n=6):
    """Returns a random id composed by base64 chars with size n. For n=6 there are 68 billion options."""
    return ''.join(random.choices(string.ascii_letters + string.digits + '+/', k=n))

# ################################################################################
# checks
# checks input formats and limits the input size
# usefull for input passed as requests payload to avoid too large data
# ################################################################################

def check_float(e):
    if type(e) not in [str, int, float]: return None
    s = str(e)[:32]
    if is_numeric_str(s):
        return float(s)
    return None

def check_int(e):
    f = check_float(e)
    if f is None:
        return None
    return int(f)

def check_str(e, n=1024):
    if type(e) not in [str, int, float]: return None
    return str(e)[:n]

def check(e, n=1024):
    """
        Check input and accept only int, float or bool
        Limit input size to n if string
    """
    if type(e) in [int, float, bool]:
        return e
    if type(e)==str:
        return str(e)[:n]
    return None

# ################################################################################
# listify
# ################################################################################

def listify(o):
    """ Transforms input into a list. """
    if o is None: return []
    if isinstance(o, list) or is_array(o): return o
    if type(o)==np.ndarray: return list(o)
    if isinstance(o, str): return [o]
    if isinstance(o, dict): return [o]
    if is_iter(o): return list(o)
    return [o]

# ################################################################################
# oget
# ################################################################################

def oget(o, fs, default_=None):
    """
        Extracts a deeper subelement of a dict base on a list of hierarchical attributes.
        Sub-elements may be dicts or lists.
    """
    if o is None or fs is None: return default_
    for f in listify(fs):
        if type(o)==dict and f in o: o = o[f]
        elif type(o)==list and (type(f)==int or np.issubdtype(f, np.integer)) and f<len(o): o = o[f]
        else: return default_
    if o is None: return default_
    return o

# ################################################################################
# re
# ################################################################################

def xre(r, s):
    """
        Returns regex pattern in string if found, otherwise None.
        Example: r = xre('(DS_Store)',str(s))
    """
    if type(r)!=str or type(s)!=str: return None
    m = re.search(r, s)
    return m.group(1) if m else None

# ################################################################################
# LRUCache
# ################################################################################

class LRUCache:
    def __init__(self, size):
        self.size,self.cache = size,OrderedDict()

    def get(self, key, load_callback=None, **kwargs):
        if key in self.cache:
            value = self.cache.pop(key)
            self.cache[key] = value
            return value
        elif load_callback is not None:
            value = load_callback(key, **kwargs)
            self.put(key, value)
            return value
        else:
            return -1
        
    async def get_async(self, key, load_callback=None, **kwargs):
        if key in self.cache:
            value = self.cache.pop(key)
            self.cache[key] = value
            return value
        elif load_callback is not None:
            value = await load_callback(key, **kwargs)
            self.put(key, value)
            return value
        else:
            return -1
            
    def put(self, key, value):
        if key in self.cache:
            self.cache.pop(key)
        elif len(self.cache) >= self.size:
            self.cache.popitem(last=False)
        self.cache[key] = value

# ################################################################################
# parallel
# ################################################################################

def parallel(f, a, nprocs=16):
    """
    Apply function f to array a, splitting the process through nprocs parallel processes.
    Splits the array a into nprocs chunks.
    Returns the combined results for all processes.
    Important Considerations:
        Global Variables: Each process has its own memory space; changes in one process don't affect the others.
        Pickling: Function f and input arguments must be pickleable.
        Performance: The overhead of creating and managing multiple processes can affect performance for very small tasks.
    """
    # Split a into nprocs chunks
    chunks = np.array_split(a, nprocs)
    chunk_sz = len(chunks[0])
    results = []
    # Use ProcessPoolExecutor for parallel processing
    with ProcessPoolExecutor(max_workers=nprocs) as executor:
        # Submit all tasks
        # future_to_chunk = {executor.submit(f, chunk): chunk for chunk in chunks}
        future_to_chunk = {executor.submit(f,chunk,i*chunk_sz): (chunk,i) for i,chunk in enumerate(chunks)}
        # Process results as they complete
        for future in as_completed(future_to_chunk):
            chunk = future_to_chunk[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as exc:
                print(f'Chunk with {len(chunk)} elements generated an exception: {exc}')
    return results

# ################################################################################
# LexIdx
# ################################################################################
        
class LexIdx():
    """
    LexIdx provides a system for managing lexicographically ordered sequences
    (lexseqs) with numeric prefixes and optional string suffixes. It supports
    encoding, decoding, and interpolation while maintaining lexical order.
    """
    def __init__(self, sz=6, max_sz=6):
        # List of sortable characters (a-z)
        self.sort_chars = [chr(i) for i in range(97, 123)]
        # Map each character to its index for quick conversion
        self.sort_map = {self.sort_chars[i]: i for i, e in enumerate(self.sort_chars)}
        # Base is the number of sortable characters
        self.base = len(self.sort_chars)
        # Prefix size and suffix size
        self.sz, self.max_sz = sz, max_sz

    def _suf_to_int(self, s):
        """Converts a string suffix to its integer representation."""
        n = 0
        # Convert each character to its base value and calculate the total
        for i, c in enumerate(s):
            n += self.sort_map[c] * (self.base ** (self.max_sz - i))
        return n

    def _int_to_suf(self, n):
        """Converts an integer back to its string suffix representation."""
        if n == 0:  # Special case: smallest integer maps to 'aaaaaa'
            return 'a' * self.max_sz
        s = ''
        # Convert the integer into characters by repeatedly dividing by the base
        while n > 0:
            n, remainder = divmod(n, self.base)
            s = self.sort_chars[remainder] + s
        # Pad with 'a' to ensure the result matches the max suffix size
        return s.rjust(self.max_sz, 'a')

    def encode(self, seq):
        """Encodes an integer into a zero-padded lexseq."""
        return f'{seq:0{self.sz}}'

    def decode(self, lseq):
        """Decodes the numeric prefix of a lexseq into an integer."""
        return int(lseq[:self.sz])

    def start(self):
        """Returns the starting lexseq (prefix = 1)."""
        return self.encode(1)

    def next(self, lseq):
        """Returns the next lexseq in lexicographical order."""
        if lseq is None:  # If no lexseq provided, start at the beginning
            return self.encode(1)
        # Increment the numeric prefix and re-encode
        return self.encode(self.decode(lseq) + 1)

    def interpolate(self, lseq1, lseq2):
        """
        Returns an lseq in the middle of the lexical order between lseq1 and lseq2.
        Handles both numeric prefixes and string suffixes.
        """
        # Decode numeric prefixes
        if lseq1 is None: lseq1 = self.encode(0)
        seq1, seq2 = self.decode(lseq1), self.decode(lseq2)
        seq1, seq2 = min(seq1, seq2), max(seq1, seq2)  # Ensure seq1 <= seq2
        # If there is room between the numeric prefixes, interpolate directly
        if seq2 > seq1 + 1: return self.encode(int((seq1 + seq2) / 2))
        # Otherwise, interpolate between string suffixes
        suf1, suf2 = lseq1[self.sz:], lseq2[self.sz:]
        # Default suffixes if none are provided
        if suf1 == '': suf1 = 'a' * self.max_sz
        if suf2 == '': suf2 = 'z' * self.max_sz
        # Convert suffixes to integers and find the midpoint
        n1, n2 = self._suf_to_int(suf1), self._suf_to_int(suf2)
        suf = self._int_to_suf(int((n1 + n2) / 2))
        # Return the interpolated lexseq
        return lseq1[:self.sz] + suf

# ################################################################################
# Etc (not yet ready, to be tested)
# ################################################################################

def setify(o):
    return o if isinstance(o,set) else set(listify(o))

def uniqueify(x, sort=False):
    res = list(OrderedDict.fromkeys(x).keys())
    if sort: res.sort()
    return res

class L():
    def __init__(self, items): self.items = listify(items)
    def __getitem__(self, idx):
        try: return self.items[idx]
        except TypeError:
            if isinstance(idx[0],bool):
                assert len(idx)==len(self) # bool mask
                return [o for m,o in zip(idx,self.items) if m]
            return [self.items[i] for i in idx]
    def __len__(self): return len(self.items)
    def __iter__(self): return iter(self.items)
    def __setitem__(self, i, o): self.items[i] = o
    def __delitem__(self, i): del(self.items[i])
    def __repr__(self):
        res = f'{self.__class__.__name__} ({len(self)} items)\n{self.items[:10]}'
        if len(self)>10: res = res[:-1]+ '...]'
        return res
    def append(self,o): return self.items.append(o)
    def remove(self,o): return self.items.remove(o)
    def unique(self): return L(dict.fromkeys(self).keys())
    def sort(self, key=None, reverse=False): return self.items.sort(key=key, reverse=reverse)
    def reverse(self ): return self.items.reverse()

_camel_re1 = re.compile('(.)([A-Z][a-z]+)')
_camel_re2 = re.compile('([a-z0-9])([A-Z])')
def camel2snake(name):
    s1 = re.sub(_camel_re1, r'\1_\2', name)
    return re.sub(_camel_re2, r'\1_\2', s1).lower()

def compose(x, funcs, *args, order_key='_order', **kwargs):
    key = lambda o: getattr(o, order_key, 0)
    for f in sorted(listify(funcs), key=key): x = f(x, **kwargs)
    return x

def ifnone(a, b): return b if a is None else a

def check_list_str(e, sz=64, n=1024):
    """
        Enforce input to be list and check_str all elements
        Limits list lenght to sz and every element size to n
    """
    if type(e)!=list: return None
    return [check_str(e1,n) for e1 in e[:sz]]

def check_dict(e, keys=[], n=1024):
    """
        Returns the input to be dict with only the attributes deffined in keys
        Every attribute must be int, float, bool or str
        String attributes are enforce to max lengh of n
    """
    if type(e)!=dict:
        return None
    d = {}
    for k in keys:
        if k not in e:
            continue
        if type(e[k]) in [bool,int,float]:
            d[k] = e[k]
        elif is_numeric_str(e[k]):
            v = check_float(e[k])
            if int(v)==v:
                v = int(v)
            d[k] = v
        else:
            d[k] = check_str(e[k], n=n)
    return d
