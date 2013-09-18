from RpiPinout.securipi import SecuriPi
import UsbToken.validation as token
from MotionDetector.fast_motion_detector import FastMovementDetector
import time

s = SecuriPi()
s.setup()
s.token_callback = token.is_valid_token

fmd = FastMovementDetector()

startTime = time.time()

try:

    while time.time() - startTime < 5:
        pass

    print("\n\t>> START!")

    while True:
        alarmOn = False

        fmd.tryToDetect()

        if fmd.motionFactor > 30:
            alarmOn = True

        s.update(alarm=alarmOn, mov_lvl=fmd.motionFactor, noise_lvl=0)
except KeyboardInterrupt:
    pass
