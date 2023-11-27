import socket
import select
import chatlib

SERVER_IP = "0.0.0.0"
SERVER_PORT = 5678
MSG_MAX_SIZE = 4096

def print_client_sockets(client_sockets:list):
    for c in client_sockets:
        print('\t',c.getpeername())


def main():
    print("Setting up server...")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen()
    print("Server is ready and listening to new clients...")
    client_sockets = []  # list of connected clients

    while True:
        ready_to_read, ready_to_write, in_error = select.select([server_socket] + client_sockets, [], [])
        for current_socket in ready_to_read:
            if current_socket is server_socket:
                client_socket, client_address = current_socket.accept()
                print(f"New client joined {client_address}")
                client_sockets.append(client_socket)
            else:
                # respond
                pass
            print_client_sockets(client_sockets)

if __name__ == '__main__':
    main()
