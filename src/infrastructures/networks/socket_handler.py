import socket
from infrastructures.networks.network_handler import NetworkHandler
import threading

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




        
