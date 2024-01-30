import socket
import sys

def send_request(request):
    """
    Connects to the server, sends a request, receives and prints the response.

    Args:
        request (str): The client's request.

    Returns:
        None
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 12345)

    try:
        client_socket.connect(server_address)
    except ConnectionRefusedError:
        print("Server is not available. Exiting.")
        sys.exit()

    try:
        client_socket.sendall(request.encode('utf-8'))
        response = client_socket.recv(1024)
        if response:
            print(response.decode('utf-8'))
        else:
            print("Server closed the connection.")
    except ConnectionResetError:
        print("Server closed the connection.")
    finally:
        client_socket.close()

def close_client():
    """
    Closes the client gracefully.

    Returns:
        None
    """
    print("\nClosing the client gracefully...")
    sys.exit()

if __name__ == '__main__':
    try:
        while True:
            print("Command: ", end=" ")
            user_input = input().strip()
            if not len(user_input) > 0:
                print("no command entered")
            else:
                send_request(user_input)
    except KeyboardInterrupt:
        close_client()