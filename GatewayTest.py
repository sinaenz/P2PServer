import socket
import threading
import time


def make_a_gateway(s):
    while True:

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, True)

        sock.connect(('p2p.gilsatech.com', 8080))

        sock.sendall(bytes('GG,g%s' % s, 'ascii'))

        print(sock.recv(1024))

        sock.settimeout(None)

        while True:
            data = str(sock.recv(1024), 'ascii').strip()
            print(data)
            if not data:
                print('Connection closed among process!')
                break
            time.sleep(1)
            sock.sendall(b'GM,g4,m3,Salaaaaam')

        print('connection closed!')
        sock.close()

for i in range(1):

    th = threading.Thread(target=make_a_gateway, args=(i,), name='Thread number %s' % i)
    th.start()
