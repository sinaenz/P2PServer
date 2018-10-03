import socket
import time
from threading import Thread

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('0.0.0.0', 4000))
sock.listen(10)


def count():
    for i in range(1024):
        print(i)
        time.sleep(1)
        print(((i+1) // 10 + 1) * '\b')


while True:
    current_connection, address = sock.accept()
    while True:
        data = str(current_connection.recv(2048), 'ascii').rstrip()
        print(data)
        t = Thread(target=count, name='salam', daemon=True)
        t.start()

        if data == 'quit' or not data:
            current_connection.shutdown(1)
            t.join()
            current_connection.close()
            break

        elif data == 'stop':
            current_connection.shutdown(1)
            t.join()
            current_connection.close()
            exit()

        elif data:
            current_connection.send(bytes(data, 'ascii'))
