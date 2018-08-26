import threading
import socketserver
import logging
import time
import jdatetime


# Config Logger
# TODO: Config more files for logging
logging.basicConfig(filename='P2PServer.log', level=logging.DEBUG, format='%(message)s')
logging.Formatter.converter = jdatetime.datetime.now
logger = logging.getLogger()


# is created for each connection
class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    # {'GatewayID': GateWaySocket, ...}
    openGatewayQueue = {}
    #
    openMobileQueue = {}

    def handle(self):
        data = str(self.request.recv(1024), 'ascii')

        # if request is from a gateway (if its just a packet to keep the session alive)
        if data.startswith('GG'):

            # find gateway name
            name = data.split(',')[1].rstrip()

            # check if gateway has a live connection
            try:
                del self.openGatewayQueue[name]
            except:
                pass

            # set current thread name and save the connection
            cur_thread = threading.current_thread()
            cur_thread.setName(name)
            self.request.sendall(bytes('OK,{}'.format(name), 'ascii'))
            self.openGatewayQueue[name] = self.request

            # keep thread alive!
            while True:

                # Set connection timeout here!
                # (max acceptable time without receiving packets)
                self.request.settimeout(100)

                try:
                    data = str(self.request.recv(1024), 'ascii').strip()

                    if not data:
                        del self.openGatewayQueue[name]
                        logger.info('{} - Thread {} killed by peer!'.format(
                            jdatetime.datetime.now().strftime('%d %B %Y %H:%M:%S'),
                            cur_thread.name, )
                        )
                        return

                    mobile, response = data.split(',')[:2]
                    mobile = self.openMobileQueue[mobile]
                    mobile.sendall(bytes(response, 'ascii'))

                # if timeout occurred
                except Exception as error:
                    del self.openGatewayQueue[name]
                    logger.info('{} - Thread {} {}'.format(
                        jdatetime.datetime.now().strftime('%d %B %Y %H:%M:%S'),
                        cur_thread.name,
                        error)
                    )
                    return
                    # if connection closed by a peer

        # if request is from a mobile device (if its a command)
        # GM,GatewayID,MobileID,Command
        elif data.startswith('GM'):

            gateway, mobile, command = [x.rstrip() for x in data.split(',')[1:4]]
            self.openMobileQueue[mobile] = self.request

            gateway = self.openGatewayQueue[gateway]
            gateway.sendall(bytes(','.join([mobile, command]), 'ascii'))

            response = self.request.recv(1024)
            self.request.sendall(response)

            del self.openMobileQueue[mobile]


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":

    # Port 0 means to select an arbitrary unused port
    HOST, PORT = '0.0.0.0', 8080

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)

    server.allow_reuse_address = True

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
                [element for element in ThreadedTCPRequestHandler.openGatewayQueue])
            )
            logger.info('{} - {}'.format(
                jdatetime.datetime.now().strftime('%d %B %Y %H:%M:%S'),
                [element for element in ThreadedTCPRequestHandler.openMobileQueue]))

            # print('{} - {}'.format(
            #     jdatetime.datetime.now().strftime('%d %B %Y %H:%M:%S'),
            #     [element for element in ThreadedTCPRequestHandler.openGatewayQueue]))

            time.sleep(5)
    except :
        server.shutdown()

