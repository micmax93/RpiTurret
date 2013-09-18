# Echo client program
import socket
import json
import time


class Client:
    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))

    def send(self, alarm, noise, movement):
        msg = json.dumps({'alarm': alarm, 'noise': noise, 'movement': movement})
        self.socket.sendall(msg)

    def close(self):
        self.socket.close()


c = Client('127.0.0.1', 5555)
c.send(False, 15, 23)
time.sleep(1)
c.send(False, 45, 66)
time.sleep(1)
c.send(False, 67, 34)
time.sleep(1)
c.send(True, 89, 11)
c.close()
c.send(True, 0, 0)
c.close()
