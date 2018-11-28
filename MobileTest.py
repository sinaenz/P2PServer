import socket

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(('127.0.0.1', 8888))
        message = input('please enter the message : \n')
        sock.sendall(bytes('gmobile,2,1,' + message, 'ascii'))
        print(sock.recv(1024))
