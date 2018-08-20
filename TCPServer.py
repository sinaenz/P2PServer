import threading
import socketserver
import logging
import time
import jdatetime


# Config Logger
logging.basicConfig(filename='P2PServer.log', level=logging.DEBUG, format='%(message)s')
logging.Formatter.converter = jdatetime.datetime.now
logger = logging.getLogger()


# is created for each connection
class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    openConnections = {}

    def handle(self):
        data = str(self.request.recv(1024), 'ascii')
        # if request is from a gateway (if its just a packet to keep the session alive)
        if data.startswith('GilsaGateway'):
            # find gateway name
            name = data.split(',')[1]
            # check if gateway has a live connection
            if name in [thread.name for thread in threading.enumerate()]:
                return
            # set current thread name and save the connection
            cur_thread = threading.current_thread()
            cur_thread.setName(name)
            self.request.sendall(bytes('OK,{}'.format(name), 'ascii'))
            self.openConnections[name] = self.request

            while True:
                data = str(self.request.recv(1024), 'ascii').strip()
                print(data)
                # if connection closed by a peer
                if not data:
                    del self.openConnections[name]
                    logger.info('{} - Thread {} killed!'.format(
                        jdatetime.datetime.now().strftime('%d %B %Y %H:%M:%S'),
                        cur_thread.name)
                    )
                    return

        # if request is from a mobile device (if its a command)
        elif data.startswith('GilsaMobile'):
            name, command = data.split(',')[1], data.split(',')[2]
            connection = self.openConnections[name]
            connection.sendall(bytes(command, 'ascii'))
            response = connection.recv(1024)
            self.request.sendall(response)

        else:
            return


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":

    logger = logging.getLogger('TCP Log')
    # Port 0 means to select an arbitrary unused port
    HOST, PORT = '0.0.0.0', 8080

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)

    ip, port = server.server_address

    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever, name='ServerThread')

    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    logger.info("{} - Server running in thread: {}".format(
        jdatetime.datetime.now().strftime('%d %B %Y %H:%M:%S'),
        server_thread.name)
    )
    try:
        while True:
            logger.info('{} - {}'.format(
                jdatetime.datetime.now().strftime('%d %B %Y %H:%M:%S'),
                [element for element in ThreadedTCPRequestHandler.openConnections])
            )
            time.sleep(60)
    except KeyboardInterrupt:
        server.shutdown()

