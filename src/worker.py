from dependency_injection import inject
from infrastructures.networks.network_handler import NetworkHandler
from infrastructures.networks.network_constants import HOST, PORT

class Worker:
    def __init__(self, network_handler):
        self.controllers_container = inject()
        self.network_handler = network_handler

    def work(self):
        self.network_handler.start()
        while True:
            request = self.network_handler.get_request()
            if request is None:
                continue
            client_socket, data = request[0], request[1]
            response = self.controllers_container.handle(client_socket, data.decode())
            self.network_handler.send_response(client_socket, response)
        self.network_handler.close()


if __name__ == "__main__":
    from infrastructures.networks.socket_handler import SocketHandler
    worker = Worker(SocketHandler(HOST, PORT))
    worker.work()
