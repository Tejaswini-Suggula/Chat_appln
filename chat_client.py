import socket
import threading

# Define the host and port to connect to
HOST = '127.0.0.1'  # Server IP address (localhost in this case)
PORT = 12345        # Port the server is running on

# Function to receive messages from the server
def receive_messages():
    while True:
        try:
            # Receive message from server
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            # Handle any connection errors
            print('An error occurred!')
            client.close()
            break

# Function to send messages to the server
def send_messages():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('utf-8'))

# Connect to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Request nickname
nickname = input('Choose your nickname: ')

# Start threads for receiving and sending messages
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

send_thread = threading.Thread(target=send_messages)
send_thread.start()
