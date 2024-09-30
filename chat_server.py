import socket
import threading

# Define server host and port
HOST = '127.0.0.1'  # Localhost
PORT = 12345  # Port to listen on

# List to keep track of connected clients
clients = []
nicknames = []


# Function to broadcast messages to all clients
def broadcast(message):
    for client in clients:
        client.send(message)


# Function to handle client connection
def handle_client(client):
    while True:
        try:
            # Receive message from client
            message = client.recv(1024)
            broadcast(message)
        except:
            # Remove client if it disconnects
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat!'.encode('utf-8'))
            nicknames.remove(nickname)
            break


# Function to start the server
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f'Server started on {HOST}:{PORT}')

    while True:
        # Accept client connection
        client, address = server.accept()
        print(f'Connected with {str(address)}')

        # Request and store nickname
        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of the client is {nickname}')
        broadcast(f'{nickname} joined the chat!'.encode('utf-8'))
        client.send('Connected to the server!'.encode('utf-8'))

        # Start a new thread to handle the client
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


if __name__ == "__main__":
    start_server()
