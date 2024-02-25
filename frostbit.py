import time
import socket

BIT_LEN_TIME = 39  # bit length of time
BIT_LEN_SEQUENCE = 8  # bit length of sequence number
BIT_LEN_MACHINE_ID = 63 - BIT_LEN_TIME - BIT_LEN_SEQUENCE  # bit length of machine id

# Errors
ERR_START_TIME_AHEAD = "start time is ahead of now"
ERR_NO_PRIVATE_ADDRESS = "no private ip address"
ERR_OVER_TIME_LIMIT = "over the time limit"
ERR_INVALID_MACHINE_ID = "invalid machine id"

# Constants for Sonyflake time unit (10 msec in nanoseconds)
SONYFLAKE_TIME_UNIT = 1e7

# Default start time for Sonyflake (Monday, 1 January 2024 12:00:00 AM)
DEFAULT_START_TIME = 1704067200000


class Sonyflake:
    def __init__(self, start_time=DEFAULT_START_TIME, machine_id=None):
        self.mutex = None
        self.start_time = start_time
        self.elapsed_time = 0
        self.sequence = 0
        self.machine_id = machine_id or self.lower_16_bit_private_ip()

    def next_id(self):
        mask_sequence = (1 << BIT_LEN_SEQUENCE) - 1
        current = self.current_elapsed_time()
        if self.elapsed_time < current:
            self.elapsed_time = current
            self.sequence = 0
        else:
            self.sequence = (self.sequence + 1) & mask_sequence
            if self.sequence == 0:
                self.elapsed_time += 1
                overtime = self.elapsed_time - current
                time.sleep(self.sleep_time(overtime))
        return self.to_id()

    def current_elapsed_time(self):
        return self.to_sonyflake_time(time.time() * 1000) - self.start_time

    def sleep_time(self, overtime):
        return (overtime * SONYFLAKE_TIME_UNIT) - (int(time.time() * 1000) % SONYFLAKE_TIME_UNIT)

    def to_id(self):
        if self.elapsed_time >= (1 << BIT_LEN_TIME):
            raise ValueError(ERR_OVER_TIME_LIMIT)

        return (self.elapsed_time << (BIT_LEN_SEQUENCE + BIT_LEN_MACHINE_ID)) | \
               (self.sequence << BIT_LEN_MACHINE_ID) | \
               self.machine_id

    def to_sonyflake_time(self, t):
        return int(t / SONYFLAKE_TIME_UNIT)

    def lower_16_bit_private_ip(self):
        ip = self.private_ipv4()
        if ip is None:
            raise ValueError(ERR_NO_PRIVATE_ADDRESS)
        return (ip[2] << 8) + ip[3]

    @staticmethod
    def sonyflake_time_unit():
        return SONYFLAKE_TIME_UNIT

    @staticmethod
    def private_ipv4():
        try:
            ips = socket.gethostbyname_ex(socket.gethostname())[2]
            for ip in ips:
                if ip.startswith("192.168.") or ip.startswith("10.") or ip.startswith("172."):
                    return list(map(int, ip.split(".")))
        except:
            pass
        return None

if __name__ == "__main__":
    sonyflake = Sonyflake()
    for _ in range(5):
        print("Generated ID:", sonyflake.next_id())