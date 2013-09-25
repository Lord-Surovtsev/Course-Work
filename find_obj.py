import cv2
import numpy as np
from functools import partial
from datetime import datetime
from ImageDescriber import ImageDescriber
from MatcherDescribedImage import MatcherDescribedImage

help_message = '''SURF image match 

USAGE: findobj.py [ <image1> <image2> ]
'''

def draw_match(img1, img2, p1, p2, status = None, H = None):
    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]
    vis = np.zeros((max(h1, h2), w1+w2), np.uint8)
    vis[:h1, :w1] = img1
    vis[:h2, w1:w1+w2] = img2
    vis = cv2.cvtColor(vis, cv2.COLOR_GRAY2BGR)
    '''
    if H is not None:
        corners = np.float32([[0, 0], [w1, 0], [w1, h1], [0, h1]])
        corners = np.int32( cv2.perspectiveTransform(corners.reshape(1, -1, 2), H).reshape(-1, 2) + (w1, 0) )
        cv2.polylines(vis, [corners], True, (255, 255, 255))
    '''
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
            continue
            r = 2
            thickness = 3
            cv2.line(vis, (x1-r, y1-r), (x1+r, y1+r), col, thickness)
            cv2.line(vis, (x1-r, y1+r), (x1+r, y1-r), col, thickness)
            cv2.line(vis, (x2+w1-r, y2-r), (x2+w1+r, y2+r), col, thickness)
            cv2.line(vis, (x2+w1-r, y2+r), (x2+w1+r, y2-r), col, thickness)
    return vis

def ProcessImages(img1, img2):  
    surf = cv2.SURF(1000)

    startTime = datetime.now()
    print "starting: ", startTime
    imgDcr1 = ImageDescriber(img1, surf)
    imgDcr2 = ImageDescriber(img2, surf)
    
    mtcDcrImg = MatcherDescribedImage(imgDcr1, imgDcr2)
    mtcDcrImg.match()    

#    print 'img1 - %d features, img2 - %d features' % (len(kp1), len(kp2))
#    print 'bruteforce match:',
    finishTime = datetime.now()
    print "finished: ", finishTime
    duration = finishTime - startTime
    print "duration: ", duration

    return mtcDcrImg

if __name__ == '__main__':
    import sys    
    try: fn1, fn2 = sys.argv[1:3]
    except:
        fn1 = "./1.jpg"
        fn2 = "./2.jpg"
    print help_message
    img1 = cv2.imread(fn1, 0)
    img2 = cv2.imread(fn2, 0)

    mtcDcrImg = ProcessImages(img1, img2)
    vis_brute = draw_match(img1, img2, mtcDcrImg.matched_p1, mtcDcrImg.matched_p2, mtcDcrImg.status, mtcDcrImg.H)
    cv2.imshow('find_obj SURF', vis_brute)
    cv2.waitKey()
    cv2.destroyAllWindows()
