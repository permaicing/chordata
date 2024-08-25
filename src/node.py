import socket
from utils import *


class Node:

    def __init__(self, port: int):
        self.port = port
        self.keys = range(port, port+KEYS_PER_NODE)
        
        self.pred = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.pred.bind((BASE_HOSTNAME, port))
        self.pred.listen(1)

        self.succ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.succ.connect((BASE_HOSTNAME, port+KEYS_PER_NODE))
        except:
            pass

    def contains_key(self, key) -> bool:
        self.keys.start <= key < self.keys.stop
    
    def query(self, data: bytes) -> None:
        self.succ.sendall(data)

    def serve(self) -> None:
        print('a')
        self.serving = True
        while self.serving:
            sock, _ = self.pred.accept()
            while self.serving:
                data = sock.recv(1024).strip()
                print(data.decode())

    def dismiss(self) -> None:
        self.serving = False
        self.pred.close()
        self.succ.close()