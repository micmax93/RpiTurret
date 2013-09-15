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
    windowNameDiff = "Camera capture diff"
    windowNameReference = "Camera capture reference"
    windowCurrent = "Camera capture current"

    def __init__(self):
        #init camera
        self.capture = cv.CaptureFromCAM(0)
        cv.NamedWindow(self.windowNameReference, 1)
        cv.NamedWindow(self.windowCurrent, 1)
        cv.NamedWindow(self.windowNameDiff, 1)
        cv.MoveWindow(self.windowNameReference, 50, 50)
        cv.MoveWindow(self.windowCurrent, 500, 600)
        cv.MoveWindow(self.windowNameDiff, 1000, 50)
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

        while True:
            currentFrame = self.getFrame()

            if self.isReferenceUpdateTime():
                self.captureReferenceImage()

            diff = self.getDiff(cv.CloneImage(currentFrame))
            motionDetected = self.isMotionDetected(diff)
            print motionDetected

            cv.ShowImage(self.windowCurrent, currentFrame)
            cv.ShowImage(self.windowNameReference, self.referencedImage)
            cv.ShowImage(self.windowNameDiff, diff)

            # Listen for ESC key
            c = cv.WaitKey(7) % 0x100
            if c == 27:
                break

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
        # get average color array for whole image
        avg = cv.Avg(diff)
        #it's grey so we only need first channel
        return avg[0] > 0.25


if __name__ == "__main__":
    t = Main()
    t.run()