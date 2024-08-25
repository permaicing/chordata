import threading
import sys
from time import sleep
from Data_com import DataCom
from Server import Server
from Client import Client

if __name__ == "__main__":
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