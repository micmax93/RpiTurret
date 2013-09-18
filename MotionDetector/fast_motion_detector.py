import cv
import time


class FastMovementDetector:
    capture = None
    previous = None
    current = None
    lastTime = None
    startTime = None
    threshold = 20
    motionFactor = 0
    actualAvgDiff = 0

    def __init__(self):
        self.capture = cv.CaptureFromCAM(0)
        self.previous = self.getGrayImage(cv.GetSize(cv.QueryFrame(self.capture)))
        self.lastTime = time.time()
        self.startTime = time.time()

    def getFrame(self):
        return cv.QueryFrame(self.capture)

    def getGrayImage(self, size):
        img = cv.CreateImage(size, cv.IPL_DEPTH_8U, 1)
        cv.CvtColor(cv.CloneImage(self.getFrame()), img, cv.CV_RGB2GRAY)
        return img

    def getMotionFactor(self, avg):
        if avg >= self.threshold:
            return 100
        else:
            return round((avg/self.threshold)*100)

    def tryToDetect(self):
        if time.time() - self.lastTime >= 0.5:
            self.current = self.getGrayImage(cv.GetSize(self.previous))
            diffImg = cv.CloneImage(self.previous)
            cv.AbsDiff(self.previous, self.current, diffImg)
            avg = cv.Avg(diffImg)

            self.previous = cv.CloneImage(self.current)
            self.lastTime = time.time()

            self.motionFactor = self.getMotionFactor(avg)
            self.actualAvgDiff = avg
        else:
            self.getFrame()