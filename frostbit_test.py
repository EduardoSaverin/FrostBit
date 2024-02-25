import time
import pytest
from frostbit import Sonyflake, ERR_OVER_TIME_LIMIT, ERR_NO_PRIVATE_ADDRESS

def test_default_start_time():
    sonyflake = Sonyflake()
    assert sonyflake.start_time == 1704067200000

def test_next_id():
    sonyflake = Sonyflake(start_time=0)
    id1 = sonyflake.next_id()
    time.sleep(0.01)
    id2 = sonyflake.next_id()
    assert id1 < id2

def test_over_time_limit():
    sonyflake = Sonyflake(start_time=0)
    sonyflake.elapsed_time = (1 << 39)
    with pytest.raises(ValueError) as e_info:
        sonyflake.next_id()
    assert str(e_info.value) == ERR_OVER_TIME_LIMIT

def test_no_private_address():
    sonyflake = Sonyflake(start_time=0)
    sonyflake.private_ipv4 = lambda: None
    with pytest.raises(ValueError) as e_info:
        sonyflake.lower_16_bit_private_ip()
    assert str(e_info.value) == ERR_NO_PRIVATE_ADDRESS
