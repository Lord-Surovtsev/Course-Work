import cv2
import imp
#ImagesProcessor = imp.load_source("ImagesProcessor", "./Processing/ImagesProcessor.py")
from Processing.ImagesProcessor import ImagesProcessor
from  Restoration.SceneRestorator import SceneRestorator

help_message = '''SURF image match 

USAGE: findobj.py [ <image1> <image2> ]
'''

if __name__ == '__main__':
    import sys
    try: fn1, fn2 = sys.argv[1:3]
    except:
        fn1 = "./1.jpg"
        fn2 = "./2.jpg"
#    print help_message
    img1 = cv2.imread(fn1, 0)
    img2 = cv2.imread(fn2, 0)

    imgPcr = ImagesProcessor(img1, img2)
    imgPcr.ProcessImages()

    vis = imgPcr.getMatchedPicture()
    cv2.imshow('SURF', vis)
    p1, p2 = imgPcr.getMatchedPoints()

    scnRtr = SceneRestorator(p1, p2)
    scnRtr.Calculate()
    scnRtr.RestorePoints()

    print "restoredPpoints"
    print scnRtr.restoredP

    cv2.waitKey()
    cv2.destroyAllWindows()


