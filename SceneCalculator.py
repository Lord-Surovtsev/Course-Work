import cv2
import imp
#ImagesProcessor = imp.load_source("ImagesProcessor", "./Processing/ImagesProcessor.py")
from Processing.ImagesProcessor import ImagesProcessor
from  Restoration.SceneRestorator import SceneRestorator
from Visualisation.Triangulation import Triangulation

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
    p1, p2 , size1, size2 = imgPcr.getMatchedPoints()
#    print "size1 ", size1
#    print "size2 ", size2
#    print "p1 ", p1
#    print "p2 ", p2
    try:
        scnRtr = SceneRestorator(p1, p2, size1, size2)
        scnRtr.Calculate()
#        scnRtr.RestorePoints()
#        print "restoredP"
#        print scnRtr.restoredP
    except Exception, e:
        print e
    trtn = Triangulation(scnRtr.restoredP)
    trtn.CalculateTriangles()
    trtn.WriteToFile("1.tr")
    cv2.waitKey()
    cv2.destroyAllWindows()


