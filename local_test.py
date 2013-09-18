from RpiPinout.securipi import SecuriPi
#import UsbToken.validation as token
#from MotionDetector.fast_motion_detector import FastMovementDetector
import time

s = SecuriPi()
s.setup()
#s.token_callback = token.is_valid_token

#fmd = FastMovementDetector()

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    pass
