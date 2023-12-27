import socket
import os
import time
import random

from threading import Thread
from typing import Optional, Tuple


class ZeusServer(object):
    def __init__(self, addr, port, listener_server_address: Optional[Tuple[str, int]] = None, password: str = ""):
        self.__addr = addr
        self.__port = port

        self.__password = password
        self.__finished = False
        self.__server = None

        self.__listener_server_address = listener_server_address
        self.__path = f".server {addr}.{port}"       

    def close(self):
        """
        Finish the server.
        """
        self.__finished = True

        message = f"CLOSE:{self.__addr}:{self.__port}"
        self.tell_listerner_server_address(message)

        print("Shutting down...")
        self.__server.close()

    def initialize_directory(self):
        """
        Initialize folder of the server.
        """
        if not os.path.exists(self.__path):
            os.mkdir(self.__path)

    def initialize_client(self, client: str):
        """
        Initialize folder for the client.
        """
        if not os.path.exists(self.__path + f"/{client}"):
            os.mkdir(self.__path + f"/{client}")

    def tell_listerner_server_address(self, message):
        """
        Send the server's address to the listener server.
        """
        if self.__listener_server_address is None: return
        
        connection = socket.create_connection(self.__listener_server_address)
        
        message = message.encode()
        connection.sendall(message)

        connection.close()

    def get_file(self, connection, client: str, filename: str):
        """
        Get file at the client's folder.
        """
        filename = self.__path + "/" + f"{client}/" + filename
        
        if not os.path.exists(filename):
            return connection.send(b"FILENOTFOUNDERROR:")

        file_length = os.path.getsize(filename)
        connection.sendall(f"{file_length}:".encode())
            
        with open(filename, "rb") as file:
            for index in range(0, file_length, 1024):
                try: connection.sendall(file.read(1024))
                except: return

    def get_header(self, connection, max_length):
        """
        Get the header of the request.
        """
        buffer = connection.recv(6)

        while buffer.count(b":") < 4:
            data = connection.recv(1)
            buffer += data
            
            if len(buffer) > max_length:
                raise OverflowError("Invalid header.")

        return buffer 

    def save_file(self, connection, client: str, filename: str, file_length: int):
        """
        Save file at the client's folder.
        """
        with open(self.__path + "/" + f"{client}/" + filename, "wb") as file:            
            while file_length > 0:
                try:
                    data = connection.recv(1024)
                    file.write(data)
                    file_length -= 1024
                except: break

    def remove_file(self, connection, client: str, filename: str):
        """
        Remove file from the client's folder.
        """
        filename = self.__path + "/" + f"{client}/" + filename
        
        if os.path.exists(filename):
            os.remove(filename)

        connection.send(b"SUCCESS:")

    def list_directory(self, connection, client: str):
        """
        Remove file from the client's folder.
        """
        path = self.__path + "/" + f"{client}/"
        
        data = (":".join(os.listdir(path)) + ":").encode()
        connection.sendall("{}:".format(len(data)).encode())
        
        for index in range(0, len(data), 1024):
            connection.sendall(data[index: index + 1024])

    def process_connection(self, connection, address):
        """
        Process the request.
        """
        try:
            message = self.get_header(connection, max_length = 512).decode()
        except Exception as error:
            with open(self.__path + "/log.txt", "a+") as file:
                file.write("ERROR: " + str(error) + "\n\n")
            return connection.close()

        with open(self.__path + "/log.txt", "a+") as file:
            file.write("REQUEST: " + message + "\n\n")
        
        command, client, filename, file_length, _ = message.split(":")

        if command.lower() == "sd" and info == self.__password:
            return self.close()
        
        client = client.upper().replace(":", ".").replace("/", ".").replace("\\", ".").replace(";", ".")
        self.initialize_client(client)

        filename = os.path.basename(filename)        

        if command.lower() == "put":
            try: file_length = int(file_length)
            except: connection.sendall(b"INVALIDFORMATERROR:")

            if isinstance(file_length, int):
                self.save_file(connection, client, filename, file_length)

        elif command.lower() == "get":
            self.get_file(connection, client, filename)

        elif command.lower() == "del":
            self.remove_file(connection, client, filename)

        elif command.lower() == "ls":
            self.list_directory(connection, client)

        else: connection.sendall(b"COMMANDNOTEXISTSERROR:")

        connection.close()

    def run_server(self):
        """
        Keep server running.
        """       
        self.__server = socket.create_server((self.__addr, self.__port))
        self.__server.listen()

        message = f"JOIN:{self.__addr}:{self.__port}"
        self.tell_listerner_server_address(message)
        
        self.initialize_directory()
        
        while not self.__finished:
            try: connection, address = self.__server.accept()
            except: break

            thread = Thread(target=self.process_connection, args=(connection, address))
            thread.start()

    
if __name__ == "__main__":
    print("Zeus Server's Address:")
    addr = input("IP Address: ")
    port = int(input("Port Number: "))

    print("Listener Server's Address:")
    listener_addr = input("IP Address: ")
    listener_port = input("Port Number: ")

    if not listener_addr and not listener_port: listener_addr = None
    else: listener_addr = (listener_addr, int(listener_port))

    password = "".join([random.choice("qwertyuiopasdfghjklzxcvbnm") for i in range(5)])
    password = password.upper()
    
    server = ZeusServer(addr, port, listener_addr, password = password)

    thread = Thread(target=server.run_server)
    thread.start()

    time.sleep(1)
    
    print("The zeus server's password is '" + password + "'.")
