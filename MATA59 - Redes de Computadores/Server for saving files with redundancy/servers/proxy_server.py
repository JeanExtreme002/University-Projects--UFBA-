import socket
import os
import time
import random

from threading import Thread
from typing import List, Tuple


class ProxyServer(object):
    def __init__(self, addr, port, listener_port: int = None, password: str = ""):
        self.__addr = addr
        self.__port = port

        self.__listener_port = listener_port
        self.__zeus_servers: List[Tuple[str, int]] = []

        self.__password = password
        self.__finished = False
        self.__server = None    

    def close(self):
        """
        Finish the server.
        """
        self.__finished = True

        print("Shutting down...")
        self.__server.close()
        self.__listener.close()

    def get_zeus_server_addresses(self):
        """
        Return list of addresses of zeus servers.
        """
        return self.__zeus_servers.copy()

    def list_files(self, address, connection, client):
        """
        Return all saved files of an user.
        """
        request = f"LS:{client}:::"

        files = dict()

        for address in self.__zeus_servers:
            try:
                zeus_server_connection = socket.create_connection(address)
                zeus_server_connection.sendall(request.encode())
            except: continue                

            length, buffer = b"", b""

            # Obtém os dados enquanto houver.
            while isinstance(length, bytes) or length > 0:
                try:
                    data = zeus_server_connection.recv(1024 if isinstance(length, int) else 1)
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
                filename = filename.lower()
                
                if filename:
                    if not filename in files: files[filename.lower()] = "1 copy"
                    else: files[filename.lower()] = str(int(files[filename.lower()].split()[0]) + 1) + " copies"

        data = (":".join([f"{k} ({v})" for k, v in files.items()]) + ":").encode()
        connection.sendall("{}:".format(len(data)).encode())

        for index in range(0, len(data), 1024):
            connection.sendall(data[index: index + 1024])

    def get_file(self, address, connection, client: str, filename: str):
        """
        Get file at the client's folder.
        """
        request = f"GET:{client}:{filename}::"
        received = False

        for zeus_server in self.__zeus_servers:            
            try:
                zeus_server_connection = socket.create_connection(zeus_server)
                zeus_server_connection.sendall(request.encode())
            except: continue

            length = b""

            # Obtém os dados enquanto houver.
            while isinstance(length, bytes) or length > 0:                
                try:
                    data = zeus_server_connection.recv(1024 if received else 1)
                except:
                    if not received: break # Se a transferência não havia iniciado, tente outros servidores.
                    return connection.close() # Se a transferência havia iniciado e falhou, então apenas aborte.

                # Obtém o tamanho do arquivo a ser recebido.
                if not received:
                    if data == b":":
                        try:
                            length = int(length)
                            received = True
                            connection.send(f"{length}:".encode())
                        except:
                            received = False
                            break
                    else: length += data
                    
                    continue

                # Se há dados, transmita para o cliente.
                if data:
                    connection.sendall(data)
                    length -= len(data)

            # Encerra se os dados tiverem sido recebidos
            if received: return

        # Se não foi possível obter o arquivo de nenhum servidor,
        # informe o cliente com um erro.
        connection.send(b"FILENOTFOUNDERROR:")

    def get_header(self, connection, max_length):
        """
        Get the header of the request.
        """
        buffer = connection.recv(6)

        while buffer.count(b":") < 5:
            data = connection.recv(1)
            buffer += data
            
            if len(buffer) > max_length:
                raise TimeoutError("Invalid header.")

        return buffer 

    def save_file(self, address, connection, client: str, filename: str, file_length: str, n_copies: int):
        """
        Save file at the client's folder.
        """
        if not os.path.exists(".proxy_server_temp"):
            os.mkdir(".proxy_server_temp")
            
        if n_copies <= 0:
            self.delete_copies(client, filename, self.__zeus_servers)
            return
        
        bytes_to_receive = file_length

        # Armazena os dados em um arquivo temporário.
        temp_filename = f"{address[0]}.{address[1]}_{client}_{filename}.temp"
        temp_filename = os.path.join(".proxy_server_temp", temp_filename)
        
        with open(temp_filename, "wb") as temporary_file:
            while bytes_to_receive > 0:
                try:
                    data = connection.recv(1024)
                    temporary_file.write(data)
                    bytes_to_receive -= len(data)
                except: return

        bytes_to_receive = file_length

        # Obtém o número de cópias desejadas e possíveis.
        n_servers = len(self.__zeus_servers)
        n_copies = min(n_copies, n_servers)

        # Verifica quais servidores já possuem cópias.
        servers_with_copies = self.check_servers_copy(client, filename)
        n_copies = n_copies - len(servers_with_copies)

        # Se já houver a quantidade exata de cópias, não faça nada.
        # Se a quantidade de cópias exceder o desejado, apague-as
        # dos servidores até que tenha o número exato desejado.
        if n_copies <= 0:
            servers = servers_with_copies[:abs(n_copies)]
            return self.delete_copies(client, filename, servers)

        # Obtém a lista de servidores aos quais os bytes dos arquivos serão enviados.
        servers = [addr for addr in self.__zeus_servers if addr not in servers_with_copies]
        servers = servers[:n_copies]
        
        # Envia os dados para os servidores.
        for address in servers:
            try: connection_server = socket.create_connection(address)
            except: continue
            
            request = f"PUT:{client}:{filename}:{file_length}:"
            connection_server.sendall(request.encode())

            bytes_to_send = file_length

            # Abre o arquivo temporário e realiza o streamming dos dados.
            with open(temp_filename, "rb") as file:       
                while bytes_to_send > 0:
                    try:
                        connection_server.sendall(file.read(1024))
                        bytes_to_send -= 1024
                    except: break

        # Remove o arquivo temporário.
        os.remove(temp_filename)

    def list_zeus_server(self, address, connection):
        """
        Send the list of address of zeus servers.
        """
        data = (":".join([f"{a}.{p}" for a, p in self.__zeus_servers]) + ":").encode()
        connection.sendall("{}:".format(len(data)).encode())

        for index in range(0, len(data), 1024):
            connection.sendall(data[index: index + 1024])

    def delete_copies(self, client, filename, servers):
        """
        Delete copies of client's file in specified servers
        """
        request = f"DEL:{client}:{filename}::"
        
        for address in servers:
            try:
                connection = socket.create_connection(address)
                connection.sendall(request.encode())
            except: continue

    def check_servers_copy(self, client, filename):
        """
        Check which servers contains copies of files
        """
        servers: List[Tuple[str, int]] = list()
        request = f"LS:{client}:::" 

        for address in self.__zeus_servers:
            try:
                connection = socket.create_connection(address)
                connection.sendall(request.encode())
                length = ""

                while True:
                    data = connection.recv(1).decode()
                    if data == ":": break
                    length += data
    
                length = int(length)   
                data = b""

                while length > 0:
                    data += connection.recv(1024)
                    length -= len(data)

                if filename in data.decode():
                    servers.append(address)

            except: continue 

        return servers

    def process_connection(self, connection, address):
        """
        Process the request.
        """
        try: message = self.get_header(connection, max_length = 512).decode()
        except: return connection.close()
        
        command, client, filename, file_length, n_copies, _ = message.split(":")

        if command.lower() == "sd" and info == self.__password:
            return self.close()
        
        client = client.upper().replace(":", ".").replace("/", ".").replace("\\", ".").replace(";", ".")

        filename = os.path.basename(filename)

        if command.lower() == "put":
            try: self.save_file(address, connection, client, filename, int(file_length), int(n_copies))
            except: pass

        elif command.lower() == "get":
            self.get_file(address, connection, client, filename)

        elif command.lower() == "ls":
            self.list_files(address, connection, client)

        elif command.lower() == "lszs":
            self.list_zeus_server(address, connection)

        elif command.lower() == "del":
            self.delete_copies(client, filename, self.__zeus_servers)

        else: connection.sendall(b"COMMANDNOTEXISTSERROR:")
        
        connection.close()

    def run_listener(self):
        """
        Keep listener running.
        """
        self.__listener = socket.create_server((self.__addr, self.__listener_port))
        self.__listener.listen()

        while not self.__finished:
            try:
                connection, address = self.__listener.accept()
                data = connection.recv(128).decode()

                if data.count(":") < 2: continue
                else: annotation, address, port = data.split(":")

                if annotation.lower() not in ["join", "close"]: continue

                try: port = int(port)
                except: continue

                if annotation.lower() == "join":
                    self.__zeus_servers.append((address, port))
                    
                if annotation.lower() == "close" and (address, port) in self.__zeus_servers:
                    self.__zeus_servers.remove((address, port))
                    
            except: break

    def run_server(self):
        """
        Keep server running.
        """       
        self.__server = socket.create_server((self.__addr, self.__port))
        self.__server.listen()

        listener_thread = Thread(target=self.run_listener)
        listener_thread.start()
        
        while not self.__finished:
            try: connection, address = self.__server.accept()
            except: break

            thread = Thread(target=self.process_connection, args=(connection, address))
            thread.start()


if __name__ == "__main__":
    print("Proxy Server's Address:")
    addr = input("IP Address: ")
    port = int(input("Port Number: "))
    listener_port = int(input("Listener Port Number: "))

    password = "".join([random.choice("qwertyuiopasdfghjklzxcvbnm") for i in range(5)])
    password = password.upper()
    
    server = ProxyServer(addr, port, listener_port, password = password)

    thread = Thread(target=server.run_server)
    thread.start()

    time.sleep(1)
    
    print("The proxy server's password is '" + password + "'.")

