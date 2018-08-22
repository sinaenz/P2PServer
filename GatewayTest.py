import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while True:

    sock.connect(('gilsatech.com', 8080))

    sock.sendall(b'GilsaGateway,gateway_no_3')

    print(sock.recv(1024))

    sock.settimeout(None)

    while True:
        data = str(sock.recv(1024), 'ascii').strip()
        if not data:
            print('Connection closed among process!')
            break
        print(data)
        sock.sendall(b'Delivered!')
        print('sent')

    print('connection closed!')
    sock.close()
