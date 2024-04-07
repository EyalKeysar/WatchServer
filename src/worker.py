from dependency_injection import inject
from infrastructures.networks.network_handler import NetworkHandler
from infrastructures.networks.network_constants import HOST, PORT

class Worker:
    def __init__(self, network_handler):
        self.controllers_container = inject()
        self.network_handler = network_handler

    def work(self):
        # self.network_handler.listen(HOST, PORT)
        # while True:
        #     print("Waiting for request...")
        #     client_socket = self.network_handler.accept_client()
        #     request = self.network_handler.receive(client_socket)
        #     print("Request received: ", request)
            
        #     if request.startswith("fetch"):
        #         ans = self.controllers_container.fetch_controller.run(request)
        #         print("Sending response: ", ans)
        #         self.network_handler.send(client_socket, ans)
            
        #     client_socket.close()

        # a = self.controllers_container.handle("auth|signup|a@gmail.com|usernameabs|passwordabs")
        a = self.controllers_container.handle("fetch|parents")
        print(a)


if __name__ == "__main__":
    from infrastructures.networks.socket_handler import SocketHandler
    worker = Worker(SocketHandler())
    worker.work()
