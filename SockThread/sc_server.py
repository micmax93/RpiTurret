import socket
import json
from threading import Thread


def empty_callback(alarm, move, noise):
    pass


class Host:
    socket = None
    movement = 0
    noise = 0
    alarm = False
    conn = None
    addr = ''
    update_callback = empty_callback

    def __init__(self, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('127.0.0.1', port))
        self.socket.listen(10)

    def client_loop(self):
        while 1:
            data = self.conn.recv(1024)
            if not data: break
            tab = json.loads(data)
            self.noise = tab['noise']
            self.movement = tab['movement']
            self.alarm = tab['alarm']
            self.update_callback(self.alarm, self.movement, self.noise)
        print "Client ", self.addr, " disconnected"

    def start(self):
        while True:
            conn, addr = self.socket.accept()
            print 'Connected by', addr
            self.conn = conn
            self.addr = addr
            t = Thread(target=self.client_loop)
            t.start()
            t.join()

    def get_movement(self):
        return self.movement

    def get_noise(self):
        return self.noise

    def is_alarmed(self):
        return self.noise

    def set_update_callback(self, callback):
        self.update_callback = callback

#Host(5555).accept_loop()
