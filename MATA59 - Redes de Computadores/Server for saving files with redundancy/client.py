from servers.proxy_server import ProxyServer
from servers.zeus_server import ZeusServer
from threading import Thread

import os
import socket
import time
import sys


class Client(object):

    def __init__(self, addr, proxy_port, listener_port):
        self.address = addr
        self.proxy_port = proxy_port
        self.listener_port = listener_port

        self.__servers = dict()

    def add_zeus_server(self, port):    
        server = ZeusServer(self.address, port, (self.address, self.listener_port))
        self.__servers[port] = server
        
        thread = Thread(target=server.run_server)
        thread.start()

        print("Zeus Server criado com sucesso.")

    def save(self, command):
        if len(command) < 4:
            return print("O comando digitado é inválido.")
        
        if not os.path.exists(command[2]):
            return print("Não foi possível encontrar o arquivo.")

        length = os.path.getsize(command[2])
        
        connection = socket.create_connection((self.address, self.proxy_port))

        request = f"PUT:{command[1]}:{command[2]}:{length}:{command[3]}:"
        connection.sendall(request.encode())

        with open(command[2], "rb") as file:
            while length > 0:
                try:
                    connection.sendall(file.read(1024))
                    length -= 1024
                except: return print("Falha durante o envio do arquivo. Restavam", length, "bytes.")

    def recover(self, command):
        if len(command) < 3:
            return print("O comando digitado é inválido.")
        
        connection = socket.create_connection((self.address, self.proxy_port))

        request = f"GET:{command[1]}:{command[2]}:::"
        connection.sendall(request.encode())

        if not os.path.exists(f".client_{command[1]}_download/"):
            os.mkdir(f".client_{command[1]}_download/")

        with open(f".client_{command[1]}_download/" + command[2], "wb") as file:
            length = b""
            
            while isinstance(length, bytes) or length > 0:
                try:
                    data = connection.recv(1024 if isinstance(length, int) else 1)

                    if isinstance(length, bytes):
                        if data == b":":
                            length = int(length)
                            continue
                        else: length += data
                except:
                    length = length if isinstance(length, int) else "inf"
                    return print("Falha durante o envio do arquivo. Restavam", length, "bytes.")
                
                if isinstance(length, int) and data:
                    file.write(data)
                    length -= len(data)

    def list_files(self, client):
        request = f"LS:{client}::::"
        
        connection = socket.create_connection((self.address, self.proxy_port))
        connection.sendall(request.encode())

        length, buffer = b"", b""

        # Obtém os dados enquanto houver.
        while isinstance(length, bytes) or length > 0:
            try:
                data = connection.recv(1024 if isinstance(length, int) else 1)
            except:
                buffer = b""
                break
            
            # Obtém o tamanho do arquivo a ser recebido.
            if isinstance(length, bytes):
                if data == b":": length = int(length)
                else: length += data
            
            elif data:
                buffer += data
                length -= len(data)

        # Adiciona os arquivos obtidos do servidor para o set.
        for filename in buffer.decode().rstrip(":").split(":"):
            if filename: print("-", filename)

    def list_zeus_server(self):
        request = f"LSZS:::::"
        
        connection = socket.create_connection((self.address, self.proxy_port))
        connection.sendall(request.encode())

        length, buffer = b"", b""

        # Obtém os dados enquanto houver.
        while isinstance(length, bytes) or length > 0:
            try:
                data = connection.recv(1024 if isinstance(length, int) else 1)
            except:
                buffer = b""
                break
            
            # Obtém o tamanho do arquivo a ser recebido.
            if isinstance(length, bytes):
                if data == b":": length = int(length)
                else: length += data
            
            elif data:
                buffer += data
                length -= len(data)

        # Adiciona os arquivos obtidos do servidor para o set.
        for address in buffer.decode().rstrip(":").split(":"):
            if address: print("-", address)

    def delete_copies(self, client, filename):
        request = f"DEL:{client}:{filename}:::"
        
        connection = socket.create_connection((self.address, self.proxy_port))
        connection.sendall(request.encode())

    def run_client(self):
        admin = False

        os.system("cls" if "win" in sys.platform else "clear")
        
        while True:
            message = "Lista de Comandos:\n"
            message += "\n- save <username> <filename> <n_copies>"
            message += "\n- recover <username> <filename>"
            message += "\n- list <username>"
            message += "\n- delete <username> <filename>"
            message += "\n- set_admin <on/off> | Libera funções especiais"

            if admin:
                message += "\n+ add_zeus_server <port_number>"
                message += "\n+ close_zeus_server <port_number>"
                message += "\n+ list_zeus_server"
                
            message += "\n- clear\n"
            message += "=" * 50

            print(message)

            command = input("Comando/> ").lower().split()
            
            if not command: pass

            elif admin and command[0] == "add_zeus_server":
                try: self.add_zeus_server(int(command[1]))
                except: print("Número de porta inválido.")

            elif admin and command[0] == "list_zeus_server":
                self.list_zeus_server()

            elif admin and command[0] == "close_zeus_server":
                try: command[1] = int(command[1])
                except: return print("O comando digitado é inválido.")
                
                if command[1] == self.proxy_port or int(command[1]) not in self.__servers:
                    print("Número de porta inválido.")
                    
                try: self.__servers[command[1]].close()
                except: pass

            elif command[0] == "save": self.save(command)

            elif command[0] == "recover": self.recover(command)

            elif command[0] == "list":
                try: self.list_files(command[1])
                except IndexError: print("O comando digitado é inválido.")

            elif command[0] == "delete":
                try: self.delete_copies(command[1], command[2])
                except IndexError: print("O comando digitado é inválido.")

            elif command[0] == "clear":
                os.system("cls" if "win" in sys.platform else "clear")

            elif command[0] == "set_admin":
                try: admin = (command[1] == "on")
                except IndexError: print("O comando digitado é inválido.")

            else: print("O comando digitado é inválido.")

            print("=" * 50)


if __name__ == "__main__":
    print("Insira o endereço IP do servidor proxy:")
    
    addr = input("Endereço IP: ")
    port = int(input("Número da Porta: "))
    listener_port = int(input("Número da Porta do Listener: "))

    if input("Deseja criar um servidor proxy (Y/N)? ").lower().startswith("y"):
        proxy_server = ProxyServer(addr, port, listener_port)

        thread = Thread(target=proxy_server.run_server)
        thread.start()
    
    time.sleep(1)

    client = Client(addr, port, listener_port)
    client.run_client()
