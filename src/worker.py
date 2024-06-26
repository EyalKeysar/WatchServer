from dependency_injection import inject
from infrastructures.networks.s_socket_handler import SecureSocketHandler
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
            # print(f"Received data: {data} from {client_socket.getpeername()}")
            response = self.controllers_container.handle(client_socket, data)
            self.network_handler.send_response(client_socket, response)
        self.network_handler.close()


if __name__ == "__main__":
    worker = Worker(SecureSocketHandler(HOST, PORT))
    worker.work()
