import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect(('127.0.0.1', 8080))

sock.sendall(b'GilsaGateway,gateway_no_3')

print(sock.recv(1024))

try:
    while True:
        data = str(sock.recv(1024), 'ascii').strip()
        if not data:
            break
        print(data)
        sock.send(b'Delivered!')

except KeyboardInterrupt:
    print('connection closed!')
    sock.close()

print('connection closed!')
sock.close()
