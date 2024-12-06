import asyncio
import numpy as np
import pytest
from pathlib import Path
from dl2050utils.core import oget
from dl2050utils.env import config_load

# ##########################################################################################
# Test config_load
# ##########################################################################################

yml = """
test1:
  attr1: 1

test2:
  attr2: value2
"""

project = 'test'
p = Path(f'./config-{project}.yml')
with open(p, 'w') as f:
    f.write(yml)

cfg = config_load('test')

@pytest.mark.parametrize('input,expected', [
    (['test1','attr1'], 1),
    (['test2','attr2'], 'value2'),
])

class Test_config_load:    
    def test_1(self, input, expected):
        assert oget(cfg,input)==expected

p.unlink()

if __name__ == "__main__":
    pytest.main()