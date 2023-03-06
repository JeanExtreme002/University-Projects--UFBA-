from .connection_crypter import ConnectionCrypter
from socket import socket, timeout, AF_INET, SOCK_STREAM 
from typing import Optional

class Connection(object):
    """
    Classe para criar uma conexão com outro jogador.
    """
    __checking_string = "Check"
    
    def __init__(self, address: list, host: bool = False):
        self.__socket: Optional[socket] = None
        self.__connection: Optional[socket] = None
        
        self.__address = tuple(address)
        self.__hosting = host

    def __coordinates_to_string(self, origin: list[int], dest: list[int], promotion: int = 0) -> str:
        """
        Recebe duas tuplas XY, indicando origem e destino,
        e retorna uma string dessas coordenadas.
        """
        return "{}{}{}{}{}".format(*origin, *dest, promotion)

    def __get_connection(self) -> Optional[socket]:
        """
        Retorna o objeto de conexão.
        """
        return self.__connection if self.is_host() else self.__socket

    def __send_data(self, string: str, encrypt: bool = True) -> bool:
        """
        Envia os dados para o receptor.
        """
        if encrypt: string = self.__crypter.encrypt(string)
        
        connection = self.__get_connection()
        
        if connection: connection.send(string.encode())
        else: raise ConnectionError("no connection")
        
        return True

    def __string_to_coordinates(self, string: str) -> Optional[tuple[tuple, tuple, int]]:
        """
        Recebe uma string e retorna duas tuplas XY, indicando
        origem e destino, e uma peça de promoção, caso haja.
        """
        if len(string) == 5:
            origin = (int(string[0]), int(string[1]))
            dest = (int(string[2]), int(string[3]))
            return origin, dest, int(string[4])
        
        return None

    def close(self):
        """
        Encerra a conexão.
        """
        if self.__connection: self.__connection.close()
        if self.__socket: self.__socket.close()

        self.__connection = None
        self.__socket = None

    def connect(self, timeout_in_seconds: float = 5, attempts: int = 1):
        """
        Estabelece uma conexão.
        """
        if attempts == 0: return
        
        self.__socket = socket(AF_INET, SOCK_STREAM)
        self.__socket.settimeout(timeout_in_seconds)

        # Tenta estabelecer uma conexão, criando um servidor
        # ou se conectando à um servidor existente.
        try:
            if self.is_host():
                self.__socket.bind(self.__address)
                self.__socket.listen(1)

                self.__connection = self.__socket.accept()[0]
            else:
                self.__socket.connect(self.__address)

            # Cria objeto para criptografar os dados.
            self.__crypter = ConnectionCrypter(
                self.__address, self.__get_connection() # type: ignore
            )

        # Caso o tempo para conectar tenha excedido, uma nova
        # tentativa de conexão será realizada.
        except timeout:
            self.close()
            self.connect(timeout_in_seconds, attempts - 1)

        # Se outro tipo de exceção ocorreu, uma nova tentativa
        # de conexão será realizada somente se o modo de abertura
        # de conexão não for host. Caso o contrário, significaria
        # que pode existir algum problema no endereço informado.
        # Neste caso, é inútil realizar novas tentativas.
        except:
            self.close()
            
            if not self.is_host():
                self.connect(timeout_in_seconds, attempts - 1)
            
    def is_connected(self, attempts: int = 1) -> bool:
        """
        Verifica se está conectado.
        """
        if not self.__connection and not self.__socket: return False

        for i in range(attempts):
            try:
                self.__send_data(self.__checking_string, encrypt = False)
                return True
            except: pass
        return False

    def is_host(self) -> bool:
        """
        Verifica se é um host ou client.
        """
        return self.__hosting

    def recv(self) -> Optional[tuple[tuple, tuple, int]]:
        """
        Retorna as coordenadas de origem e destino.
        """
        getter = self.__get_connection()
        if not getter: raise ConnectionError("no connection")

        try:
            string = getter.recv(256).decode()
            string = string.replace(self.__checking_string, "")
            string = self.__crypter.decrypt(string)
            return self.__string_to_coordinates(string)
            
        except (ConnectionAbortedError, ConnectionResetError):
            return self.close()
            
        except timeout: return None

    def send(self, origin: list[int], dest: list[int], promotion: int = 0) -> bool:
        """
        Envia as coordenadas de origem e destino.
        """
        try:
            string = self.__coordinates_to_string(origin, dest, promotion)
            return self.__send_data(string)

        except ConnectionResetError:
            self.close()
        
        except timeout: pass

        return False 

