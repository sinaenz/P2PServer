import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect(('gilsatech.com', 8080))

sock.sendall(b'GilsaGateway,gateway_no_3')

print(sock.recv(1024))

try:
    while True:
        data = str(sock.recv(1024), 'ascii').strip()
        print(data)
        sock.send(b'Delivered!')

except KeyboardInterrupt:
    sock.close()
