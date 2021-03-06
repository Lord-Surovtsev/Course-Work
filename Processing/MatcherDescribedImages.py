import cv2
import numpy as np

class MatcherDescribedImages:
    def __init__(self, imgDcr1, imgDcr2):
        self.imgDcr1 = imgDcr1
        self.imgDcr2 = imgDcr2
        if self.imgDcr1.kp is None:
            self.imgDcr1.detectAndCompute()
        if self.imgDcr2.kp is None:
            self.imgDcr2.detectAndCompute()
        self.bruteForceIndexes = None
        self.H = None
        self.status = None
        self.matchedIndexes = None
        self.zP1 = None
        self.zP2 = None
        self.descriptorsIndexes = None
        self.descriptors_p1 = None
        self.descriptord_p2 = None

    def match(self, r_threshold = 0.75):
        self.bruteForceIndexes = match_bruteforce(self.imgDcr1.desc, self.imgDcr2.desc, r_threshold)
        self.matched_p1 = np.array([self.imgDcr1.kp[i].pt for i, j in self.bruteForceIndexes])
        self.matched_p2 = np.array([self.imgDcr2.kp[j].pt for i, j in self.bruteForceIndexes])
        print "matchedLen ", len(self.matched_p1)
        if (4 < len(self.matched_p1)) and (4 < len(self.matched_p2)):
            self.H, self.status = cv2.findHomography(self.matched_p1, self.matched_p2, cv2.RANSAC, 5)
#           print '%d / %d  inliers/matched' % (np.sum(self.status), len(self.status))
            print np.sum(self.status), " / ", len(self.status), "  inliers/matched"
        else:
            self.H = None
            self.status = None
            print "status is None"

    def collectMatchedIndexes(self):
        if self.matched_p1 is None:
            self.mathc()
        if self.status is None:
            self.matchedIndexes = range(len(self.matched_p1))
            return
        self.matchedIndexes = []
        for i in range(len(self.status)):
            if self.status[i]:
                self.matchedIndexes.append(i)

    def collectDescriptorsIndexes(self):
        if self.matched_p1 is None:
            self.match()
        if self.status is None:
            self.descriptorsIndexes = self.bruteForceIndexes
            return
        self.descriptorsIndexes = []
        for i in range(len(self.status)):
            if self.status[i]:
                self.descriptorsIndexes.append(self.bruteForceIndexes[i])

    def collectMatchedZippedPoints(self):
        self.zP1 = []
        self.zP2 = []

        if self.matchedIndexes is None:
            self.collectMatchedIndexes()

        dx1 = -1 * self.imgDcr1.img.shape[:2][1] / 2
        dy1 = -1 * self.imgDcr1.img.shape[:2][0] / 2

        dx2 = -1 * self.imgDcr2.img.shape[:2][1] / 2
        dy2 = -1 * self.imgDcr2.img.shape[:2][0] / 2

        for i in range(len(self.matchedIndexes)):
            self.zP1.append([-1*(self.matched_p1[i][0] + dx1) / dx1 / 2, -1*(self.matched_p1[i][1] + dy1)/dy1 / 2, 1])
            self.zP2.append([-1*(self.matched_p2[i][0] + dx2) / dx2 / 2, -1*(self.matched_p2[i][1] + dy2)/dy2 / 2, 1])

    def collectMatchedDescriptors(self):
        self.descriptors_p1 = []
        self.descriptors_p2 = []

        if self.descriptorsIndexes is None:
            self.collectDescriptorsIndexes()

        for i1, i2 in self.descriptorsIndexes:
            self.descriptors_p1.append((self.imgDcr1.desc[i1], self.imgDcr2.desc[i2]))

def match_bruteforce(desc1, desc2, r_threshold = 0.75):
    res = []
    for i in xrange(len(desc1)):
        dist = anorm( desc2 - desc1[i] )
        n1, n2 = dist.argsort()[:2]
        r = dist[n1] / dist[n2]
        if r < r_threshold:
            res.append((i, n1))
    return np.array(res)

def anorm2(a):
    return (a*a).sum(-1)

def anorm(a):
    return np.sqrt( anorm2(a) )
