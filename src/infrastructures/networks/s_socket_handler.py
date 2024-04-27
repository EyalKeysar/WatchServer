from ServerAPI.s_socket import *
from infrastructures.networks.network_handler import NetworkHandler

import threading

"""
For reference, this is multiuser echo server

def start_multiuser_secure_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        tls_protocol = s_socket.TLSProtocol(client_socket)
        tls_protocol.server_handshake()

        threading.Thread(target=handle_client, args=(client_socket, tls_protocol)).start()

"""
"""
For reference, this is the normal socket handler
class SocketHandler(NetworkHandler):
    def __init__(self, host, port):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen()
        print(f"Server is listening on {host}:{port}")
        
        self.threads = []
        self.client_sockets = []
        self.requests_queue = []

    def start(self):
        # this function wont block the main thread
        threading.Thread(target=self._accept_clients).start()

    def _accept_clients(self):
        while True:
            client_socket, _ = self.server_socket.accept()
            print(f"Accepted connection from {client_socket.getpeername()}")
            self.client_sockets.append(client_socket)
            threading.Thread(target=self._handle_client, args=(client_socket,)).start()

    def _handle_client(self, client_socket):
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            self.requests_queue.append((client_socket, data))

    def get_request(self):
        if len(self.requests_queue) == 0:
            return None
        return self.requests_queue.pop(0)
    
    def send_response(self, client_socket, response):
        # send over thread to avoid blocking the main thread
        print(f"Sending response to {client_socket.getpeername()}")
        threading.Thread(target=client_socket.send, args=((str(response)).encode(),)).start()

    def close(self):
        self.server_socket.close()
        for client_socket in self.client_sockets:
            client_socket.close()
"""

class SSLSocketHandler(NetworkHandler):
    def __init__(self, host, port):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen()
        print(f"Server is listening on {host}:{port}")
        
        self.threads = []
        self.client_sockets = []
        self.requests_queue = []
        self.tls_protocols = []

    def start(self):
        # this function wont block the main thread
        threading.Thread(target=self._accept_clients).start()

    def _accept_clients(self):
        while True:
            client_socket, _ = self.server_socket.accept()
            print(f"Accepted connection from {client_socket.getpeername()}")
            self.client_sockets.append(client_socket)
            threading.Thread(target=self._handle_client, args=(client_socket,)).start()

    def _handle_client(self, client_socket):
        tls_protocol = TLSProtocol(client_socket)
        tls_protocol.server_handshake()
        self.tls_protocols.append((client_socket, tls_protocol))
        while True:
            data = tls_protocol.receive()
            if not data:
                break
            self.requests_queue.append((client_socket, data))

    def get_request(self):
        if len(self.requests_queue) == 0:
            return None
        return self.requests_queue.pop(0)
    
    def send_response(self, client_socket, response):
        # send over thread to avoid blocking the main thread
        print(f"Sending response to {client_socket.getpeername()} : {response}")
        for socket, tls_protocol in self.tls_protocols:
            if socket == client_socket:
                tls_protocol.send(response)
                break
        
    def close(self):
        self.server_socket.close()
        for client_socket in self.client_sockets:
            client_socket.close()
        for socket, tls_protocol in self.tls_protocols:
            close(socket)
