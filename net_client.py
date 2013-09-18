from SockThread.client import Client
from NoiseDetector.noise_detect import NoiseDetect
from MotionDetector.main import MotionDetector
from threading import Thread
import time

c = Client('192.168.1.12', 5555)

n = NoiseDetect()
n.noise_callback = c.update_noise

m = MotionDetector()
m.move_callback = c.update_movement

Thread(target=n.run).start()
Thread(target=m.run).start()

while True:
    #time.sleep(0.001)
    c.send()