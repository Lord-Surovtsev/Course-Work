from sys import argv
from random import randint
#from FundMatrCalc import A, VecToEM, DecomposeFundMatr, SetZeros, getTFromTX
from FundMatrCalc import *
from numpy import linalg, concatenate

'''
def ReadPointsFromFile(fileName):
    inputFile = open(fileName)
    P = []
    PR = []
    firstLine = True
    for line in inputFile:
        if firstLine:
            firstLine = False
            continue
        PS = line.split()
        P1 = []
        P2 = []
        P1.append(float(PS[0]))
        P1.append(float(PS[1]))
        P1.append(1)
        P2.append(float(PS[2]))
        P2.append(float(PS[3]))
        P2.append(1)
        P.append(P1)
        PR.append(P2)
    inputFile.close()
    return P, PR
'''
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

    def Restore(self):
        pntNum = GenerateRandomDistinctIntegers(0, len(self.P) - 1, 8)

        p = GetPointsFromArray(pntNum, self.P)
        pR = GetPointsFromArray(pntNum, self.PR)

        self.R, self.t = CalculateRAndT(p, pR, self.accuracy)


#    if __name__ == '__main__':
#        if len(argv) < 2:
#            print "please specify *.scene"
#            exit()
#        P, PR = ReadPointsFromFile(argv[1])

#        R, t = Restore(P, PR, 1e-12)
#        restoredP = RestorePoints(P, PR, R, t)
#        WritePointsToFile(restoredP, 'out.txt')



def GenerateRandomDistinctIntegers(left, right, quantity):
    return range(left,left+quantity)    
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

    def RestorePoints(P, PR, R, t):
        res = []
        for i in range(len(P)):
            p2 = P3DToP2D(P[i])
            pR2 = P3DToP2D(PR[i])
    #        print P[i], " -> ", PR[i]
            z = CalcZ(p2, pR2, R, t)
	    res.append(P[i] * z)
    #        print "calculated: ", z
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
