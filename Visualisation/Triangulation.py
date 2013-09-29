import math
import numpy as np

class Triangulation:
    def __init__(self, p):
        self.p = p
        self.l= len(self.p)
        self.arr = np.zeros(shape=(self.l, self.l))
        self.triangles = None

    def CalculateTriangles(self):
        for i in range(self.l):
            for j in range(i, self.l):
                self.arr[i][j] = Distance(self.p[i], self.p[j])
                self.arr[j][i] = self.arr[i][j]

    #    print "arr"
    #    print arr
        self.triangles = []
        for i in range(self.l):
            (p1, p2) = GetTwoNearest(self.arr, self.l, i)
            if p1 is None or p2 is None:
                continue
            self.triangles.append((self.p[p1], self.p[p2], self.p[i]))

    def WriteToFile(self, fileName):
        outputFile = open(fileName, 'w')
        outputFile.write(str(len(self.triangles)) + "\n")
        for t in self.triangles:
            for i in range(len(t)):
                outputFile.write(str(t[i][0]) + " " + str(t[i][1]) + " " + str(t[i][2]) + "\n")
            outputFile.write("----\n")
        outputFile.close()


def Distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def GetTwoNearest(arr, l, n):
    min1 = 0
    min1P = -1
    min2 = 0
    min2P = -1
#    add1P = []
#    add2P = []
    for i in range(l):
        if i == n:
            continue
        if min1P == -1:
            min1P = i
            min1 = arr[n][i]
            continue
        if min2P  == -1:
            min2P = i
            min2 = arr[n][i]
            continue
        if min1 > arr[n][i]:
            min1P = i
            min1 = arr[n][i]
            continue
        if min2 > arr[n][i]:
            min2P = i
            min2 = arr[n][i]
    return (min1P, min2P)

