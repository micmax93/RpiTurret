from RpiPinout.securipi import SecuriPi
import UsbToken.validation as token
from MotionDetector.fast_motion_detector import FastMovementDetector

s = SecuriPi()
s.setup()
s.token_callback = token.is_valid_token

fmd = FastMovementDetector()

try:

    for i in range(5):
        fmd.tryToDetect()

    while True:
        alarmOn = False

        fmd.tryToDetect()

        if fmd.motionFactor > 30:
            alarmOn = True

        s.update(alarm=alarmOn, mov_lvl=fmd.motionFactor, noise_lvl=0)
except KeyboardInterrupt:
    pass
