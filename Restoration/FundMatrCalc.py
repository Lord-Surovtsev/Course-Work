from numpy import *
from JoinedCoordinate import *
from PointsConverter import *

def A(P, PR):
    res = []
    for i in range(len(P)):
        res.append((JoinedCoordinate(P3DToP2D(P[i]), P3DToP2D(PR[i])).T)[0, :])
    return array(res)

def SetZeros(M, accuracy):
    row, col = M.shape
    for i in range(row):
        for j in range(col):
            if abs(M[i, j]) < abs(accuracy):
                M[i, j] = 0
    return M

def EMToVec(Em):
    res = []
    for i in range(len(Em) * len(Em[0])):
        res.append(Em[i / 3, i % 3])
    return array(res)

def VecToEM(v, pos):
    res = ones(shape = (3, 3))
    for i in range(0, pos):
        res[i / 3, i % 3] = v[i]
    for i in range(pos + 1, 9):
        res[i / 3, i % 3] = v[i - 1]
    return res

def getEMFromAM(AMatrix):
    res = ones(shape = (3, 3))
    for i in range(8):
        res[i / 3, i % 3] = -1 * AMatrix[i, 8] / AMatrix[i, i]
    return res

def getXFromAM(AMatrix):
    res = ones(shape = (9, 1))
    for i in range(8):
        res[i] = -1 * AMatrix[i, 8] / AMatrix[i, i]
    return res

def getTFromTX(tX):
    res = ones(shape = (3, 1))
    res[0] = tX[2, 1]
    res[1] = tX[0, 2]
    res[2] = tX[1, 0]
    return res

def CalcZ(p, pR, R, t):
    res = dot((R[1] - pR[1] * R[2]), t) / dot((R[1] - pR[1] * R[2]), p)
    return res

def Process(P, PR):
    jCs = A(P, PR)
    print jCs
    print "MyGauss-Jordan"
    GJ = MyGauss_Jordan(jCs)
    print GJ

    E = ones(shape = (3, 3))
    for i in range(8):
        E[i / 3, i % 3] = GJ[i, i] / GJ[i, 8]
    return E
#    return None
#    if gauss_jordan(jCs):
#        print jCs
#    else:
#        print "trololo\n"
#        print jCs


def MyGauss_Jordan(M):
    row, col = M.shape

    i = 0
    j = col - 1
    while (j > 0):
        if (i >= row):
            break
        if 0 == M[i, j]:
            for k in range(i + 1, row):
                if 0 != M[k, j]:
                    M[i] += M[k]
                    break;
        if 0 == M[i, j]:
            j -= 1
            continue
        for k in range(i + 1, row):
            M[k] -= M[i] * M[k, j] / M[i, j]
        for k in range(i):
            M[k] -= M[i] * M[k, j] / M[i, j]
        i += 1
        j -= 1
    return M

def DecomposeFundMatr(F):
    U, s, VT = linalg.svd(F)
    S = diag(s)
    R = dot(dot(U, W()), VT)
    TX = dot(dot(dot(VT.T, W()), S), VT)
    return (R, TX)

def W():
    res = zeros(shape = (3, 3))
    res[0, 1] = -1
    res[1, 0] = 1
    res[2, 2] = 1
    return res
