
def P3DToP2D(p):
    if p[2] == 0:
        raise Exception("Z is 0")
    res = []
    res.append(p[0] / p[2])
    res.append(p[1] / p[2])
    res.append(1)
    return res
