import asyncio
import numpy as np
import pytest
from dl2050utils.core import is_numeric_str, check_float, check_int, check_str, check
from dl2050utils.core import listify, oget, xre, LRUCache

# ##########################################################################################
# Test is_numeric_str
# ##########################################################################################

@pytest.mark.parametrize('input,expected', [
    (None, False),
    (True, False),
    (False, False),
    ([], False),
    ({}, False),
    (1, False),
    ('abc', False),
    ('ab1', False),
    ('1ab', False),
    ('0,000', False),
    ('0', True),
    ('-0', True),
    ('100000', True),
    ('-100000', True),
    ('0.0001', True),
    ('10.0001', True),
    ('-100.000', True),
    ('0.000', True),
])

class Test_is_numeric_str:
    def test_1(self, input, expected):
        assert is_numeric_str(input)==expected

# ##########################################################################################
# Test check_float
# ##########################################################################################

@pytest.mark.parametrize('input,expected', [
    (None, None),
    (True, None),
    (False, None),
    ([], None),
    ({}, None),
    (1, 1.),
    (1., 1.),
    ('abc', None),
    ('ab1', None),
    ('1ab', None),
    ('0,000', None),
    ('0', 0.),
    ('-0', 0.),
    ('100000', 100000),
    ('-100000', -100000),
    ('0.0001', 0.0001),
    ('10.0001', 10.0001),
    ('-100.000', -100.000),
    ('0.000', 0.),
    ('12345678901234567890123456789012', 12345678901234567890123456789012.),
    ('123456789012345678901234567890123', 12345678901234567890123456789012.),
    ('123456789012345678901234567890123456789123456789123456789123456789123456789', 12345678901234567890123456789012.),
])

class Test_check_float:
    def test_1(self, input, expected):
        f = check_float(input)
        assert f==expected and (f is None or type(f)==float)

# ##########################################################################################
# Test check_int
# ##########################################################################################

@pytest.mark.parametrize('input,expected', [
    (None, None),
    (True, None),
    (False, None),
    ([], None),
    ({}, None),
    (1, 1.),
    (1., 1.),
    ('abc', None),
    ('ab1', None),
    ('1ab', None),
    ('0,000', None),
    ('0', 0.),
    ('-0', 0.),
    ('100000', 100000),
    ('-100000', -100000),
    ('0.0001', 0),
    ('10.0001', 10),
    ('-100.000', -100.000),
    ('0.000', 0.),
    ('12345678901234567890123456789012', 12345678901234567890123456789012.),
    ('123456789012345678901234567890123', 12345678901234567890123456789012.),
    ('123456789012345678901234567890123456789123456789123456789123456789123456789', 12345678901234567890123456789012.),
])

class Test_check_int:
    def test_1(self, input, expected):
        f = check_int(input)
        assert f==expected and (f is None or type(f)==int)

# ##########################################################################################
# Test check_str
# ##########################################################################################

@pytest.mark.parametrize('input,expected', [
    ((None,8), None),
    ((True,8), None),
    ((False,8), None),
    (([],8), None),
    (({},8), None),
    ((10,8), '10'),
    ((1234567890,8), '12345678'),
    (('abcdefgh',8), 'abcdefgh'),
    (('abcdefgh',4), 'abcd'),
])

class Test_check_str:
    def test_1(self, input, expected):
        (e,n) = input
        f = check_str(e, n=n)
        assert f==expected and (f is None or type(f)==str)

# ##########################################################################################
# Test check
# ##########################################################################################

@pytest.mark.parametrize('input,expected', [
    ((None,8), None),
    ((True,8), True),
    ((False,8), False),
    (([],8), None),
    (({},8), None),
    ((10,8), 10),
    ((12345678,8), 12345678),
    (('abcdefgh',8), 'abcdefgh'),
    (('abcdefgh',4), 'abcd'),
])

class Test_check:
    def test_1(self, input, expected):
        (e,n) = input
        f = check(e, n=n)
        assert f==expected

# ##########################################################################################
# Test listify
# ##########################################################################################

@pytest.mark.parametrize('input,expected', [
    (None, []),
    ([], []),
    (2, [2]),
    ([1, 2, 3], [1, 2, 3]),
    (np.array([4, 5, 6]), [4, 5, 6]),
    ("test", ["test"]),
    (['A','B'], ['A','B']),
    ([1], [1]),
    ([1,2], [1,2]),
    ((7, 8, 9), [7, 8, 9]),
    (iter([11, 12, 13]), [11, 12, 13]),
    (iter([]), []),
    ("", [""]),
    (np.array([]), []),
    ([[],[]], [[],[]]),
    ([None,[]], [None,[]]),
])

class Test_listify:
    def test_1(self, input, expected):
        assert listify(input) == expected

# ##########################################################################################
# Test oget
# ##########################################################################################

d = {'a':1, 'b':2, 'c':{'d':3}, 'e':[0,1,2]}

@pytest.mark.parametrize('o,attrs,default_,expected', [
    (None, None, None, None),
    (None, ['a'], None, None),
    ([], ['a'], None, None),
    (1, ['a'], None, None),
    ('a', ['a'], None, None),
    (['a'], ['a'], None, None),
    (d, ['z'], None, None),
    (d, ['a'], None, 1),
    (d, ['a','d'], None, None),
    (d, ['c','d'], None, 3),
    (d, ['c'], None, {'d':3}),
    (d, ['e',1], None, 1),
    (d, ['z'], 10, 10),
    (d, ['a','c'], 10, 10),
    (d, ['z'], 10, 10),
])

class Test_oget:
    def test_1(self, o, attrs, default_, expected):
        assert oget(o, attrs, default_) == expected

# ##########################################################################################
# Test xre
# ##########################################################################################

@pytest.mark.parametrize('input,expected', [
    ((None,None), None),
    (('(abc)def', None), None),
    ((None, 'abcdef'), None),
    (('(abc)def', 'abcdef'), 'abc'),
    (('(abc)def', 'abcdefghij'), 'abc'),
    (('(abc)def', 'abcdxxj'), None),
    ((r'/data/exp-(\d+).txt', '/data/exp-42.txt'), '42'),
])

class Test_xre:
    def test_1(self, input, expected):
        (r,s) = input
        m = xre(r,s)
        assert m==expected

# ##########################################################################################
# Test LRUCache
# ##########################################################################################

def load_callback_sync(key, **kwargs):
    return f"Loaded value for key: {key}"

async def load_callback_async(key, **kwargs):
    await asyncio.sleep(0.1)  # Simulate some asynchronous load delay
    return f"Async loaded value for key: {key}"

lru = LRUCache(3)

class Test_LRUCache:
    # @pytest.fixture
    # def lru(self):
    #     return LRUCache(3)
        
    def test_1(self):
        lru.put(1, 'value1')
        lru.put(2, 'value2')
        lru.put(3, 'value3')
        assert lru.get(1)=='value1'
    
    def test_2(self):
        assert lru.get(4)==-1

    def test_3(self):
        lru.put(4, 'value4')
        assert lru.get(4)=='value4'

    def test_4(self):
        """ 2 was the last beeing access, so was deleted """
        assert lru.get(2)==-1
        
    def test_5(self):
        """ Get value not in cache (now 2 is not) with load_callback_sync. """
        assert lru.get(2, load_callback=load_callback_sync)=='Loaded value for key: 2'
    
    @pytest.mark.asyncio
    async def test_6(self):
        """ Async get value not in cache (now 3 is not) with load_callback. """
        assert await lru.get_async(3, load_callback=load_callback_async)=='Async loaded value for key: 3'

if __name__ == "__main__":
    pytest.main()
