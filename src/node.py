import socket
import select
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
        self.pred.listen()

        self.succ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.fingerTable = []

    def contains_key(self, key: int) -> bool:
        return key in self.resources.keys()
    
    def query(self, data: bytes) -> None:
        self.succ.sendall(data)
        sleep(0.01)
        try:
            r, _, _ = select.select([self.succ], [], [], 0.01)
            if r:
                data = self.succ.recv(1024).strip()
                if data:
                    return data
            return b''
        except:
            return b''

    def serve(self) -> None:
        self.serving = True
        while self.serving:
            conn, _ = self.pred.accept()
            while self.serving:
                data = conn.recv(1024).strip()
                if not data:
                    break
                k, ip, port, cmd = data.decode().split('|')
                
                if cmd == 'detentor':
                    if ip == self.host and port == str(self.port):
                        print(f'Chave {k} não encontrada.')
                        #conn.send(b'C')
                    elif self.contains_key(int(k)):
                        msg = \
                            (k+'|'+self.host+'|'+str(self.port)+'|detem').encode()
                        conn.send(msg)
                    else:
                        conn.send(self.query(data))
                #elif cmd == 'detém':
                #    print(f'Chave {k} encontrada no nó #{port}')

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

    def calculateFingerTable(self, nodes: list):
        nodeId = self.port - BASE_PORT 
        bitNum = 64 
        self.fingerTable = [] 
        
        if nodeId not in nodes:
            nodes.append(nodeId)
        
        if not nodes:  
            raise ValueError("A lista de nós está vazia!")

        for i in range(1, 7): 
            fingerStart = (nodeId + 2**(i-1)) % bitNum  
            successor = None
        
            for node in sorted(nodes):
                if node >= fingerStart:
                    successor = node
                    break
            if successor is None:
                successor = sorted(nodes)[0]
            
            self.fingerTable.append(successor)

    def showFingerTable(self):
        print(f"Finger Table: {self.fingerTable}")