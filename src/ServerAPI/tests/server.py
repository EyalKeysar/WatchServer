import socket
import s_socket

def start_secure_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        tls_protocol = s_socket.TLSProtocol(client_socket)
        tls_protocol.server_handshake()

        handle_client(client_socket, tls_protocol)

def handle_client(client_socket, tls_protocol):
    while True:
        decrypted_data = tls_protocol.receive()
        if not decrypted_data:
            continue
        print("Received:", decrypted_data)
        tls_protocol.send(decrypted_data)


    s_socket.close(client_socket)

if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 12345
    start_secure_server(HOST, PORT)
