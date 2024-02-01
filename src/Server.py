import socket
import threading
import re
from Main import *

def handle_client(client_socket):
    """
    Handles a client connection by receiving requests, processing them, and sending back responses.

    Args:
        client_socket (socket.socket): The socket object representing the client connection.

    Returns:
        None
    """
    while True:
        request = client_socket.recv(1024).decode('utf-8')
        if not request:
            break

        response = process_request(request)
        client_socket.sendall(response.encode('utf-8'))

    client_socket.close()

def process_request(request):
    """
    Processes a client request and returns the corresponding response.

    Args:
        request (str): The client's request.

    Returns:
        str: The response to be sent back to the client.
    """
    userInput = request.strip()

    # Check for "ASK" command
    if userInput == "ASK":
        return ask()

    # Check for no IP address entered
    userInput = userInput.split(" ", 1)
    if not len(userInput) == 2:
        return "Invalid command"

    # Check for valid IP address format
    command, ipInputted = userInput
    if not re.search(r"^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$", ipInputted):
        return "Invalid IP address"

    match command:
        case "RENEW":
            return renew(ipInputted)
        case "RELEASE":
            return release(ipInputted)
        case "STATUS":
            return status(ipInputted)
        case _:
            return "Invalid command"

def start_server():
    """
    Starts the server and listens for incoming client connections.

    Returns:
        None
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 12345)
    server_socket.bind(server_address)
    server_socket.listen(5)
    print('Server is listening on {}:{}'.format(*server_address))

    while True:
        client_socket, client_address = server_socket.accept()
        print('Accepted connection from {}:{}'.format(*client_address))
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == '__main__':
    start_server()