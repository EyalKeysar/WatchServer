from abc import ABC, abstractmethod

class NetworkHandler(ABC):
    @abstractmethod
    def listen(self, host, port):
        pass

    @abstractmethod
    def accept_client(self):
        pass

    @abstractmethod
    def receive(self, client_socket):
        pass

    @abstractmethod
    def send(self, client_socket, data):
        pass
