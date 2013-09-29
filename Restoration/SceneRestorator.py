from sys import argv
from random import randint
from FundMatrCalc import *
from numpy import linalg, concatenate
from Delaunay import Tesselation

class SceneRestorator:
    def __init__(self, P, PR, size, sizeR, accuracy = 1e-12):
        self.P = P
        self.PR = PR
        self.size = size
        self.sizeR = sizeR
        self.accuracy = accuracy
        self.R = None
        self.t = None
        self.restoredP = None
        self.restoredPR = None

        self.p = None
        self.pR = None
        if len(self.P) < 8 or len(self.PR) < 8:
            raise Exception("little points. needed at least 8, but given  ", len(self.P))

    def Calculate(self):
        while True:
            pntNum = GenerateRandomDistinctIntegers(0, len(self.P) - 1, 8)

            print "pntNum ", pntNum
            p = GetPointsFromArray(pntNum, self.P)
            pR = GetPointsFromArray(pntNum, self.PR)

            for i in range(len(p)):
                print p[i][0], " ", p[i][1], " ", pR[i][0], " ", pR[i][1]

            self.p = p
            self.pR = pR

            self.R, self.t = CalculateRAndT(p, pR, self.accuracy)

            self.RestorePoints()
            if CheckResPoints(self.restoredP):
                break

    def RestorePoints(self):
        if self.R is None:
            self.Calculate()
#        Tesselation(self.P, self.size)
        self.restoredP = []
        for i in range(len(self.P)):
            p2 = P3DToP2D(self.P[i])
            pR2 = P3DToP2D(self.PR[i])
    #        print P[i], " -> ", PR[i]
            z = CalcZ(p2, pR2, self.R, self.t)
            print i, " ", z
            self.restoredP.append(self.P[i] * z * 100)
    #        print "calculated: ", z
        WritePointsToFile(self.restoredP, "out.txt")

'''
def CheckTranslationVector(t):
    i = 1
    if t[0] < 0:
        i *= -1
    if t[1] < 0:
        i *= -1
    if t[2] < 0:
        i *= -1
    return i > 0
'''

def CheckResPoints(p):
    g = 0
    l = 0
    for i in range(len(p)):
        if g > 0 and l > 0:
            return False
        if p[i][2] < 0:
            l += 1
            continue
        if p[i][2] > 0:
            g += 1
    return True

def GenerateRandomDistinctIntegers(left, right, quantity):
#    return range(left,left+quantity)
    res = []
    count = 0
    while count < quantity:
        n = randint(left, right)
        if n in res:
            continue
        res.append(n)
        count += 1
    return res

def GetPointsFromArray(numbers, P):
    res = []
    for i in range(len(numbers)):
        res.append(P[numbers[i]])
    return res

def CalculateRAndT(P, PR, accuracy):
    AMatrix = A(P, PR)

    minDet = 1000
    for i in range(9):
        mEMV = linalg.solve(concatenate((AMatrix[:, :i] * -1, AMatrix[:, i + 1:] * -1), axis = 1), AMatrix[:, i])
        mEM = VecToEM(mEMV, i)
        det = linalg.det(mEM)
        if abs(det) < abs(minDet):
            minEM = mEM
            minDet = det
    mEM = minEM

    '''
    print "---"
    print "mEM"
    print mEM
    print "det(mEM): ", linalg.det(mEM)
    '''
    SetZeros(mEM, accuracy)
    '''
    print "zMEM"
    print mEM
    print "det(mEm) = ", linalg.det(mEM)
    '''
    R, TX = DecomposeFundMatr(mEM)
    t = getTFromTX(TX)
    '''
    print "R"
    print R
    '''
    SetZeros(R, accuracy)
    '''
    print "zR"
    print R
    print "TX"
    print TX
    '''
    print "t--"
    print t

    return R, t

def WritePointsToFile(P, fileName):
    outputFile = open(fileName, 'w')
    for i in range(len(P)):
        outputFile.write(str(P[i][0]) + ' ' + str(P[i][1]) + ' ' + str(P[i][2]) + '\n')
    outputFile.close()


