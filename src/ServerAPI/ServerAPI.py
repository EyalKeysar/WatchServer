from .send_recv import *
from .const import *
class ServerAPI:
    '''
        This class is used by the clients to communicate with the server.
    '''

    def __init__(self):
        self.server_ip = SERVER_IP
        self.server_port = SERVER_PORT

        print(f"Connecting to server at {self.server_ip}:{self.server_port}")

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.connect((self.server_ip, self.server_port))

    def build_request(self, service, command, *args):
        '''
            This method is used to build the request to be sent to the server.
        '''
        return self.server_socket, f"{service}{ARGS_SEPERATOR}{command}{ARGS_SEPERATOR}" + f"{ARGS_SEPERATOR}".join(args)


# AUTHENTICATION -----------------------------------------------------------------------------------------------------

    def login(self, email, password):
        '''
            This method is used to login to the server.
        '''
        return send_request(*self.server_socket, self.build_request("auth", "login", email, password))
    
    def signup(self, email, password, username):
        '''
            This method is used to signup to the server.
        '''
        return send_request(*self.build_request("auth", "signup", email, password, username))
# ---------------------------------------------------------------------------------------------------------------------


# FETCHING INFORMATION -----------------------------------------------------------------------------------------------
    def get_info(self):
        '''
            This method is used to get the information from the server.
        '''
        return send_request(*self.build_request("fetch", "parents"))
    
    def get_statistics(self):
        '''
            This method is used to get the statistics from the server.
        '''
        return send_request(*self.build_request("fetch", "statistics"))
    
    def get_restrictions(self):
        '''
            This method is used to get the restrictions from the server.
        '''
        return send_request(*self.build_request("fetch", "restrictions"))
# ---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    server = ServerAPI()
    print(server.get_info())