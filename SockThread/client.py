# Echo client program
import socket
import json
import time


class Client:
    movement = 0
    noise = 0
    alarm = False

    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))

    def update(self, alarm=None, noise=None, movement=None):
        if alarm is not None:
            self.alarm = alarm
        if noise is not None:
            self.noise = noise
        if movement is not None:
            self.movement = movement
            #self.send()

    def update_movement(self, val):
        self.movement = val
        if val == 100:
            self.alarm = True
            #self.send()

    def update_noise(self, val):
        self.noise = val
        if val == 100:
            self.alarm = True
            #self.send()

    def send(self):
        data = {'alarm': self.alarm, 'noise': self.noise, 'movement': self.movement}
        msg = json.dumps(data)
        self.socket.sendall(msg)
        self.alarm = (self.movement == 100) or (self.noise == 100)

    def close(self):
        self.socket.close()

#
# c = Client('192.168.1.12', 5555)
# c.update(False, 15, 23)
# time.sleep(1)
# c.update(False, 45, 66)
# time.sleep(1)
# c.update(False, 67, 34)
# time.sleep(1)
# c.update(True, 89, 11)
# time.sleep(1)
# c.update(True, 0, 0)
# c.close()
