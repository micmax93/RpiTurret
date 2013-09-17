import cv
import time


class MovementDetector:
    capture = None
    previous = None
    current = None
    lastTime = None
    startTime = None

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

    def run(self):
        while True:
            if time.time() - self.lastTime >= 0.5:
                self.current = self.getGrayImage(cv.GetSize(self.previous))
                diffImg = cv.CloneImage(self.previous)
                cv.AbsDiff(self.previous, self.current, diffImg)
                avg = cv.Avg(diffImg)
                print "\t" + str(avg[0] > 5)

                self.previous = cv.CloneImage(self.current)
                self.lastTime = time.time()
            else:
                self.getFrame()

            if time.time() - self.startTime > 20:
                break

        print "\n>> END <<\n"

if __name__ == "__main__":
    md = MovementDetector()
    md.run()