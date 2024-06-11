import socket

def main():
    host = '127.0.0.1'
    port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    try:
        # Authentication
        authenticated = False
        while not authenticated:
            print(client_socket.recv(1024).decode(), end='')
            acc_id = input()
            client_socket.sendall(acc_id.encode())
            print(client_socket.recv(1024).decode(), end='')
            password = input()
            client_socket.sendall(password.encode())

            response = client_socket.recv(1024).decode()
            if "Invalid" not in response:
                authenticated = True
            print(response)

        # Main operations
        while True:
            print(client_socket.recv(1024).decode(), end='')
            choice = input()
            client_socket.sendall(choice.encode())

            if choice == '4':  # Exit
                break

            response = client_socket.recv(1024).decode()
            print(response)

            if "Final balance" in response:
                break

            if choice in ['2', '3']:
                print(client_socket.recv(1024).decode(), end='')
                amount = input()
                client_socket.sendall(amount.encode())
                response = client_socket.recv(1024).decode()
                print(response)

    finally:
        client_socket.close()

if __name__ == "__main__":
    main()