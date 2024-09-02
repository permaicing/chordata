import threading
import sys
from time import sleep
from node import Node
from utils import parse_int
"""
from Data_com import DataCom
from Server import Server
from Client import Client
"""


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f'Uso: {sys.argv[0]} PORTA')
        sys.exit(1)
    port = parse_int(sys.argv[1])

    allNodes = [port]

    node = Node(port)
    server = threading.Thread(target=node.serve, daemon=True)
    server.start()
    node.calculateFingerTable(allNodes)

    while True:
        cmd = input('|> ').strip().lower()

        if cmd.startswith('connect '):
            cmd, port = cmd.split()
            port = parse_int(port)
            if node.connect(port):
                print(f'Conectado ao nó #{port}.')
                allNodes.append(port)
                node.calculateFingerTable(allNodes)
            else:
                print(f'Não foi possível conectar-se ao nó #{port}.')
        elif cmd.startswith('query '):
            cmd, k = cmd.split()
            k = parse_int(k)
            if node.contains_key(k):
                print(f'Chave {k} presente no nó atual.')
            else:
                result = \
                    node.query((('%i|' % (k))+node.host+'|'+str(node.port)+'|detentor').encode()).strip()
                if result:
                    k, _, port, cmd = result.decode().split('|')
                    if cmd == 'detem':
                        print(f'Chave {k} encontrada no nó {port}.')
        elif cmd == 'finger':
            node.showFingerTable()
        elif cmd == 'exit':
            node.dismiss()
            break
    """
    numDePares = 2
    if len(sys.argv) >= 2:
        numDePares = int(sys.argv[1])
    
    info = DataCom("portas.txt", numDePares)
    servidor = Server(info)
    cliente = Client(info)

    tserver = threading.Thread(target=servidor.run)
    tserver.start()
    sleep(1 / 10)

    print(info)
    print("**************** [<<ENTER>>=CONECTAR] ****************")

    enter = input().strip() == ''
    if (enter):
        print("**************** [<<EXIT>>=SAIR] ****************")
        tclient = threading.Thread(target=cliente.run)
        tclient.start()
        tserver.join()
        tclient.join()
        print("**************** FIM CONECTADO ****************")
        print(input().strip())
    else:
        print("**************** ABORT ANTES DE CONECTAR ****************")
        cliente.close()
        print(input().strip())
    """