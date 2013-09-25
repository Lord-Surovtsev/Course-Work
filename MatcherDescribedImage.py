import cv2
import numpy as np

class MatcherDescribedImage:
    def __init__(self, imgDcr1, imgDcr2):
        self.imgDcr1 = imgDcr1
        self.imgDcr2 = imgDcr2
        if self.imgDcr1.kp is None:
            self.imgDcr1.detectAndCompute()
        if self.imgDcr2.kp is None:
            self.imgDcr2.detectAndCompute()
        self.H = None
        self.status = None
        self.matchedIndexes = None

    def match(self, r_threshold = 0.75):
        m = match_bruteforce(self.imgDcr1.desc, self.imgDcr2.desc, r_threshold)
        self.matched_p1 = np.array([self.imgDcr1.kp[i].pt for i, j in m])
        self.matched_p2 = np.array([self.imgDcr2.kp[j].pt for i, j in m])
        if (4 < len(self.matched_p1)) and (4 < len(self.matched_p2)):
            self.H, self.status = cv2.findHomography(self.matched_p1, self.matched_p2, cv2.RANSAC, 5)
#           print '%d / %d  inliers/matched' % (np.sum(self.status), len(self.status))
            print np.sum(self.status), " / ", len(self.status), "  inliers/matched"
        else:
            self.H = None
            self.status = None
            print "status is None"

    def retriveMatchedIndexes(self):
        if self.status is None:
            self.matchedIndexes = range(self.imgDcr1.kp)
            return
        self.matchedIndexes = []
        for i in range(len(self.status)):
            if self.matchedIndexes[i]:
                self.matchedIndexes.append(i)
        return res


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
