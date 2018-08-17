import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print(sock)

sock.connect(('0.0.0.0', 8080))

sock.sendall(b'GilsaGatewaysalam')

print(sock.recv(1024))

while True:
    data = str(sock.recv(1024), 'ascii').strip()
    print(data)
    sock.send(b'Delivered!')
