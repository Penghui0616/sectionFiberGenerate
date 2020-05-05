######################################################################################
#  Author: Junjun Guo
#  E-mail: guojj@tongji.edu.cn/guojj_ce@163.com
#    Date: 05/02/2020
#  Environemet: Successfully excucted in python 3.6
######################################################################################
# import necessary modules
import matplotlib.pyplot as plt
import numpy as np
cimport numpy as np
from scipy.linalg import solve
import math
import time
import pygmsh
import meshio
import matplotlib.tri as tri
from pointInPolygon import is_in_2d_polygon
cimport cython
@cython.boundscheck(False)
@cython.wraparound(False)
######################################################################################
class CircleSection():
    """
    Circle section fibers generate
    Input:ax-axes
          d0-concreate cover length (m)
          outD-outside diameter (m)
          inD-inner diameter (m)
          if inD==None,the section is solid circle, otherwise is torus
    #######################---solid section circle example---#########################
    from fiberGenerate import CircleSection
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(5, 5))
    ax = fig.add_subplot(111)
    outbarD = 0.03  # outside bar diameter
    outbarDist = 0.15  # outside bar space
    d0 = 0.06  # the thinckness of the cover concrete
    eleSize = 0.15  # the size of core concrete fiber
    coverSize = 0.15  # the size of cover concrete fiber
    outD = 3  # the diameter of the outside circle
    circleInstance = CircleSection(ax, d0, outD)  # call the circle section generate class
    circleInstance.initSectionPlot()  # plot profile of the circle
    coreFiber = circleInstance.coreMesh(eleSize)  # generate core concrete fiber elements [(x1,y1,area1),...]
    coverFiber = circleInstance.coverMesh(coverSize)  # generate cover concrete fiber elements [(x1,y1,area1),...]
    barFiber = circleInstance.barMesh(outbarD, outbarDist)  # generate the bar fiber elements [(x1,y1,area1),...]
    plt.show()
    #######################---torus section example---#########################
    from fiberGenerate import CircleSection
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(5, 5))
    ax = fig.add_subplot(111)
    outbarD = 0.03  # outside bar diameter
    outbarDist = 0.15  # outside bar space
    inBarD = 0.03  # inside bar diameter
    inBarDist = 0.15  # inside bar space
    d0 = 0.1  # the thinckness of the cover concrete
    coreSize = 0.15  # the size of core concrete fiber
    coverSize = 0.15  # the size of cover concrete fiber
    outD = 3  # the diameter of the outside circle
    inD = 1  # the diameter of the inner circle
    circleInstance = CircleSection(ax, d0, outD, inD)  # call the circle section generate class
    circleInstance.initSectionPlot()  # plot profile of the circle
    coreFiber = circleInstance.coreMesh(coreSize)  # generate core concrete fiber elements
    coverFiber = circleInstance.coverMesh(coverSize)  # generate cover concrete fiber elements
    barFiber = circleInstance.barMesh(outbarD, outbarDist, inBarD, inBarDist)  # generate the bar fiber elements
    plt.show()
    """
    ####################################################
    def __init__(self, ax, d0, outD, inD=None):
        """
        Initialize the class
        """
        self.ax = ax
        self.coverThick = d0
        self.outDiameter = outD
        self.innerDiameter = inD

    ####################################################
    def initSectionPlot(self):
        """
        Plot the original section
        """
        theta = np.arange(0, 2 * np.pi, 0.01)
        outxList = (self.outDiameter / 2.0) * np.cos(theta)
        outyList = (self.outDiameter / 2.0) * np.sin(theta)
        self.ax.plot(outxList, outyList, "r", linewidth=1, zorder=2)
        if self.innerDiameter != None:
            inxList = (self.innerDiameter / 2.0) * np.cos(theta)
            inyList = (self.innerDiameter / 2.0) * np.sin(theta)
            self.ax.plot(inxList, inyList, "r", linewidth=1, zorder=2)

    ####################################################
    def _triEleInfo(self,points, triangles):
        """
        Calculate the area and the centroid coordinates of triangle element
        Input:points-vertex of triangel element[[x1,y1,Z1],[x2,y2,Z2]]
             triangles-triangle element list[[I1,J1,K1],[I2,J2,K2]]
        Output:
			inFoList:fiber element information [(xc1,yc1,area1),(xc2,yc2,area2)]
        """
        inFoList = []
        for each in triangles:
            I, J, K = each[0], each[1], each[2]
            x1 = points[I][0]
            y1 = points[I][1]
            x2 = points[J][0]
            y2 = points[J][1]
            x3 = points[K][0]
            y3 = points[K][1]
            area = 0.5 * (x1 * y2 - x2 * y1 + x2 * y3 - x3 * y2 + x3 * y1 - x1 * y3)
            xc = (x1 + x2 + x3) / 3.0
            yc = (y1 + y2 + y3) / 3.0
            inFoList.append((xc, yc, area))
        return inFoList
    ####################################################
    def coreMesh(self,eleSize):
        """
        Core concrete fiber generate
        Input: eleSize- fiber element size
        Output: coreFiberInfo:core concrete fiber elment informaiton [(xc1,yc1,area1),(xc2,yc2,area2)]
        """
        outDiameterNew = self.outDiameter - self.coverThick * 2.0
        if self.innerDiameter != None:
            innerDiameterNew = self.innerDiameter + self.coverThick * 2.0
            geom = pygmsh.opencascade.Geometry()
            diskOut = geom.add_disk([0.0, 0.0, 0.0], outDiameterNew/2.0, radius1=None, char_length=eleSize)
            diskInner = geom.add_disk([0.0,0.0, 0.0], innerDiameterNew/2.0, radius1=None, char_length=eleSize)
            geom.boolean_difference([diskOut], [diskInner])
            mesh = pygmsh.generate_mesh(geom)
            points=mesh.points
            triangles=mesh.cells["triangle"]
            coreFiberInfo = self._triEleInfo(points, triangles)
            self.ax.triplot(points[:, 0], points[:, 1], triangles)
        else:
            geom = pygmsh.opencascade.Geometry()
            disk = geom.add_disk([0.0, 0.0, 0.0], outDiameterNew / 2.0, radius1=None, char_length=eleSize)
            mesh = pygmsh.generate_mesh(geom)
            points = mesh.points
            triangles = mesh.cells["triangle"]
            coreFiberInfo = self._triEleInfo(points, triangles)
            self.ax.triplot(points[:, 0], points[:, 1], triangles)
        return coreFiberInfo

    ####################################################
    def _coverDivide(self, coverSize, pos="out"):
        """
        Cover concrete fiber generate
        coverSize-fiber size
        pos-outSize cover("out"),inner cover("in)"
        """
        if pos == "out":
            D = self.outDiameter
            DNew = self.outDiameter - self.coverThick * 2.0
            circumLength = np.pi * self.outDiameter
            Area = (np.pi * self.outDiameter ** 2) / 4.0
            NewArea = (np.pi * DNew ** 2) / 4.0
            nCover = int(circumLength / coverSize)
            coverArea = (Area - NewArea) / nCover
            R = self.outDiameter / 2.0
            NewR = DNew / 2.0
        elif pos == "in":
            D = self.innerDiameter
            DNew = self.innerDiameter + self.coverThick * 2.0
            circumLength = np.pi * D
            Area = (np.pi * D ** 2) / 4.0
            NewArea = (np.pi * DNew ** 2) / 4.0
            nCover = int(circumLength / coverSize)
            coverArea = (NewArea - Area) / nCover
            R = self.innerDiameter / 2.0
            NewR = DNew / 2.0
        else:
            print("Please select pos=out or pos=in!")
        Angle = 2 * np.pi / nCover
        NodeList = [(R * np.cos(Angle * i1), R * np.sin(Angle * i1)) for i1 in range(nCover)]
        NewNodeList = [(NewR * np.cos(Angle * i2), NewR * np.sin(Angle * i2)) for i2 in range(nCover)]
        fiberNCover = nCover
        fiberAngle = (2 * np.pi) / fiberNCover
        FiberRadius = (D + DNew) / 4.0
        FiberXList = [FiberRadius * np.cos((2 * i3 - 1) * 0.5 * fiberAngle) for i3 in range(1, fiberNCover + 1)]
        FiberYList = [FiberRadius * np.sin((2 * i4 - 1) * 0.5 * fiberAngle) for i4 in range(1, fiberNCover + 1)]
        coverFiberInfo = [(xc, yc, coverArea) for xc, yc in zip(FiberXList, FiberYList)]
        return coverFiberInfo, FiberXList, FiberYList, NodeList, NewNodeList

    ####################################################
    def coverMesh(self, coverSize):
        """
        Cover concrete mesh
        Input:
            coverSize: cover concrete fiber size
        Output:
            coverFiberInfo: cover fiber information [(xc1,yc1,area1),(xc2,yc2,area2)]
        """
        coverFiberInfo = None
        outCoverFiberInfo, outFiberXList, outFiberYList, outNodeList, \
            outNewNodeList = self._coverDivide(coverSize,pos="out")
        coverFiberInfo = outCoverFiberInfo
        outDNew = self.outDiameter - 2.0 * self.coverThick
        theta = np.arange(0, 2 * np.pi, 0.01)
        outThetaX = (outDNew / 2.0) * np.cos(theta)
        outThetaY = (outDNew / 2.0) * np.sin(theta)
        self.ax.plot(outThetaX, outThetaY, "r", linewidth=1, zorder=2)
        # self.ax.scatter(outFiberXList,outFiberYList,s=10,c="k",zorder = 2)
        for i5 in range(len(outNodeList)):
            xList = [outNodeList[i5][0], outNewNodeList[i5][0]]
            yList = [outNodeList[i5][1], outNewNodeList[i5][1]]
            self.ax.plot(xList, yList, "r", linewidth=1, zorder=2)
        if self.innerDiameter != None:
            inDNew = self.innerDiameter + 2.0 * self.coverThick
            inCoverFiberInfo, inFiberXList, inFiberYList, inNodeList, inNewNodeList \
                = self._coverDivide(coverSize, pos="in")
            coverFiberInfo = coverFiberInfo + inCoverFiberInfo
            inThetaX = (inDNew / 2.0) * np.cos(theta)
            inThetaY = (inDNew / 2.0) * np.sin(theta)
            self.ax.plot(inThetaX, inThetaY, "r", linewidth=1, zorder=2)
            # self.ax.scatter(inFiberXList,inFiberYList,s=10,c="k",zorder = 2)
            for i5 in range(len(inNodeList)):
                xList = [inNodeList[i5][0], inNewNodeList[i5][0]]
                yList = [inNodeList[i5][1], inNewNodeList[i5][1]]
                self.ax.plot(xList, yList, "r", linewidth=1, zorder=2)
        return coverFiberInfo
    ####################################################
    def _barDivide(self, barD, barDist, pos="out"):
        """
        Bar fiber divide
        Input:barD-bar diameter (m)
             barDist-bar space (m)
        """
        newR=None
        area = (np.pi * barD ** 2) / 4.0
        if pos == "out":
            newR = (self.outDiameter - 2.0 * self.coverThick) / 2.0-barD/2.0
        elif pos == "in":
            newR = (self.innerDiameter + 2.0 * self.coverThick)/2.0 +barD/2.0
        circumLength = 2 * np.pi * newR
        nBar = int(circumLength / barDist)
        angle = (2 * np.pi) / nBar
        fiberXList = [newR * np.cos(angle * i1) for i1 in range(1, nBar + 1)]
        fiberYList = [newR * np.sin(angle * i2) for i2 in range(1, nBar + 1)]
        barFiberInfo = [(xb, yb, area) for xb, yb in zip(fiberXList, fiberYList)]
        return barFiberInfo, fiberXList, fiberYList
    ####################################################
    def barMesh(self, outBarD, outBarDist, inBarD=None, inBarDist=None):
        """
        Bar mesh
        Input:
            outBarD: bar diameter in outside cover zone
            outBarDist: bar space in outside cover zone
            inBarD: bar diameter in inner cover zone
            inBarDist: bar space in inner cover zone
        Output:
            barFiberInfo:bar fiber infomation [(xc1,yc1,area1),(xc2,yc2,area2)]
        """
        barFiberInfo = None
        outFiberInfo, outFiberXList, outFiberYList = self._barDivide(outBarD, outBarDist, pos="out")
        barFiberInfo = outFiberInfo
        self.ax.scatter(outFiberXList, outFiberYList, s=10, c="k", zorder=3)
        if self.innerDiameter != None:
            inFiberInfo, inFiberXList, inFiberYList = self._barDivide(inBarD, inBarDist, pos="in")
            barFiberInfo = barFiberInfo + inFiberInfo
            self.ax.scatter(inFiberXList, inFiberYList, s=10, c="k", zorder=3)
        return barFiberInfo
########################################################################################################################
########################################################################################################################