import socket
import os

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

def prep_send(connection):
    message = input("Enter message to send (type 'send_file filename' to send file): ")

    if message.startswith("send_file"):
        _, file_name = message.split()
        connection.sendall(message.encode('utf-8'))
        send_file(connection, file_name)
    else:
        connection.sendall(message.encode('utf-8'))

def handle_client(connection, address):
    print(f"Connected to {address}")

    while True:
        data = connection.recv(1024)

        if data == b'exit':
            break

        if data.startswith(b'send_file'):
            _, file_name = data.split()
            receive_file(connection, file_name.decode())
            print(f"Received file: {file_name.decode()}")
        else:
            message = data.decode('utf-8')
            print(f"Received message: {message}")
            
        prep_send(connection)

    print("Connection closed")
    connection.close()
    

def start_server():
    host = 'localhost'
    port = 5000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server listening on {host}:{port}")


    connection, address = server_socket.accept()
    handle_client(connection, address)

if __name__ == "__main__":
    start_server()


