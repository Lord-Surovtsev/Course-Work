from numpy import *

def JoinedCoordinate(p, pR):
    lP = len(p)
    lPR = len(pR)
    if lP <> lPR:
        return None
    res = ones(shape = (lP * lPR, 1))
    for i in range(lPR):
        for j in range(lP):
            res[i * lP + j, 0] *= float(p[j])
            res[i * lP + j, 0] *= pR[i]
    return res
    
'''
    res[0, 1] = p[0] * pR[0]
    res[0, 2] = p[1] * pR[0]
    res[0, 3] = p[2] * pR[0]
    res[0, 4] = p[0] * pR[1]
    res[0, 5] = p[1] * pR[1]
    res[0, 6] = p[2] * pR[1]
    res[0, 7] = p[0] * pR[2]
    res[0, 8] = p[1] * pR[2]
    res[0, 9] = p[2] * pR[2]
'''