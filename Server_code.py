import socket
import threading

# Dictionary to store account details {account_id: (password, balance)}
accounts = {
    'acc1': ('pass1', 1000),
    'acc2': ('pass2', 500),
    'acc3': ('pass3', 1500),
}

# Lock to prevent simultaneous access to shared resources by multiple threads
lock = threading.Lock()

# Function to handle each client connection
def handle_client(conn, addr):
    print(f"Accepted connection from {addr}")

    # Authenticate client
    authenticated = False
    while not authenticated:
        conn.sendall(b"Enter account ID: ")
        acc_id = conn.recv(1024).decode().strip()
        conn.sendall(b"Enter password: ")
        password = conn.recv(1024).decode().strip()

        if acc_id in accounts and accounts[acc_id][0] == password:
            authenticated = True
        else:
            conn.sendall(b"Invalid credentials. Try again.\n")

    # Main loop to serve the authenticated client
    while True:
        try:
            conn.sendall(b"\nAvailable operations:\n1. Check Balance\n2. Deposit\n3. Withdraw\n4. Exit\nEnter your choice: ")
            choice = conn.recv(1024).decode().strip()

            if choice == '1':  # Check Balance
                balance = accounts[acc_id][1]
                conn.sendall(f"Your balance is: {balance}\n".encode())

            elif choice == '2':  # Deposit
                conn.sendall(b"Enter amount to deposit: ")
                amount = int(conn.recv(1024).decode().strip())
                with lock:
                    accounts[acc_id] = (accounts[acc_id][0], accounts[acc_id][1] + amount)
                conn.sendall(f"Amount {amount} deposited successfully.\n".encode())

            elif choice == '3':  # Withdraw
                conn.sendall(b"Enter amount to withdraw: ")
                amount = int(conn.recv(1024).decode().strip())
                with lock:
                    if accounts[acc_id][1] >= amount:
                        accounts[acc_id] = (accounts[acc_id][0], accounts[acc_id][1] - amount)
                        conn.sendall(f"Amount {amount} withdrawn successfully.\n".encode())
                    else:
                        conn.sendall(b"Insufficient balance.\n")

            elif choice == '4':  # Exit
                break

            else:
                conn.sendall(b"Invalid choice. Try again.\n")

        except Exception as e:
            print(f"Exception: {e}")
            break

    # Send final balance to client and close connection
    final_balance = accounts[acc_id][1]
    conn.sendall(f"Session ended. Final balance: {final_balance}\n".encode())
    print(f"Closed connection from {addr}")
    conn.close()

# Main function to run the server
def main():
    host = '127.0.0.1'
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    try:
        while True:
            conn, addr = server_socket.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()

    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
