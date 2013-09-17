# Echo server program
import socket
import json
from threading import Thread

class Accumulator:
    value_list = [0]
    max_count = 1
    type = 'sum'

    def __init__(self, size, type='avg'):
        self.max_count = size
        self.type = type

    def add_item(self, val):
        self.value_list.insert(0, val)
        if len(self.value_list) <= self.max_count:
            pass
        elif len(self.value_list) == self.max_count + 1:
            self.value_list.pop()
        else:
            raise Exception("too much items in array")

    def get_value(self):
        sum = 0
        for val in self.value_list:
            sum += val
        if self.type == 'sum':
            return sum
        elif self.type == 'avg':
            return sum / self.max_count


class Host:
    socket = None
    movement = Accumulator(10)
    noise = Accumulator(10)
    conn = None
    addr = ''

    def __init__(self, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('127.0.0.1', port))
        self.socket.listen(10)

    def client_loop(self):
        while 1:
            data = self.conn.recv(1024)
            if not data: break
            tab = json.loads(data)
            self.noise.add_item(tab['noise'])
            self.movement.add_item(tab['movement'])
        print "Client ", self.addr, " disconnected"

    def start(self):
        conn, addr = self.socket.accept()
        print 'Connected by', addr
        self.conn = conn
        self.addr = addr
        Thread(target=self.client_loop).start()

    def get_movement(self):
        return self.movement.get_value()

    def get_noise(self):
        return self.noise.get_value()


#Host(5555).accept_loop()
