import socket
import os
import threading

def receive_file(connection, file_name):
    path_file = os.path.join("filesofsender/", file_name)
    with open(path_file, 'wb') as file:
        while True:
            data = connection.recv(1024)
            if data.endswith(b'<END>'):
                file.write(data[:-len(b'<END>')])  # Write all data except the <END> marker
                break
            file.write(data)

def send_file(connection, file_name):
    with open(file_name, 'rb') as file:
        for data in file:
            connection.sendall(data)
        connection.sendall(b'<END>')
    print(f"File '{file_name}' sent successfully.")

def prep_send(connection, other_connection):
    message = input("Enter message to send (type 'send_file filename' to send file): ")

    if message.startswith("send_file"):
        _, file_name = message.split()
        connection.sendall(message.encode('utf-8'))
        send_file(connection, file_name)
        other_connection.sendall(message.encode('utf-8'))
        send_file(other_connection, file_name)
    else:
        connection.sendall(message.encode('utf-8'))
        other_connection.sendall(message.encode('utf-8'))

def handle_client(connection, address, other_connection):
    print(f"Connected to {address}")

    while True:
        data = connection.recv(1024)

        if data.startswith(b'send_file'):
            _, file_name = data.split()
            receive_file(connection, file_name.decode())
            print(f"Received file: {file_name.decode()}")
            other_connection.sendall(data)
            send_file(other_connection, file_name.decode())
        else:
            other_connection.sendall(data)
            message = data.decode('utf-8')
            print(f"Received message: {message}")
        
        data = other_connection.recv(1024)

        if data.startswith(b'send_file'):
            _, file_name = data.split()
            receive_file(other_connection, file_name.decode())
            print(f"Received file: {file_name.decode()}")
            connection.sendall(data)
            send_file(connection, file_name.decode())
        else:
            connection.sendall(data)
            message = data.decode('utf-8')
            print(f"Received message: {message}")

        # Prepare and send data to the current client again
        prep_send(connection, other_connection)


def start_server():
    host = '192.168.18.159'
    port = 5000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(2)
    print(f"Server listening on {host}:{port}")

    connection_client1, address_client1 = server_socket.accept()
    print(f"Connected to {address_client1} (Client 1)")

    connection_client2, address_client2 = server_socket.accept()
    print(f"Connected to {address_client2} (Client 2)")

    handle_client(connection_client1, address_client1, connection_client2)

if __name__ == "__main__":
    start_server()

