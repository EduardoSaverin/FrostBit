import time
import pytest
from frostbit import FrostBit, ERR_OVER_TIME_LIMIT, ERR_NO_PRIVATE_ADDRESS

def test_default_start_time():
    frostbit = FrostBit()
    assert frostbit.start_time == 1704067200000

def test_next_id():
    frostbit = FrostBit(start_time=0)
    id1 = frostbit.next_id()
    time.sleep(0.01)
    id2 = frostbit.next_id()
    assert id1 < id2

def test_over_time_limit():
    frostbit = FrostBit(start_time=0)
    frostbit.elapsed_time = (1 << 39)
    with pytest.raises(ValueError) as e_info:
        frostbit.next_id()
    assert str(e_info.value) == ERR_OVER_TIME_LIMIT

def test_no_private_address():
    frostbit = FrostBit(start_time=0)
    frostbit.private_ipv4 = lambda: None
    with pytest.raises(ValueError) as e_info:
        frostbit.lower_16_bit_private_ip()
    assert str(e_info.value) == ERR_NO_PRIVATE_ADDRESS
