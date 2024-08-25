import socket
from time import sleep
from utils import *


class Node:

    def __init__(self, port: int):
        self.host = BASE_HOSTNAME
        self.port = port
        self.resources = \
            {k: None for k in range(port-BASE_PORT, port-BASE_PORT+KEYS_PER_NODE)}
        
        self.serving = self.connected = False
        
        self.pred = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.pred.settimeout(0)
        self.pred.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.pred.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.pred.bind((self.host, self.port))
        self.pred.listen(1)

        self.succ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def contains_key(self, key: int) -> bool:
        return key in self.resources.keys()
    
    def query(self, data: bytes) -> None:
        self.succ.sendall(data)
        sleep(0.01)
        data = self.succ.recv(1024).strip()
        if data:
            return data
        return b''

    def serve(self) -> None:
        self.serving = True
        while self.serving:
            conn, _ = self.pred.accept()
            while self.serving:
                data = conn.recv(1024).strip()
                if not data:
                    print('D')
                    break
                print(data.decode())
                k, ip, port, cmd = data.decode().split('|')
                
                if cmd == 'detentor':
                    if ip == self.host and port == str(self.port):
                        print(f'Chave {k} não encontrada.')
                        self.pred.send(b'\0')
                    elif self.contains_key(int(k)):
                        msg = \
                            (k+'|'+self.host+'|'+str(self.port)+'|detém').encode()
                        self.pred.send(msg)
                    else:
                        self.pred.send(self.query(data))

    def connect(self, port: int) -> bool:
        try:
            self.succ.connect((BASE_HOSTNAME, port))
            return True
        except Exception as e:
            return False

    def dismiss(self) -> None:
        self.serving = self.connected = False
        self.pred.close()
        self.succ.close()