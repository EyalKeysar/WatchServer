import socket
import threading

def send_request(server_socket, request):
    '''
        This function is used to send the request to the server, with optional args.
    '''
    # threading.Thread(target=server_socket.sendall, args=(request.encode(),)).start()
    
    server_socket.sendall(request.encode())
    response = server_socket.recv(1024).decode()
    return response

def send_request_blocking(server_socket, request):
    '''
        This function is used to send the request to the server, with optional args.
    '''
    server_socket.sendall(request.encode())
    response = server_socket.recv(1024).decode()
    return response