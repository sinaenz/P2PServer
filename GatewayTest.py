import socket
import threading
import time


def make_a_gateway(s):

    while True:

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.connect(('127.0.0.1', 8888))

        sock.sendall(bytes('gdevice,%s' % s, 'ascii'))

        print(sock.recv(1024))

        sock.settimeout(None)

        while True:
            data = str(sock.recv(1024), 'ascii').strip()
            print(data)
            if not data:
                print('Connection closed among process!')
                break
            sock.sendall(bytes(data, 'ascii'))

        print('connection closed!')
        sock.close()

for i in [10]:

    th = threading.Thread(target=make_a_gateway, args=(i,), name='Thread number %s' % i)
    th.start()
