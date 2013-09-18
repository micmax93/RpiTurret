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
            return sum / len(self.value_list)


def empty_callback(alarm, move, noise):
    pass


class Host:
    socket = None
    movement = Accumulator(10)
    noise = Accumulator(10)
    update_callback = empty_callback

    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        self.socket.listen(10)

    def client_loop(self, conn, addr):
        while 1:
            data = conn.recv(1024)
            if not data: break
            tab = json.loads(data)
            self.noise.add_item(tab['noise'])
            self.movement.add_item(tab['movement'])
            self.update_callback(tab['alarm'], self.movement.get_value(), self.noise.get_value())
        print "Client ", addr, " disconnected"

    def start(self):
        while True:
            conn, addr = self.socket.accept()
            print 'Connected by', addr
            Thread(target=self.client_loop, args=(conn, addr)).start()

    def get_movement(self):
        return self.movement.get_value()

    def get_noise(self):
        return self.noise.get_value()

    def is_alarmed(self):
        return self.noise.get_value()

    def set_update_callback(self, callback):
        self.update_callback = callback

#Host(5555).accept_loop()
