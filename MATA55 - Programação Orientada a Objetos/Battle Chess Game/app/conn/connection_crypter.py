from ..crypter import Crypter
import random, socket

class ConnectionCrypter(Crypter):
    """
    Classe para encriptografar e descriptografar
    os dados trafegados pela conexão.
    """
    def __init__(self, address: tuple, connection: socket.socket):
        self.__connection = connection
        super().__init__(address)

    def generate_key(self, address: tuple) -> str:
        """
        Recebe uma senha e retorna uma chave parcial.
        """
        password = str()

        for index in range(0, len(address[0]), 2):
            password += address[0][index: index + 2]
            
            if index // 2 < len(str(address[1])):
                 password += str(address[1])[index // 2]

        values = []
        values.append(str(random.randint(10**6, 10**10)))

        self.__connection.send(values[0].encode())
        values.append(self.__connection.recv(32).decode())

        values.sort()
        salt = "".join(values)

        return password + salt
