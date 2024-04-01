import socket
from infrastructures.networks.network_handler import NetworkHandler

class SocketHandler(NetworkHandler):
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def listen(self, host, port):
        self.server_socket.bind((host, port))
        self.server_socket.listen()

    def accept_client(self):
        client_socket, _ = self.server_socket.accept()
        return client_socket

    def receive(self, client_socket):
        return client_socket.recv(1024).decode()

    def send(self, client_socket, data):
        client_socket.send(data.encode())
