import cv2
import numpy as np
from datetime import datetime
from ImageDescriber import ImageDescriber
from MatcherDescribedImages import MatcherDescribedImages

class ImagesProcessor:
    def __init__(self, img1, img2):
        self.img1 = img1
        self.img2 = img2
        self.mtcDcrImg = None

    def getMatchedPicture(self, withBadPoints = False):
        h1, w1 = self.img1.shape[:2]
        h2, w2 = self.img2.shape[:2]

        p1 = self.mtcDcrImg.matched_p1
        p2 = self.mtcDcrImg.matched_p2
        status = self.mtcDcrImg.status
        H = self.mtcDcrImg.H

        vis = np.zeros((max(h1, h2), w1+w2), np.uint8)
        vis[:h1, :w1] = self.img1
        vis[:h2, w1:w1+w2] = self.img2
        vis = cv2.cvtColor(vis, cv2.COLOR_GRAY2BGR)
        if status is None:
            status = np.ones(len(p1), np.bool_)
        green = (0, 255, 0)
        red = (0, 0, 255)
        for (x1, y1), (x2, y2), inlier in zip(np.int32(p1), np.int32(p2), status):
            col = [red, green][inlier]
            if inlier:
                cv2.line(vis, (x1, y1), (x2+w1, y2), col)
                cv2.circle(vis, (x1, y1), 2, col, -1)
                cv2.circle(vis, (x2+w1, y2), 2, col, -1)
            else:
                if not withBadPoints:
                    continue
                r = 2
                thickness = 3
                cv2.line(vis, (x1-r, y1-r), (x1+r, y1+r), col, thickness)
                cv2.line(vis, (x1-r, y1+r), (x1+r, y1-r), col, thickness)
                cv2.line(vis, (x2+w1-r, y2-r), (x2+w1+r, y2+r), col, thickness)
                cv2.line(vis, (x2+w1-r, y2+r), (x2+w1+r, y2-r), col, thickness)
        return vis

    def ProcessImages(self, withTimeInfo = False):
        surf = cv2.SURF(1000)

        if withTimeInfo:
            startTime = datetime.now()
            print "startTime:", startTime

        imgDcr1 = ImageDescriber(self.img1, surf)
        imgDcr2 = ImageDescriber(self.img2, surf)

        self.mtcDcrImg = MatcherDescribedImages(imgDcr1, imgDcr2)
        self.mtcDcrImg.match()

        if withTimeInfo:
            finishTime = datetime.now()
            print "finished: ", finishTime
            duration = finishTime - startTime
            print "duration: ", duration

    def getMatchedPoints(self):
        if self.mtcDcrImg.zP1 is None:
            self.mtcDcrImg.collectMatchedZippedPoints()
        return self.mtcDcrImg.zP1, self.mtcDcrImg.zP2, self.img1.shape[:2], self.img2.shape[:2]
