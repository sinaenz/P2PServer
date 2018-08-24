import socket

while True:

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.connect(('localhost', 8080))

    sock.sendall(b'GG,g3')

    print(sock.recv(1024))

    sock.settimeout(100)

    while True:
        data = str(sock.recv(1024), 'ascii').strip()
        if not data:
            print('Connection closed among process!')
            break
        print(data)
        sock.sendall(bytes(data, 'ascii'))
        print('looped')

    print('connection closed!')
    sock.close()
