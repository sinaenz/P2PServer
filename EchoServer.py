import socket


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('0.0.0.0', 4000))
sock.listen(10)

while True:
    current_connection, address = sock.accept()
    while True:
        data = str(current_connection.recv(2048), 'ascii').rstrip()
        print(data)

        if data == 'quit':
            current_connection.shutdown(1)
            current_connection.close()
            break

        elif data == 'stop':
            current_connection.shutdown(1)
            current_connection.close()
            exit()

        elif data:
            current_connection.send(bytes(data, 'ascii'))
