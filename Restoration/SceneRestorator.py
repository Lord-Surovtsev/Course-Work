from sys import argv
from random import randint
from FundMatrCalc import *
from numpy import linalg, concatenate
from Delaunay import *

'''
def WritePointsToFile(P, fileName):
    outputFile = open(fileName, 'w')
    for i in range(len(P)):
        outputFile.write('Field ' + str(P[i][0]) + ' ' + str(P[i][1]) + ' ' + str(P[i][2]) + '\n')
    outputFile.close()
'''
class SceneRestorator:
    def __init__(self, P, PR, accuracy = 1e-12):
        self.P = P
        self.PR = PR
#        self.left = None
        self.accuracy = accuracy
        self.R = None
        self.t = None
        self.restoredP = None
        self.restoredPR = None

    def Calculate(self):
        pntNum = GenerateRandomDistinctIntegers(0, len(self.P) - 1, 8)

        p = GetPointsFromArray(pntNum, self.P)
        pR = GetPointsFromArray(pntNum, self.PR)

        self.R, self.t = CalculateRAndT(p, pR, self.accuracy)

    def RestorePoints(self):
        if self.R is None:
            self.Calculate()
        self.restoredP = []
        for i in range(len(self.P)):
            p2 = P3DToP2D(self.P[i])
            pR2 = P3DToP2D(self.PR[i])
    #        print P[i], " -> ", PR[i]
            z = CalcZ(p2, pR2, self.R, self.t)
            self.restoredP.append(self.P[i] * z)
    #        print "calculated: ", z
        Tesselation(self.P)

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

    print "---"
    print "mEM"
    print mEM
    print "det(mEM): ", linalg.det(mEM)
    SetZeros(mEM, accuracy)
    print "zMEM"
    print mEM
    print "det(mEm) = ", linalg.det(mEM)
    R, TX = DecomposeFundMatr(mEM)
    t = getTFromTX(TX)
    print "R"
    print R
    SetZeros(R, accuracy)
    print "zR"
    print R
    print "TX"
    print TX
    print "t"
    print t
    return R, t
