import socket


def send_request(server_socket, request, *args):
    '''
        This function is used to send the request to the server, with optional args.
    '''
    server_socket.sendall(request.encode())
    response = server_socket.recv(1024).decode()
    return response