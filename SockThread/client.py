# Echo client program
import socket
import json
import time


class Client:
    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))

    def send(self, noise, movement):
        msg = json.dumps({'noise': noise, 'movement': movement})
        self.socket.sendall(msg)

    def close(self):
        self.socket.close()


c = Client('192.168.1.101', 5555)
c.send(15, 23)
time.sleep(1)
c.send(45, 66)
time.sleep(1)
c.send(67, 34)
time.sleep(1)
c.send(89, 11)
c.close()
