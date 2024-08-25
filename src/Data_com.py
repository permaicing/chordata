import sys

class DataCom:
    SHOST = "localhost" # Static: DataCom.SHOST
    SPORT = 3000        # Static: DataCom.SPORT
    FAIXA = 1000

    def __init__(self, filename, numero_de_pares: int) -> None:
        if (numero_de_pares < 0): numero_de_pares = 1
        self.SIZE = numero_de_pares
        self.MAP = []
        for a in range(self.SIZE):    # IDEIA CIRCULAR P2P: [0, 1], [a,a+1], ..., [size-1, 0]
            server_port, client_port = a, (a+1) 
            if (client_port < self.SIZE):
                self.MAP.append([server_port, client_port])
            else:
                self.MAP.append([server_port, 0])
        self.IdxMAP = self._config_ports(filename)

    def _config_ports(self, filename): # IDEIA P2P: [S0,C1],[S1,C2],[S2,C0] ...
        _port = int(-1)
        try:
            with open(filename, 'r') as f: _port = int(f.read()) # Le porta usada no servidor
            with open(filename, 'w') as f: f.write(str(_port+1)) # Grava Porta usada para cliente conectar ao servidor parceiro
        except IOError:
            print("Erro ao ler arquivo!!")
            sys.exit(0)
            
        I = _port % self.SIZE # resto da divisão
        self.HOST_SERVER = DataCom.SHOST
        self.PORT_SERVER = self.MAP[I][0]+DataCom.FAIXA + DataCom.SPORT
        self.SUCESSOR = self.MAP[I][1]+DataCom.FAIXA + DataCom.SPORT
        self.sucessor_name = "NO[{0}]".format(self.SUCESSOR)
        self.host_name = "NO[{0}]".format(self.PORT_SERVER)
        Ant_I = I - 1 if I > 0 else self.SIZE - 1 # diminuir, e quando negativo Ant_I = SIZE-1
        self.antecessor_name = "NO[{0}]".format(self.MAP[Ant_I][0]+DataCom.FAIXA + DataCom.SPORT)

        # self.Fi, self.Fj = 0, 0
        sys.exit(I)
        
        return (I)

    def __repr__(self) -> str:
        s = "Servidor({0}), PortaServidor({1}), SUCESSOR({2}) -> FAIXA[{3}-{4}] ....".format(self.HOST_SERVER, 
            str(self.PORT_SERVER), str(self.SUCESSOR), 
            self.Fi, self.Fj)
        return s + "\nCliente vai conectar assim: ESCUTA({0}), SUCESSOR({1}) OK!!".format(self.HOST_SERVER, str(self.SUCESSOR))

    def self(self, I: int):
        self.Fi = self.MAP[I][0]+DataCom.SPORT-DataCom.FAIXA + 1
        self.Fj = self.MAP[I][1]+DataCom.SPORT-DataCom.FAIXA + 1
        if (I+1 == self.SIZE): self.Fi = int(self.PORT_SERVER-DataCom.SPORT + 1) # Caso Faixa Final até zero
