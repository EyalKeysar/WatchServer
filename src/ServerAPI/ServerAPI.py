from .send_recv import *
from .const import *
class ServerAPI:
    '''
        This class is used by the clients to communicate with the server.
    '''

    def build_request(self, service, command, *args):
        '''
            This method is used to build the request to be sent to the server.
        '''
        return f"{service}{ARGS_SEPERATOR}{command}{ARGS_SEPERATOR}" + f"{ARGS_SEPERATOR}".join(args)

    def __init__(self):
        self.server_ip = SERVER_IP
        self.server_port = SERVER_PORT

    def get_info(self):
        '''
            This method is used to get the information from the server.
        '''
        return send_request(self.build_request("fetch", "parents"))
    
    def login(self, email, password):
        '''
            This method is used to login to the server.
        '''
        return send_request(self.build_request("auth", "login", email, password))
    
    def signup(self, email, password, username):
        '''
            This method is used to signup to the server.
        '''
        return send_request(self.build_request("auth", "signup", email, password, username))
    
    
if __name__ == '__main__':
    server = ServerAPI()
    print(server.get_info())