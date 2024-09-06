import threading
import sys
from time import sleep
from node import Node
from utils import parse_int


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
