# Echo server program
import socket
import json
from threading import Thread


class ClientSock:
    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr

    def recv_loop(self):
        while 1:
            data = self.conn.recv(1024)
            if not data: break
            tab = json.loads(data)
            print 'Noise value ', tab['noise']
            print 'Movement value ', tab['movement']
        print "Client ", self.addr, " disconnected"


class Host:
    socket = None

    def __init__(self, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('127.0.0.1', port))
        self.socket.listen(10)

    def accept(self):
        conn, addr = self.socket.accept()
        print 'Connected by', addr
        client = ClientSock(conn, addr)
        Thread(target=client.recv_loop).start()

    def accept_loop(self):
        try:
            while 1:
                self.accept()
        except KeyboardInterrupt:
            print "Server out\n"
            self.socket.close()


Host(5555).accept_loop()
