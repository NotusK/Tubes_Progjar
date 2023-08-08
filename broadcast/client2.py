import socket
import os

def send_file(connection, file_name):
    with open(file_name, 'rb') as file:
        for data in file:
            connection.sendall(data)
        connection.sendall(b'<END>')
    print(f"File '{file_name}' sent successfully.")

def receive_file(connection, file_name):
    path_file = os.path.join("file2/", file_name)
    with open(path_file, 'wb') as file:
        while True:
            data = connection.recv(1024)
            if data.endswith(b'<END>'):
                file.write(data[:-len(b'<END>')])  # Write all data except the <END> marker
                break
            file.write(data)

def start_client():
    host = 'localhost'
    port = 5000

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print(f"Connected to server at {host}:{port}")

    while True:
        data = client_socket.recv(1024)

        if data.startswith(b'send_file'):
            _, file_name = data.split()
            receive_file(client_socket, file_name.decode())
            print(f"Received file: {file_name.decode()}")
        else:
            message = data.decode('utf-8')
            print(f"Received message: {message}")

        message = input("Enter message to send (type 'send_file filename' to send file): ")

        if message.startswith('send_file'):
            _, file_name = message.split()
            client_socket.sendall(message.encode('utf-8'))
            send_file(client_socket, file_name)
        else:
            client_socket.sendall(message.encode('utf-8'))

        data = client_socket.recv(1024)

        if data.startswith(b'send_file'):
            _, file_name = data.split()
            receive_file(client_socket, file_name.decode())
            print(f"Received file: {file_name.decode()}")
        else:
            message = data.decode('utf-8')
            print(f"Received message: {message}")

if __name__ == "__main__":
    start_client()

