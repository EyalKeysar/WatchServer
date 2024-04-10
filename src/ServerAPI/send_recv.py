import socket


def send_request(request, *args):
    '''
        This function is used to send the request to the server, with optional args.
    '''
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("localhost", 2230))
    client_socket.sendall(request.encode())
    response = client_socket.recv(1024).decode()
    client_socket.close()
    return response