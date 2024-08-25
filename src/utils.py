import sys


BASE_HOSTNAME = '127.0.0.1'
BASE_PORT = 50000
MAX_NODES = 2
KEYS_PER_NODE = 100

def parse_int(s: str) -> int:
    try:
        return int(s)
    except Exception as e:
        print(f'{e}')
        sys.exit(1)