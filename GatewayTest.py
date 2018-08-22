import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect(('164.132.81.148', 8080))

sock.sendall(b'GilsaGateway,gateway_no_3')

print(sock.recv(1024))

while True:
    data = str(sock.recv(1024), 'ascii').strip()
    if not data:
        print('Connection closed among process!')
        break
    print(data)
    sock.send(b'Delivered!')

print('connection closed!')
sock.close()
