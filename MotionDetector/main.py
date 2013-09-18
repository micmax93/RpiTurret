import cv
import time


class TimeUtil:
    @staticmethod
    def getCurrentTime():
        return int(round(time.time() * 1000))


class Main:
    lastReferenceCaptureTime = None
    referencedImage = None
    capture = None
    frameSize = None

    def __init__(self):
        #init camera
        self.capture = cv.CaptureFromCAM(0)
        self.captureReferenceImage()

    def getFrame(self):
        return cv.QueryFrame(self.capture)

    def captureReferenceImage(self):
        frame = self.getFrame()
        self.frameSize = cv.GetSize(frame)
        self.referencedImage = cv.CloneImage(frame)
        cv.Smooth(self.referencedImage, self.referencedImage, cv.CV_GAUSSIAN, 9, 0)
        self.lastReferenceCaptureTime = TimeUtil.getCurrentTime()

    def run(self):
        while 1:
            currentFrame = self.getFrame()
            if self.isReferenceUpdateTime():
                self.captureReferenceImage()
            diff = self.getDiff(cv.CloneImage(currentFrame))
            motionDetected = self.isMotionDetected(diff)
            print motionDetected

    def isReferenceUpdateTime(self):
        #capture reference img every 5 secs
        return TimeUtil.getCurrentTime() - self.lastReferenceCaptureTime > 500

    def getDiff(self, frame):
        diffImg = cv.CloneImage(self.referencedImage)
        cv.Smooth(frame, frame, cv.CV_GAUSSIAN, 9, 0)
        cv.AbsDiff(self.referencedImage, frame, diffImg)

        greyImg = cv.CreateImage(cv.GetSize(frame), cv.IPL_DEPTH_8U, 1)

        cv.CvtColor(diffImg, greyImg, cv.CV_RGB2GRAY)
        cv.Threshold(greyImg, greyImg, 30, 255, cv.CV_THRESH_BINARY)
        cv.Dilate(greyImg, greyImg, None, 9)
        cv.Erode(greyImg, greyImg, None, 5)

        # return greyImg
        return greyImg

    def isMotionDetected(self, diff):
        avg = cv.Avg(diff)
        return avg[0]
        #return avg[0] > 20

if __name__ == "__main__":
    t = Main()
    t.run()
