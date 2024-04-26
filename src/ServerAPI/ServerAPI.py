import s_socket
from .const import *
import threading
import time
import json
class ServerAPI:
    '''
        This class is used by the clients to communicate with the server.
    '''

    def __init__(self):
        self.server_ip = SERVER_IP
        self.server_port = SERVER_PORT

        self.is_connected = False

        print(f"Connecting to server at {self.server_ip}:{self.server_port}")

        # connect via thread to avoid blocking the main thread
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        threading.Thread(target=self.connect).start()
        self.children = []

    def connect(self):
        '''
            This method is used to connect to the server.
        '''
        while True:
            time.sleep(2)
            if not self.is_connected:
                try:
                    self.server_socket.connect((self.server_ip, self.server_port))
                    self.is_connected = True
                except Exception as e:
                    print(f"Failed to connect to server: {e}")
                    self.is_connected = False

    def build_request(self, service, command, *args):
        '''
            This method is used to build the request to be sent to the server.
        '''
        if args == ():
            return self.server_socket, f"{service}{ARGS_SEPERATOR}{command}"
        else:
            print("args: ", args)
            return self.server_socket, f"{service}{ARGS_SEPERATOR}{command}{ARGS_SEPERATOR}" + f"{ARGS_SEPERATOR}".join(args) 


# AUTHENTICATION -----------------------------------------------------------------------------------------------------

    def login(self, email, password):
        '''
            This method is used to login to the server.
        '''
        return send_request(*self.build_request("auth", "login", email, password))
    
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
    
    def get_children(self):
        '''
            This method is used to get the children from the server.
        '''
        respond = send_request(*self.build_request("fetch", "children"))
        # parse the respond as json of list of ChildData
        print("respond (json ch)" + respond)
        self.children = json.loads(respond)
        return self.children
        
    def new_agent_request(self, mac_address):
        '''
            This method is used to send a new agent request to the server.
        '''
        return send_request(*self.build_request("auth", "new_agent", mac_address))

# ---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    server = ServerAPI()
    print(server.get_info())