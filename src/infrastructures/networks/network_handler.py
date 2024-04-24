from abc import ABC, abstractmethod

class NetworkHandler(ABC):
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def get_request(self):
        pass

    @abstractmethod
    def send_response(self, client_socket, response):
        pass

    @abstractmethod
    def close(self):
        pass