#-*-coding: UTF-8-*-
######################################################################################
#  Author: Junjun Guo
#  E-mail: guojj@tongji.edu.cn/guojj_ce@163.com
#    Date: 05/02/2020
#  Environemet: Successfully excucted in python 3.6
######################################################################################
# import necessary modules
import matplotlib.pyplot as plt
import numpy as np
from scipy.linalg import solve
import math
import time
import pygmsh
import meshio
import matplotlib.tri as tri
from pointInPolygon import isin_multipolygon
import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #set standard output default encoding
######################################################################################
geom = pygmsh.opencascade.Geometry()
disk0=geom.add_disk([1.5, 1.5, 0.0], 1,radius1=None,char_length=0.1)
disk1 = geom.add_disk([1.5, 1.5, 0.0], 0.3,radius1=None,char_length=0.1)
flat = geom.boolean_difference([disk0], [disk1])

# geom.extrude(flat, [0, 0, 0])
########################################################################################################################
########################################################################################################################
class CircleSection():
    """
    圆形及圆环形截面纤维划分类
    输入: ax-绘图轴
          d0-保护层混凝土厚度（m)
          outD-外圆直径 (m)
          inD-内圆直径 (m)
    若inD=None则为实心圆截面，否则为圆环截面
    """

    ####################################################
    def __init__(self, ax, d0, outD, inD=None):
        """
        类的初始化
        """
        self.ax = ax
        self.coverThick = d0
        self.outDiameter = outD
        self.innerDiameter = inD

    ####################################################
    def initSectionPlot(self):
        """
        初始截面绘制
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
        计算各个三角形单元的面积与形心坐标
        输入：points-三角形单元顶点坐标数组[[x1,y1,Z1],[x2,y2,Z2]]
             triangles-三角形纤维数组[[I1,J1,K1],[I2,J2,K2]
        返回：
			inFoList:纤维单元信息列表[(xc1,yc1,area1),(xc2,yc2,area2)]
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
        核心混凝土纤维截面划分
        输入：eleSize-核心区纤维单元尺寸 （m)
        输出：coreFiberInfo:核心混凝土纤维单元列表[(xc1,yc1,area1),(xc2,yc2,area2)]
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
        保护层混凝土的分割
        coverSize-纤维单元大小
        pos-外轮廓("out"),内轮廓("in)"
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
        保护层混凝土纤维划分
        输入：
            coverSize：保护层混凝土单元的大小
        返回：
            coverFiberInfo：保护层 混凝土纤维列表[(xc1,yc1,area1),(xc2,yc2,area2)]
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
        纵向纤维划分
        输入：barD-钢筋直径 (m)
             barDist-钢筋间距 (m)
        """
        area = (np.pi * barD ** 2) / 4.0
        if pos == "out":
            newR = (self.outDiameter - 2.0 * self.coverThick) / 2.0-barD/2.0
        elif pos == "in":
            newR = (self.innerDiameter + 2 * self.coverThick) / 2.0+barD/2.0
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
        纵向钢筋纤维划分
        输入：
            outBarD：外轮廓纵筋的直径
            outBarDist：外轮廓纵筋的间距
            inBarD：内轮廓纵筋的直径
            inBarDist:内轮廓纵筋的间距
        返回:
            barFiberInfo:纵筋纤维列表[(xc1,yc1,area1),(xc2,yc2,area2)]
        """
        barFiberInfo = None
        outFiberInfo, outFiberXList, outFiberYList = self._barDivide(outBarD, outBarDist, pos="out")
        barFiberInfo = outFiberInfo
        self.ax.scatter(outFiberXList, outFiberYList, s=10, c="k", zorder=3)
        if self.innerDiameter != None:
            inFiberInfo, inFiberXList, inFiberYList = self._barDivide(inBarD, inBarDist, pos="in")
            barFiberInfo = barFiberInfo + inFiberInfo
            self.ax.scatter(inFiberXList, inFiberYList, s=15, c="k", zorder=3)
        return barFiberInfo
########################################################################################################################
########################################################################################################################
class PolygonSection():
    """
	实心，空心的多边形截面纤维单元划分(保护层混凝土，核心混凝土及纵筋纤维）
    """

    def __init__(self, ax, outNode, outEle, inNode=None, inEle=None):
        """
        初始化参数：
        ax：图形坐标轴
        outNode:外部轮廓节点字典--outSideNode={1:(3.5,3),2:(1.5,5),3:(-1.5,5),4:(-3.5,3)}
        outEle: 外部轮廓单元字典（逆时针）outSideEle = {1: (1, 2), 2: (2, 3), 3: (3, 4), 4: (4,1)}
        inNode: 内部轮廓节点列表，每个轮廓是一个字典inSideNode=[{1:(1.9,2.4),2:(1.1,3.2),3:(-1.1,3.2),4:(-1.9,2.4)}]
        inEle: 内部轮廓单元列表--inSideEle = [{1: (1, 2), 2: (2, 3), 3: (3, 4), 4: (4, 1)}]
        """
        self.outNode = outNode
        self.outEle = outEle
        self.inNode = inNode
        self.inEle = inEle
        self.ax = ax
        self.outNewNodeDict = None  # 新生成的外侧保护层混凝土线节点字典
        self.inNewNodeDict = None  # 新生成的内侧保护层混凝土线节点字典列表
        self.lineWid = 1  # 线宽
        self.coverColor = "g"  # 保护层线颜色
        self.coreColor = "r"  # 核心混凝土颜色
        self.barColor = "k"  # 纵筋颜色
        self.barMarkSize = 15  # 散点大小

    ####################################################
    def sectPlot(self):
        """
        绘制未划分纤维的截面轮廓
        """
        outLineList = self._lineNodeList(self.outNode, self.outEle) #返回每个线单元两端节点的X，Y坐标列表[([x1,x2],[y1,y2])]
        for each1 in outLineList:
            self.ax.plot(each1[0], each1[1], self.coverColor, self.lineWid, zorder=0)
        if self.inNode != None:
            for eachNode, eachEle in zip(self.inNode, self.inEle):
                innerLineList= self._lineNodeList(eachNode, eachEle)#返回每个线单元两端节点的X，Y坐标列表[([x1,x2],[y1,y2])]
                for each2 in innerLineList:
                    self.ax.plot(each2[0], each2[1], self.coverColor, self.lineWid, zorder=0)
    ####################################################
    def _lineNodeList(self, nodeDict, eleDict):
        """
        返回每个线单元两端节点的X，Y坐标列表[([x1,x2],[y1,y2])]
        输入：nodeDict-节点字典{1:(3.5,3),2:(1.5,5),3:(-1.5,5),4:(-3.5,3)}
             eleDict-单元及其两端节点字典，{1: (1, 2), 2: (2, 3), 3: (3, 4), 4: (4,1)}
        """
        nEle = len(eleDict)
        keysList = list(eleDict.keys())
        lineList = []
        for i1 in range(nEle):
            nodeI = eleDict[keysList[i1]][0]
            nodeJ = eleDict[keysList[i1]][1]
            nodeIx = nodeDict[nodeI][0]
            nodeIy = nodeDict[nodeI][1]
            nodeJx = nodeDict[nodeJ][0]
            nodeJy = nodeDict[nodeJ][1]
            lineList.append(([nodeIx, nodeJx], [nodeIy, nodeJy]))
        return lineList
    ####################################################
    def coverLinePlot(self, coverThick):
        """
        通过轮廓线及保护层厚度计算核心混凝土与外侧保护层混凝土交界线
        输入：
            coverThick:保护层混凝土厚度
        返回：
            returnNodeList:外分界线节点列表[(x1,y1),(x2,y2),...,(xn,yn)]
        """
        #计算分界线节点列表[(x1, y1), (x2, y2), ..., (xn, yn)]
        returnNodeList = self._middleLineNode(self.outNode, coverThick, pos="outLine")
        outNodeNewDict = {(i1 + 1): returnNodeList[i1] for i1 in range(len(returnNodeList))}
        self.outNewNodeDict = outNodeNewDict  ##外层混凝土保护层线节点字典，与外轮廓节点一一对应
        outEleDict = self.outEle
        # 返回每个线单元两端节点的X，Y坐标列表[([x1,x2],[y1,y2])]
        coverlineList = self._lineNodeList(outNodeNewDict, outEleDict)
        for each2 in coverlineList:
            self.ax.plot(each2[0], each2[1], self.coverColor, self.lineWid, zorder=0)
        return returnNodeList
    ####################################################
    def innerLinePlot(self, coverThick):
        """
        核心混凝土与内轮廓保护层混凝土的分界线绘制
        输入：
            coverThick--保护层混凝土厚度
        返回：
            innerList:内分界线节点列表[[(x1,y1),(x2,y2),...,(xn,yn)],...,]
        """
        if self.inNode != None:
            innerList = []
            innerListDict = []
            for eachNodeDict, eachEleDict in zip(self.inNode, self.inEle):
                #计算分界线各节点的列表[(x1,y1),(x2,y2),...,(xn,yn)]
                returnNodeList = self._middleLineNode(eachNodeDict,coverThick,pos="innerLine")
                innerList.append(returnNodeList)
                innerListDict.append({(j1 + 1): returnNodeList[j1] for j1 in range(len(returnNodeList))})
                inNodeDict = {(i1 + 1): returnNodeList[i1] for i1 in range(len(returnNodeList))}
                inEleDict = eachEleDict
                #返回每个线单元两端节点的X，Y坐标列表[([x1,x2],[y1,y2])]
                inlineList = self._lineNodeList(inNodeDict, inEleDict)
                for each2 in inlineList:
                    self.ax.plot(each2[0], each2[1], self.coverColor, self.lineWid, zorder=0)
            self.inNewNodeDict = innerListDict
            return innerList
    ####################################################
    def _polygonInnerPoint(self,nodeDict):
        """
        得到封闭多边形内一点坐标
        输入: nodeDict-节点字典 {1:(2.3,4.3)}
        输出：InNode-内部一个节点坐标[(xi,yi)]
        """
        nodeValues = list(nodeDict.values())
        nodeValues.append(nodeValues[0])
        nodeValuesX = [each1[0] for each1 in nodeValues]
        nodeValuesY = [each1[1] for each1 in nodeValues]
        setNodeValuesX = set(nodeValuesX)
        setNodeValuesY = set(nodeValuesY)
        setNodexList = list(setNodeValuesX)
        setNodeyList = list(setNodeValuesY)
        setNodexList.sort(reverse=False)
        setNodeyList.sort(reverse=False)
        xMiddleList = [0.5 * (setNodexList[i1] + setNodexList[i1 + 1]) for i1 in range(len(setNodexList) - 1)]
        yMiddleList = [0.5 * (setNodeyList[i2] + setNodeyList[i2 + 1]) for i2 in range(len(setNodeyList) - 1)]
        possibleInPoints = [(x1, y1) for x1 in xMiddleList for y1 in yMiddleList]
        innerPoint = None
        for each1 in possibleInPoints:
            returnIndex = isin_multipolygon(each1, nodeValues, contain_boundary=False)
            if returnIndex == True:
                innerPoint = each1
                break
            else:
                continue
        return innerPoint
    ####################################################
    def _pointToLineDist(self,a,b,c,innerPointCoord):
        """
        计算点到直线距离
        ax+by+c=0
        输入：a,b,c参数
              innerPointCoord-一点坐标
        输出：d-点到直线距离
        """
        x0=innerPointCoord[0]
        y0=innerPointCoord[1]
        d=np.abs((a*x0+b*y0+c))/float(math.sqrt(a**2+b**2))
        return d
    ####################################################
    def _interNodeCoord(self,nodeDict,coverThick,pos,innerNode):
        """
        计算多边形整体缩放后的交点坐标
        输入:nodeDict-节点字典 {1:(2.3,4.3)}
             coverThick-保护层厚度
             pos-外侧分界线（"outLine"),内侧分界线("innerLine")
             innerNode-封闭多边形内一点 [(x1,y1)]
        输出：NodeList-新节点坐标列表 [(x1,y1),(x2,y2),...,(xn,yn)]
        """
        NodeKeys = list(nodeDict.keys())
        NodeKeys.append(NodeKeys[0])
        NodeKeys.append(NodeKeys[1])
        IterNode = []
        for i1 in range(len(nodeDict)):
            IterNode.append((NodeKeys[i1], NodeKeys[i1 + 1], NodeKeys[i1 + 2]))
        NodeList = []
        for each1 in IterNode:
            nodeI = nodeDict[each1[0]]
            nodeJ = nodeDict[each1[1]]
            nodeK = nodeDict[each1[2]]
            nodeIx, nodeIy = nodeI[0], nodeI[1]
            nodeJx, nodeJy = nodeJ[0], nodeJ[1]
            nodeKx, nodeKy = nodeK[0], nodeK[1]
            a1 = (nodeJy - nodeIy)  #两点法确定直线方程 （y2-y1）x+(x1-x2)y+(x2-x1)y1-x1(y2-y1)=0
            b1 = -(nodeJx - nodeIx)
            c1 = (nodeJx - nodeIx) * nodeIy - (nodeJy - nodeIy) * nodeIx
            a2 = (nodeKy - nodeJy)
            b2 = -(nodeKx - nodeJx)
            c2 = (nodeKx - nodeJx) * nodeJy - (nodeKy - nodeJy) * nodeJx
            c1_1 = c1 - math.sqrt(a1 ** 2 + b1 ** 2) * coverThick
            c1_2 = c1 + math.sqrt(a1 ** 2 + b1 ** 2) * coverThick
            c2_1 = c2 - math.sqrt(a2 ** 2 + b2 ** 2) * coverThick
            c2_2 = c2 + math.sqrt(a2 ** 2 + b2 ** 2) * coverThick
            d1_1=self._pointToLineDist(a1,b1,c1_1,innerNode) #计算点到直线距离
            d1_2=self._pointToLineDist(a1,b1,c1_2,innerNode)
            d2_1 = self._pointToLineDist(a2, b2, c2_1, innerNode)  # 计算点到直线距离
            d2_2 = self._pointToLineDist(a2, b2, c2_2, innerNode)
            if pos == "outLine":
                c11 = c1_1 if abs(d1_1) < abs(d1_2) else c1_2
                c22 = c2_1 if abs(d2_1) < abs(d2_2) else c2_2
            elif pos == "innerLine":
                c11 = c1_1 if abs(d1_1) > abs(d1_2) else c1_2
                c22 = c2_1 if abs(d2_1) > abs(d2_2) else c2_2
            else:
                print("Error!Please select outLine or innerLine mode!")
            A = np.array([[a1, b1], [a2, b2]])
            B = np.array([-c11, -c22])
            newNode = list(solve(A, B))
            NodeList.append((newNode[0], newNode[1]))
        NodeList.insert(0, NodeList[-1])
        del NodeList[-1]
        return NodeList
    ####################################################
    def _middleLineNode(self, nodeDict,coverThick,pos="outLine"):
        """
        计算分界线各节点的列表
        输入：
            nodeDict:节点字典 {1:(2.3,4.3)}
            coverThick:保护层厚度
            pos:外侧分界线（"outLine"),内侧分界线("innerLine")
        返回：
            NodeList:外分界线节点列表[(x1,y1),(x2,y2),...,(xn,yn)]
        """
        innerNodeCoord=self._polygonInnerPoint(nodeDict) #得到封闭多边形内一点坐标
        newNodeList=self._interNodeCoord(nodeDict, coverThick, pos, innerNodeCoord)#计算多边形整体缩放后的交点坐标
        return newNodeList
    ####################################################
    def _triEleInfo(self, nodeNArray, eleNArray):
        """
        计算生成的三角纤维单元的面积与形心坐标
        输入：
            nodeNArray:节点坐标列表[[x1,y1],[x2,y2]]
            eleNArray:单元列表[[I1,J1,K1],[I2,J2,K2]
        返回：
            inFoList:纤维单元信息列表[(xc1,yc1,area1),(xc2,yc2,area2)]
        """
        inFoList = []
        for each in eleNArray:
            I, J, K = each[0], each[1], each[2]
            x1 = nodeNArray[I][0]
            y1 = nodeNArray[I][1]
            x2 = nodeNArray[J][0]
            y2 = nodeNArray[J][1]
            x3 = nodeNArray[K][0]
            y3 = nodeNArray[K][1]
            area = 0.5 * (x1 * y2 - x2 * y1 + x2 * y3 - x3 * y2 + x3 * y1 - x1 * y3)
            xc = (x1 + x2 + x3) / 3.0
            yc = (y1 + y2 + y3) / 3.0
            inFoList.append((xc, yc, area))
        return inFoList
    ####################################################
    def coreMesh(self, eleSize, outLineList, inLineList=None):
        """
        多边形截面核心混凝土纤维的划分
        输入：
            eleSize:纤维单元的大小
            outLineList:外分界线节点列表[(x1,y1),(x2,y2),...,(xn,yn)]
            inLineList:内分界线节点列表[[(x1,y1),(x2,y2),...,(xn,yn)],[(x1,y1),(x2,y2),...,(xn,yn)]]
        返回：
            triEleInfoList:纤维单元信息列表[(xc1,yc1,area1),(xc2,yc2,area2)]
        """
        triEleInfoList = None
        outNOdeList=[[outLineList[i1][0],outLineList[i1][1],0] for i1 in range(len(outLineList))]

        if inLineList == None:
            geom = pygmsh.opencascade.Geometry()
            geom.add_polygon(outNOdeList,lcar=eleSize)
            mesh = pygmsh.generate_mesh(geom)
            points = mesh.points
            triangles = mesh.cells["triangle"]
            triEleInfoList = self._triEleInfo(points, triangles)
            self.ax.triplot(points[:, 0], points[:, 1], triangles)
        else:
            geom=pygmsh.opencascade.Geometry()
            outPolygon=geom.add_polygon(outNOdeList, lcar=eleSize)
            for eachInnerList in inLineList:
                inNodeList = [[eachInnerList[i2][0], eachInnerList[i2][1], 0] for i2 in range(len(eachInnerList))]
                inPolygon=geom.add_polygon(inNodeList, lcar=eleSize)
                differencePolygon=geom.boolean_difference([outPolygon],[inPolygon])
                outPolygon=differencePolygon
            mesh = pygmsh.generate_mesh(geom)
            points = mesh.points
            triangles = mesh.cells["triangle"]
            triEleInfoList = self._triEleInfo(points, triangles)
            self.ax.triplot(points[:, 0], points[:, 1], triangles)
        return triEleInfoList
    ####################################################
    def _coverDivide(self, outNodeDict, inNodeDict, eleDict, eleSize, coverThick):
        """
        保护层混凝土纤维的分割
        输入:
            outNodeDict:外侧轮廓节点字典--{1:(3.5,3),2:(1.5,5),3:(-1.5,5),4:(-3.5,3)}
            inNodeDict:内侧轮廓节对应点字典--{1:(2.5,2),2:(0.5,4),3:(-0.5,4),4:(-2.5,2)}
            eleDict:外侧轮廓单元字典:--{1:(1,2),2:(2,3),3:(3,4),4:(4,1)}
            eleSize:保护层混凝土纤维单元尺寸
            coverThick:混凝土保护层厚度
        返回：
            centerCoordList:保护层纤维单元中心坐标及面积列表--[(xc1,yc1,A1),(xc2,yc2,A2),...,)
            outPlotNode:外侧分割后各个节点坐标列表--[(x1,y1),(x2,y2),...,(xn,yn)]
            inPlotNode:内侧分割后各个节点坐标列表--[(xin1,yin1),...,(xinn,yinn)]
        """
        nLine = len(eleDict)
        outPlotNode = []
        inPlotNode = []
        centerCoordList = []
        for i1 in range(1, nLine + 1):
            nodeI = eleDict[i1][0]
            nodeJ = eleDict[i1][1]
            outNodeIx = outNodeDict[nodeI][0]
            outNodeIy = outNodeDict[nodeI][1]
            outNodeJx = outNodeDict[nodeJ][0]
            outNodeJy = outNodeDict[nodeJ][1]
            inNodeIx = inNodeDict[nodeI][0]
            inNodeIy = inNodeDict[nodeI][1]
            inNodeJx = inNodeDict[nodeJ][0]
            inNodeJy = inNodeDict[nodeJ][1]
            length = math.sqrt((outNodeJx - outNodeIx) ** 2 + (outNodeJy - outNodeIy) ** 2)
            nEle = int(length /float(eleSize))
            totalOutNodeList = []
            totalInNodeList = []
            totalOutNodeList.append((outNodeIx, outNodeIy))
            totalInNodeList.append((inNodeIx, inNodeIy))
            for i2 in range(1, nEle):
                outxi = ((nEle - i2) * outNodeIx + i2 * outNodeJx) / nEle  # n等分点公式
                outyi = ((nEle - i2) * outNodeIy + i2 * outNodeJy) / nEle
                inxi = ((nEle - i2) * inNodeIx + i2 * inNodeJx) / nEle
                inyi = ((nEle - i2) * inNodeIy + i2 * inNodeJy) / nEle
                totalOutNodeList.append((outxi, outyi))
                totalInNodeList.append((inxi, inyi))
            totalOutNodeList.append((outNodeJx, outNodeJy))
            totalInNodeList.append((inNodeJx, inNodeJy))
            inLength = math.sqrt((totalInNodeList[1][0] - totalInNodeList[0][0]) ** 2 \
                                 + (totalInNodeList[1][1] - totalInNodeList[0][1]) ** 2)
            outLength = math.sqrt((totalOutNodeList[1][0] - totalOutNodeList[0][0]) ** 2 + \
                                  (totalOutNodeList[1][1] - totalOutNodeList[0][1]) ** 2)
            eleArea = (inLength + outLength) * coverThick / 2.0
            for j2 in range(len(totalOutNodeList) - 1):
                outPlotNode.append(totalOutNodeList[j2])
                inPlotNode.append(totalInNodeList[j2])
            for i3 in range(len(totalOutNodeList) - 1):
                outI = totalOutNodeList[i3]
                outJ = totalOutNodeList[i3 + 1]
                inI = totalInNodeList[i3]
                inJ = totalInNodeList[i3 + 1]
                outCenter = ((outI[0] + outJ[0]) / 2.0, (outI[1] + outJ[1]) / 2.0)
                inCenter = ((inI[0] + inJ[0]) / 2.0, (inI[1] + inJ[1]) / 2.0)
                centerCoord = (
                (outCenter[0] + inCenter[0]) / 2.0, (outCenter[1] + inCenter[1]) / 2.0, eleArea)  # 纤维中心坐标及其面积
                centerCoordList.append(centerCoord)
        return centerCoordList, outPlotNode, inPlotNode
    ####################################################
    def coverMesh(self, eleSize, coverThick):
        """
        保护层混凝土纤维的划分
        输入：
            eleSize：核心混凝土纤维尺寸
            coverThick：保护层厚度
        返回：
            coverFiberInfo:保护层混凝土纤维单元[(xc1,yc1,area1),(xc2,yc2,area2)]
        """
        coverFiberInfo = None
        nodeOutDict = self.outNode
        eleOutDict = self.outEle
        nodeNewOutDict = self.outNewNodeDict  # 新生成的外侧保护层混凝土线节点字典
        nodeNewInDict = self.inNewNodeDict  # 新生成的内侧保护层混凝土线节点字典列表
        nodeInDict = self.inNode
        eleInDict = self.inEle
        #保护层混凝土纤维的分割
        fiberInfo, outNodeInfo, inNodeInfo = self._coverDivide(nodeOutDict, nodeNewOutDict,\
                                                               eleOutDict,eleSize,coverThick)
        print(fiberInfo)








########################################################################################################################
if __name__=="__main__":
    # import meshio
    # mesh=pygmsh.generate_mesh(geom)
    # nodes=mesh.points
    # cells=mesh.cells["triangle"]
    # print(mesh.cells)
    # meshio.write("opecsa.vtk",mesh)
    #
    # fig1, ax1 = plt.subplots()
    # for each in cells:
    #     nodeI,nodeJ,nodeK=each[0],each[1],each[2]
    #     x=[nodes[nodeI][0],nodes[nodeJ][0],nodes[nodeK][0]]
    #     y = [nodes[nodeI][1], nodes[nodeJ][1], nodes[nodeK][1]]
    #     triang=tri.Triangulation(x,y)
    #     ax1.set_aspect('equal')
    #     ax1.triplot(triang, 'bo-', lw=1,ms=1)
    # plt.show()

    #######################---circle section---#########################################################################
    ####################################################################################################################
    """
    fig = plt.figure(figsize=(5, 5))
    ax = fig.add_subplot(111)
    outbarD = 0.03  # 纵向钢筋直径
    outbarDist = 0.15  # 纵向钢筋间距
    inBarD = 0.03
    inBarDist = 0.15
    coverThick = 0.1  # 保护层混凝土厚度
    coreEleSize = 0.15  # 核心纤维的大小
    coverEleSize = 0.15  # 保护层纤维大小
    outDiameter = 3  # 截面外圆直径
    innerDiameter = 1 #截面内圆直径
    circleInstance = CircleSection(ax, coverThick, outDiameter)
    circleInstance.initSectionPlot()
    coreFiber=circleInstance.coreMesh(coreEleSize)
    coverFiber = circleInstance.coverMesh(coverEleSize)
    barFiber = circleInstance.barMesh(outbarD, outbarDist)
    plt.show()

    # fig1 = plt.figure(figsize=(5, 5))
    # ax1 = fig1.add_subplot(111)
    # coreFiberXList = [each1[0] for each1 in coreFiber]
    # coreFiberYList = [each1[1] for each1 in coreFiber]
    # coreFiberAreaList = [each1[2] for each1 in coreFiber]
    # coverFiberXList = [each1[0] for each1 in coverFiber]
    # coverFiberYList = [each1[1] for each1 in coverFiber]
    # coverFiberAreaList = [each1[2] for each1 in coverFiber]
    # barFiberXList = [each1[0] for each1 in barFiber]
    # barFiberYList = [each1[1] for each1 in barFiber]
    # barFiberAreaList = [each1[2] for each1 in barFiber]
    # ax1.scatter(coreFiberXList, coreFiberYList, s=5, c="k", zorder=3)
    # ax1.scatter(coverFiberXList, coverFiberYList, s=5, c="k", zorder=3)
    # ax1.scatter(barFiberXList, barFiberYList, s=5, c="k", zorder=3)
    # plt.show()
    """
    #######################---polygon section---#########################################################################
    ####################################################################################################################
    outSideNode = {1: (-5, -5), 2: (5, -5), 3: (5, 5), 4: (-5, 5)}
    outSideEle = {1: (1, 2), 2: (2, 3), 3: (3, 4), 4: (4, 1)}
    inSideNode = [{1: (-3, -3), 2: (-1, -3), 3: (-1, 3), 4: (-3, 3)}, {1: (1, -3), 2: (3, -3), 3: (3, 3), 4: (1, 3)}]
    inSideEle = [{1: (1, 2), 2: (2, 3), 3: (3, 4), 4: (4, 1)}, {1: (1, 2), 2: (2, 3), 3: (3, 4), 4: (4, 1)}]
    fig = plt.figure(figsize=(5, 5))
    ax = fig.add_subplot(111)
    coverThick = 0.2  # 保护层厚度 (m)
    coreEleSize = 0.5  # 核心混凝土纤维单元大小 (m)
    coverEleSize = 0.3  # 保护层混凝土纤维单元大小 (m)
    outBarDist = 0.4 #外侧钢筋间距 (m)
    outBarD = 0.032 #外侧钢筋直径 (m)
    inBarDist = 0.4 #内侧钢筋间距 (m)
    inBarD = 0.032 #内侧钢筋直径 (m)
    sectInstance = PolygonSection(ax, outSideNode, outSideEle, inSideNode, inSideEle)
    sectInstance.sectPlot()
    outLineList = sectInstance.coverLinePlot(coverThick)
    inLineList = sectInstance.innerLinePlot(coverThick)
    coreFiber = sectInstance.coreMesh(coreEleSize, outLineList, inLineList)
    coverFiber = sectInstance.coverMesh(coverEleSize, coverThick)

    plt.show()


