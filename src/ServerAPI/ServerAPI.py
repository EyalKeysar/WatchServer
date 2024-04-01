from send_recv import *

class ServerAPI:
    '''
        This class is used by the clients to communicate with the server.
    '''
    def __init__(self):
        self.server_ip = "localhost"
        self.server_port = 2230

    def get_info(self):
        '''
            This method is used to get the information from the server.
        '''
        return self.send_request("fetch_info|")
    
    def login(self, username, password):
        '''
            This method is used to login to the server.
        '''
        return send_request(f"login|{username}|{password}")
    
    
if __name__ == '__main__':
    server = ServerAPI()
    print(server.get_info())