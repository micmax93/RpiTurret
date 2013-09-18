from MotionDetector.fast_motion_detector import FastMovementDetector
import time

fmd = FastMovementDetector()

startTime = time.time()

try:
    while True:
        alarmOn = False

        fmd.tryToDetect()

        if fmd.motionFactor > 30:
            alarmOn = True

        print (str(fmd.motionFactor) + " : " + str(fmd.actualAvgDiff))

except KeyboardInterrupt:
    pass
