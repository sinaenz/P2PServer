import socket

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        message = input('please enter the message : \nGilsaMobile,')
        sock.connect(('gilsatech.com', 8080))
        sock.sendall(bytes('GilsaMobile,gateway_no_3,' + message, 'ascii'))
        print(sock.recv(1024))
        sock.close()

