#-*-coding: UTF-8-*-
######################################################################################
#  Author: Junjun Guo
#  E-mail: guojj@tongji.edu.cn/guojj_ce@163.com
#    Date: 01/01/2020
#  Environemet: Successfully excucted in python 3.6
######################################################################################
import os
import dmsh
import optimesh
import meshio
import matplotlib.pyplot as plt
import numpy as np
from scipy.linalg import solve
import math
import time
######################################################################################
class PolygonSection():
	"""
	实心，一个及两个空心的多边形截面纤维单元划分(保护层混凝土，核心混凝土及纵筋纤维）
	"""
	def __init__(self,ax,outNode,outEle,inNode=None,inEle=None):
		"""
		初始化参数：
		ax：图形轴
		outNode:外部轮廓节点字典--outSideNode={1:(3.5,3),2:(1.5,5),3:(-1.5,5),4:(-3.5,3)}
		outEle: 外部轮廓单元字典（逆时针）outSideEle = {1: (1, 2), 2: (2, 3), 3: (3, 4), 4: (4,1)}
		inNode: 内部轮廓节点列表，每个轮廓是一个字典inSideNode=[{1:(1.9,2.4),2:(1.1,3.2),3:(-1.1,3.2),4:(-1.9,2.4)}]
		inEle: 内部轮廓单元列表--inSideEle = [{1: (1, 2), 2: (2, 3), 3: (3, 4), 4: (4, 1)}]
		"""
		self.outNode=outNode
		self.outEle=outEle
		self.inNode=inNode
		self.inEle=inEle
		self.ax=ax
		self.outNewNodeDict=None  #新生成的外侧保护层混凝土线节点字典
		self.inNewNodeDict=None	  #新生成的内侧保护层混凝土线节点字典列表
		self.lineWid=0.5 #线宽
		self.coverColor="r" #保护层线颜色
		self.coreColor="b" #核心混凝土颜色
		self.barColor="k" #纵筋颜色
		self.barMarkSize=1 #散点大小
	def _lineNodeList(self,nodeDict,eleDict):
		"""
		返回每个线单元两端节点的X，Y坐标列表[([x1,x2],[y1,y2])]
		"""
		nEle=len(eleDict)
		keysList=list(eleDict.keys())
		lineList=[]
		for i1 in range(nEle):
			nodeI = eleDict[keysList[i1]][0]
			nodeJ = eleDict[keysList[i1]][1]
			nodeIx = nodeDict[nodeI][0]
			nodeIy = nodeDict[nodeI][1]
			nodeJx = nodeDict[nodeJ][0]
			nodeJy = nodeDict[nodeJ][1]
			lineList.append(([nodeIx,nodeJx],[nodeIy,nodeJy]))
		return lineList

	def sectPlot(self):
		"""
		绘制未划分纤维的截面轮廓
		"""
		###外部轮廓线绘制
		lineList=self._lineNodeList(self.outNode, self.outEle)
		for each1 in lineList:
			self.ax.plot(each1[0],each1[1], self.coverColor,self.lineWid/5,zorder = 0)
		if self.inNode != None:
			for eachNode,eachEle in zip(self.inNode,self.inEle):
				lineList1=self._lineNodeList(eachNode, eachEle)
				for each2 in lineList1:
					self.ax.plot(each2[0],each2[1], self.coverColor,self.lineWid/5,zorder = 0)
		else:
			pass

	def _nearLineIdentify(self,paraList1,paraList2,zhole,yhole):
		"""
		距离坐标轴最近距离线段识别
		输入：
			paraList1,paraList2:交界线特征值[(a1,b1,c1_1,c1_2),(a2,b2,c2_1,c2_2),...]
		返回：
			indexChangeList:识别的位置索引列表[index1,index2]
		"""
		indexChangeList = []
		posit=None
		if zhole == 2 and yhole == 1:
			posit=0
		else:
			posit=1
		horizonNum = []
		horizonValue = []
		for num, value1 in enumerate(paraList1):
			if value1[posit] == 0:
				horizonNum.append(num)
				horizonValue.append(value1[2])
		index1 = horizonValue.index(min(np.abs(horizonValue)))
		indexChange = horizonNum[index1]
		indexChangeList.append((indexChange))
		horizonNum2 = []
		horizonValue2 = []
		for num2, value2 in enumerate(paraList2):
			if value2[posit] == 0:
				horizonNum2.append(num2)
				horizonValue2.append(value2[2])
		index2 = horizonValue2.index(min(np.abs(horizonValue2)))
		indexChange2 = horizonNum2[index2]
		indexChangeList.append((indexChange2))
		return indexChangeList

	def _middleLineNode(self,nodeDict,d0,zhole=1,yhole=1,pos="outLine"):
		"""
		计算分界线各节点的列表
		输入：
			nodeDict:节点字典 {1:(2.3,4.3)}
			d0:保护层厚度
			pos:外侧分界线（"outLinee"),内侧分界线("inLine")
			zhole,yhole:局部z,y向内轮廓数量
		返回：
			NodeList:外分界线节点列表[(x1,y1),(x2,y2),...,(xn,yn)]
		"""
		NodeKeys = list(nodeDict.keys())
		NodeKeys.append(NodeKeys[0])
		NodeKeys.append(NodeKeys[1])
		IterNode = []
		for i1 in range(len(nodeDict)):
			IterNode.append((NodeKeys[i1],NodeKeys[i1 + 1],NodeKeys[i1 + 2]))
		NodeList = []
		paraList1=[]
		paraList2 = []
		for each1 in IterNode:
			nodeI = nodeDict[each1[0]]
			nodeJ = nodeDict[each1[1]]
			nodeK = nodeDict[each1[2]]
			nodeIx, nodeIy = nodeI[0], nodeI[1]
			nodeJx, nodeJy = nodeJ[0], nodeJ[1]
			nodeKx, nodeKy = nodeK[0], nodeK[1]
			a1 = (nodeJy - nodeIy)
			b1 = -(nodeJx - nodeIx)
			c1 = (nodeJx - nodeIx) * nodeIy - (nodeJy - nodeIy) * nodeIx
			a2 = (nodeKy - nodeJy)
			b2 = -(nodeKx - nodeJx)
			c2 = (nodeKx - nodeJx) * nodeJy - (nodeKy - nodeJy) * nodeJx
			c1_1 = c1 - math.sqrt(a1 ** 2 + b1 ** 2) * d0
			c1_2 = c1 + math.sqrt(a1 ** 2 + b1 ** 2) * d0
			c2_1 = c2 - math.sqrt(a2 ** 2 + b2 ** 2) * d0
			c2_2 = c2 + math.sqrt(a2 ** 2 + b2 ** 2) * d0
			paraList1.append((a1,b1,c1_1,c1_2))
			paraList2.append((a2,b2,c2_1,c2_2))
		indexChangeList=None
		if zhole==2 or yhole==2:
			indexChangeList=self._nearLineIdentify(paraList1, paraList2, zhole, yhole)
		for i2 in range(len(paraList1)):
			c1_1=paraList1[i2][2]
			c1_2 = paraList1[i2][3]
			c2_1 = paraList2[i2][2]
			c2_2 = paraList2[i2][3]
			a1=paraList1[i2][0]
			b1 = paraList1[i2][1]
			a2 = paraList2[i2][0]
			b2 = paraList2[i2][1]
			if pos=="outLine":
				c11 = c1_1 if abs(c1_1) < abs(c1_2) else c1_2
			elif indexChangeList==None:
				c11 = c1_2 if abs(c1_1) < abs(c1_2) else c1_1
			else:
				if i2!=indexChangeList[0]:
					c11 = c1_2 if abs(c1_1) < abs(c1_2) else c1_1
				else:
					c11=c1_2 if abs(c1_1) > abs(c1_2) else c1_1

			if pos=="outLine":
				c22 = c2_1 if abs(c2_1) < abs(c2_2) else c2_2
			elif indexChangeList==None:
				c22 = c2_2 if abs(c2_1) < abs(c2_2) else c2_1
			else:
				if i2!=indexChangeList[1]:
					c22 = c2_2 if abs(c2_1) < abs(c2_2) else c2_1
				else:
					c22 = c2_2 if abs(c2_1) > abs(c2_2) else c2_1
			A = np.array([[a1, b1], [a2, b2]])
			B = np.array([-c11, -c22])
			newNode = list(solve(A, B))
			NodeList.append((newNode[0], newNode[1]))
		NodeList.insert(0,NodeList[-1])
		del NodeList[-1]
		return NodeList

	def coverLinePlot(self,d0):
		"""
		通过轮廓线及保护层厚度计算核心混凝土与外侧保护层混凝土交界线
		输入：
			d0:保护层混凝土厚度
		返回：
			returnNodeList:外分界线节点列表[(x1,y1),(x2,y2),...,(xn,yn)]
		"""
		returnNodeList=self._middleLineNode(self.outNode, d0, pos="outLine",zhole=1,yhole=1)
		outNodeDict={(i1+1):returnNodeList[i1] for i1 in range(len(returnNodeList))}
		self.outNewNodeDict=outNodeDict  ##外层混凝土保护层线节点字典，与外轮廓节点一一对应
		outEleDict=self.outEle
		coverlineList = self._lineNodeList(outNodeDict, outEleDict)
		for each2 in coverlineList:
			self.ax.plot(each2[0], each2[1], self.coverColor,self.lineWid/5,zorder = 0)
		return returnNodeList

	def _twoHoleDirect(self,inNodeDictList):
		"""
		判断两个空心所在的方向(若关于Y轴对称，则在Z轴）
		输入：
			inNodeDictList:每个轮廓是一个字典[{1:(1.9,2.4),2:(1.1,3.2),3:(-1.1,3.2),4:(-1.9,2.4)}]
		返回：
			zHole,yHole:Z,Y轴空心的个数
		"""
		xList=[]
		for each in inNodeDictList[0].values():
			xList.append(each[0])
		if max(xList)<0 or min(xList)>0:
			zHole,yHole=1,2
		else:
			zHole,yHole=2,1
		return zHole,yHole

	def innerLinePlot(self,d0):
		"""
		核心混凝土与内轮廓保护层混凝土的分界线绘制
		输入：
			d0--保护层混凝土厚度
		返回：
			innerList:内分界线节点列表[(x1,y1),(x2,y2),...,(xn,yn)]
		"""
		if self.inNode != None:
			zhole,yhole=None,None
			if len(self.inNode)==1:
				zhole,yhole=1,1
			elif len(self.inNode)==2:
				zhole,yhole=self._twoHoleDirect(self.inNode)
			innerList = []
			innerListDict = []
			for eachNode, eachEle in zip(self.inNode, self.inEle):
				returnNodeList = self._middleLineNode(eachNode, d0, zhole, yhole, pos="inLine")
				innerList.append(returnNodeList)
				innerListDict.append({(j1 + 1): returnNodeList[j1] for j1 in range(len(returnNodeList))})
				inNodeDict = {(i1 + 1): returnNodeList[i1] for i1 in range(len(returnNodeList))}
				inEleDict = eachEle
				inlineList = self._lineNodeList(inNodeDict, inEleDict)

				for each2 in inlineList:
					self.ax.plot(each2[0], each2[1], self.coverColor, self.lineWid, zorder=0)
			self.inNewNodeDict = innerListDict
			return innerList

	def _lineSort(self,lineNodeList,xInc=0,yInc=0):
		"""
		封闭曲线以坐标轴对称的节点排序
		输入：
			lineNodeList:曲线节点列表[(x1,y1),(x2,y2),...,(xn,yn)]
			pos:外部轮廓线（outline),内部轮廓线（inLine)
			xInc:按X坐标升序排列
			yInc:按y坐标升序排列
		返回：
			outList1:增序
			outList2:降序
			outmin:最小值
			outmax:最大值
		"""
		outNode1 = []
		outNode2 = []
		outList1=None
		outList2=None
		outmin=None
		outmax=None
		posit=None
		if xInc==1:
			posit=0
			for num, node in enumerate(lineNodeList):
				if node[1] < 0:
					outNode1.append(node)
				else:
					outNode2.append(node)
		else:
			posit = 1
			for num, node in enumerate(lineNodeList):
				if node[0] > 0:
					outNode1.append(node)
				else:
					outNode2.append(node)
		outNode1xy = [each1[posit] for each1 in outNode1]
		index1Out = np.argsort(np.array(outNode1xy))
		outList1 = [outNode1[each2] for each2 in index1Out]
		outNode2xy = [each3[posit] for each3 in outNode2]
		index2Out = np.argsort(-np.array(outNode2xy))
		outList2 = [outNode2[each4] for each4 in index2Out]
		outmin = min(outNode1xy)
		outmax = max(outNode1xy)
		return outList1,outList2,outmin,outmax

	def _twoHolePolygonDivide(self,outLineList,inLineList,zhole,yhole):
		"""
		具有两个内轮廓的多边形核心混凝土划分
		输入：
			outLineList:外分界线节点列表[(x1,y1),(x2,y2),...,(xn,yn)]
			inLineList:内分界线节点列表[[(x1,y1),(x2,y2),...,(xn,yn)],[(x1,y1),(x2,y2),...,(xn,yn)]]
			zhole,yhole:Z，Y轴空心数
		返回:
			list1,list2:多边形1及多边形2节点列表[(x1,y1),(x2,y2),...,(xn,yn)]
		"""
		inLine1=inLineList[0]
		inLine1X=[each1[0] for each1 in inLine1]
		inLine1Y =[each2[1] for each2 in inLine1]
		posit=None
		xInc=None
		yInc=None
		if (zhole==1) and (yhole==2):
			posit=0
			xInc,yInc=1,0
		elif (zhole==2) and (yhole==1):
			posit=1
			xInc, yInc = 0,1
		inLineList0 = [each5[posit] for each5 in inLineList[0]]
		if min(inLineList0) > 0:
			inList1 = inLineList[0]
			inList2 = inLineList[1]
		else:
			inList1 = inLineList[1]
			inList2 = inLineList[0]
		outInc, outDec, outmin, outmax = self._lineSort(outLineList, xInc, yInc)
		inUpperInc, inUpperDec, inUpperMin, inUpperMax = self._lineSort(inList1, xInc, yInc)
		inUpperInc.reverse()
		inUpperDec.reverse()
		inLowerInc, inLowerDec, inLowerMin, inLowerMax = self._lineSort(inList2, xInc, yInc)
		inLowerInc.reverse()
		inLowerDec.reverse()
		list1 = []
		list2 = []
		for each6 in outInc:
			list1.append(each6)
		if (zhole==1) and (yhole==2):
			list1.append((outmax,0))
			list1.append(((inUpperMax,0)))
		else:
			list1.append((0,outmax))
			list1.append(((0,inUpperMax)))

		for each7 in inUpperInc:
			list1.append(each7)
		if (zhole == 1) and (yhole == 2):
			list1.append(( inUpperMin,0))
			list1.append((inLowerMax,0))
		else:
			list1.append((0, inUpperMin))
			list1.append((0, inLowerMax))
		for each8 in inLowerInc:
			list1.append(each8)
		if (zhole == 1) and (yhole == 2):
			list1.append((inLowerMin,0))
			list1.append((outmin,0))
		else:
			list1.append((0, inLowerMin))
			list1.append((0, outmin))

		for each9 in outDec:
			list2.append(each9)
		if (zhole == 1) and (yhole == 2):
			list2.append((outmin,0))
			list2.append((inLowerMin,0))
		else:
			list2.append((0, outmin))
			list2.append((0, inLowerMin))
		for each10 in inLowerDec:
			list2.append(each10)
		if (zhole == 1) and (yhole == 2):
			list2.append((inLowerMax,0))
			list2.append((inUpperMin,0))
		else:
			list2.append((0, inLowerMax))
			list2.append((0, inUpperMin))
		for each11 in inUpperDec:
			list2.append(each11)
		if (zhole == 1) and (yhole == 2):
			list2.append((inUpperMax,0))
			list2.append((outmax,0))
		else:
			list2.append((0, inUpperMax))
			list2.append((0, outmax))
		return list1,list2

	def _triEleInfo(self,nodeNArray,eleNArray):
		"""
		计算生成的三角纤维单元的面积与形心坐标
		输入：
			nodeNArray:节点坐标列表[[x1,y1],[x2,y2]]
			eleNArray:单元列表[[I1,J1,K1],[I2,J2,K2]
		返回：
			inFoList:纤维单元信息列表[(xc1,yc1,area1),(xc2,yc2,area2)]
		"""
		inFoList=[]
		for each in eleNArray:
			I,J,K=each[0],each[1],each[2]
			x1=nodeNArray[I][0]
			y1 = nodeNArray[I][1]
			x2 = nodeNArray[J][0]
			y2 = nodeNArray[J][1]
			x3 = nodeNArray[K][0]
			y3 = nodeNArray[K][1]
			area=0.5*(x1*y2-x2*y1+x2*y3-x3*y2+x3*y1-x1*y3)
			xc=(x1+x2+x3)/3.0
			yc=(y1+y2+y3)/3.0
			inFoList.append((xc,yc,area))
		return inFoList

	def coreMesh(self,eleSize,outLineList,inLineList=None):
		"""
		核心混凝土的划分
		输入：
			eleSize:纤维单元的边长
			outLineList:外分界线节点列表[(x1,y1),(x2,y2),...,(xn,yn)]
			inLineList:内分界线节点列表[[(x1,y1),(x2,y2),...,(xn,yn)],[(x1,y1),(x2,y2),...,(xn,yn)]]
		返回：
			triEleInfoList:纤维单元信息列表[(xc1,yc1,area1),(xc2,yc2,area2)]
		"""
		triEleInfoList=None
		if inLineList==None:
			geo=dmsh.Polygon(outLineList)
			points, elements = dmsh.generate(geo, eleSize)
			triEleInfoList = self._triEleInfo(points, elements)
			self.ax.triplot(points[:, 0], points[:, 1], elements, c=self.coreColor, linewidth=self.lineWid, zorder=0)
		elif len(inLineList)==1:
			geo = dmsh.Difference(
				dmsh.Polygon(outLineList),
				dmsh.Polygon(inLineList[0]),
			)
			points, elements = dmsh.generate(geo, eleSize)
			triEleInfoList = self._triEleInfo(points, elements)
			self.ax.triplot(points[:,0],points[:,1],elements,c=self.coreColor,linewidth=self.lineWid, zorder=0)

		elif len(inLineList)==2:
			zhole,yhole=self._twoHoleDirect(self.inNode)
			list1,list2=self._twoHolePolygonDivide(outLineList, inLineList,zhole,yhole)
			geo1= dmsh.Polygon(list1)
			geo2 = dmsh.Polygon(list2)
			points1, elements1 = dmsh.generate(geo1, eleSize)
			points2, elements2 = dmsh.generate(geo2, eleSize)
			triEleInfoList1=self._triEleInfo(points1,elements1)
			triEleInfoList2 = self._triEleInfo(points2, elements2)
			triEleInfoList=triEleInfoList1+triEleInfoList2
			self.ax.triplot(points1[:, 0], points1[:, 1], elements1,c=self.coreColor,linewidth=self.lineWid,zorder = 0)
			self.ax.triplot(points2[:, 0], points2[:, 1], elements2, c=self.coreColor,linewidth=self.lineWid,zorder=0)
		return triEleInfoList

	def _coverDivide(self,outNodeDict,inNodeDict,eleDict,size,d0):
		"""
		保护层混凝土的分割
		输入:
			outNodeDict:外侧轮廓节点字典--{1:(3.5,3),2:(1.5,5),3:(-1.5,5),4:(-3.5,3)}
			inNodeDict:内侧轮廓节对应点字典--{1:(2.5,2),2:(0.5,4),3:(-0.5,4),4:(-2.5,2)}
			eleDict:外侧轮廓单元字典:--{1:(1,2),2:(2,3),3:(3,4),4:(4,1)}
			size:保护层混凝土纤维单元尺寸
			d0:混凝土保护层厚度
		返回：
			centerCoordList:保护层纤维单元中心坐标及面积列表--[(xc1,yc1,A1),(xc2,yc2,A2),...,)
			outPlotNode:外侧分割后各个节点坐标列表--[(x1,y1),(x2,y2),...,(xn,yn)]
			inPlotNode:内侧分割后各个节点坐标列表--[(xin1,yin1),...,(xinn,yinn)]
		"""
		nLine=len(eleDict)
		outPlotNode=[]
		inPlotNode=[]
		centerCoordList=[]
		for i1 in range(1,nLine+1):
			nodeI=eleDict[i1][0]
			nodeJ=eleDict[i1][1]
			outNodeIx=outNodeDict[nodeI][0]
			outNodeIy=outNodeDict[nodeI][1]
			outNodeJx=outNodeDict[nodeJ][0]
			outNodeJy=outNodeDict[nodeJ][1]
			inNodeIx=inNodeDict[nodeI][0]
			inNodeIy=inNodeDict[nodeI][1]
			inNodeJx=inNodeDict[nodeJ][0]
			inNodeJy=inNodeDict[nodeJ][1]
			length=math.sqrt((outNodeJx-outNodeIx)**2+(outNodeJy-outNodeIy)**2)
			nEle=int(length/size)
			totalOutNodeList=[]
			totalInNodeList=[]
			totalOutNodeList.append((outNodeIx,outNodeIy))
			totalInNodeList.append((inNodeIx,inNodeIy))
			for i2 in range(1,nEle):
				outxi=((nEle-i2)*outNodeIx+i2*outNodeJx)/nEle  #n等分点公式
				outyi=((nEle-i2)*outNodeIy+i2*outNodeJy)/nEle
				inxi=((nEle-i2)*inNodeIx+i2*inNodeJx)/nEle
				inyi = ((nEle - i2)*inNodeIy+i2*inNodeJy) / nEle
				totalOutNodeList.append((outxi,outyi))
				totalInNodeList.append((inxi,inyi))
			totalOutNodeList.append((outNodeJx,outNodeJy))
			totalInNodeList.append((inNodeJx, inNodeJy))
			inLength=math.sqrt((totalInNodeList[1][0]-totalInNodeList[0][0])**2\
							   +(totalInNodeList[1][1]-totalInNodeList[0][1])**2)
			outLength=math.sqrt((totalOutNodeList[1][0]-totalOutNodeList[0][0])**2+\
								(totalOutNodeList[1][1]-totalOutNodeList[0][1])**2)
			eleArea=(inLength+outLength)*d0/2.0
			for j2 in range(len(totalOutNodeList)-1):
				outPlotNode.append(totalOutNodeList[j2])
				inPlotNode.append(totalInNodeList[j2])
			for i3 in range(len(totalOutNodeList)-1):
				outI=totalOutNodeList[i3]
				outJ=totalOutNodeList[i3+1]
				inI=totalInNodeList[i3]
				inJ=totalInNodeList[i3+1]
				outCenter=((outI[0]+outJ[0])/2.0,(outI[1]+outJ[1])/2.0)
				inCenter=((inI[0]+inJ[0])/2.0,(inI[1]+inJ[1])/2.0)
				centerCoord=((outCenter[0]+inCenter[0])/2.0,(outCenter[1]+inCenter[1])/2.0,eleArea) #纤维中心坐标及其面积
				centerCoordList.append(centerCoord)
		return centerCoordList,outPlotNode,inPlotNode

	def coverMesh(self,size,d0):
		"""
		保护层混凝土的划分
		输入：
			size：核心混凝土纤维尺寸
			d0：保护层厚度
		返回：
			coverFiberInfo:保护层混凝土纤维单元[(xc1,yc1,area1),(xc2,yc2,area2)]
		"""
		coverFiberInfo=None
		nodeOutDict=self.outNode
		eleOutDict=self.outEle
		nodeNewOutDict=self.outNewNodeDict# 新生成的外侧保护层混凝土线节点字典
		nodeNewInDict=self.inNewNodeDict# 新生成的内侧保护层混凝土线节点字典列表
		nodeInDict=self.inNode
		eleInDict=self.inEle
		fiberInfo,outNodeInfo,inNodeInfo=self._coverDivide(nodeOutDict,nodeNewOutDict,eleOutDict,size,d0)
		coverFiberInfo=fiberInfo
		outNodeInfo.append(outNodeInfo[0])
		inNodeInfo.append(inNodeInfo[0])
		xList=[]
		yList=[]
		areaList=[]
		for each1 in fiberInfo:
			xList.append(each1[0])
			yList.append(each1[1])
			areaList.append(each1[2])
		# self.ax.scatter(xList,yList,s=2,c="r")
		for i1 in range(len(outNodeInfo)-1):
			self.ax.plot([inNodeInfo[i1][0],outNodeInfo[i1][0]],[inNodeInfo[i1][1],outNodeInfo[i1][1]],self.coverColor,\
						 linewidth=self.lineWid/5,zorder = 0)
		for i2 in range(len(outNodeInfo)-1):
			self.ax.plot([inNodeInfo[i2][0], inNodeInfo[i2+1][0]], [inNodeInfo[i2][1], inNodeInfo[i2+1][1]], \
						 self.coverColor,linewidth=self.lineWid/5,zorder = 0)
		for i3 in range(len(outNodeInfo)-1):
			self.ax.plot([outNodeInfo[i3][0], outNodeInfo[i3+1][0]], [outNodeInfo[i3][1], outNodeInfo[i3+1][1]],\
						 self.coverColor,linewidth=self.lineWid/5,zorder = 0)
		##内部保护层混凝土的划分
		if self.inNode != None:
			nInhole=len(self.inNode)
			inxList = []
			inyList = []
			inareaList = []
			for i4 in range(nInhole):
				Innerfiber, innerOut, innerIn = self._coverDivide(nodeInDict[i4],nodeNewInDict[i4],eleInDict[i4], size,d0)
				coverFiberInfo=coverFiberInfo+Innerfiber

				innerOut.append(innerOut[0])
				innerIn.append(innerIn[0])
				for each2 in Innerfiber:
					inxList.append(each2[0])
					inyList.append(each2[1])
					inareaList.append(each2[2])
				for i5 in range(len(innerOut)-1):
					self.ax.plot([innerOut[i5][0], innerIn[i5][0]], [innerOut[i5][1], innerIn[i5][1]], \
								 self.coverColor,linewidth=self.lineWid/5,zorder = 0)
				for i6 in range(len(innerOut)-1):
					self.ax.plot([innerIn[i6][0], innerIn[i6 + 1][0]], [innerIn[i6][1], innerIn[i6 + 1][1]],\
								 self.coverColor,linewidth=self.lineWid/5,zorder = 0)
				for i7 in range(len(innerIn)-1):
					self.ax.plot([innerOut[i7][0], innerOut[i7 + 1][0]],[innerOut[i7][1],innerOut[i7 + 1][1]],\
								 self.coverColor,linewidth=self.lineWid/5,zorder = 0)
			# self.ax.scatter(inxList,inyList,s=2,c="r")
		return coverFiberInfo

	def _innerBarLineDict(self,barToEdgeDist):
		"""
		核心混凝土与内轮廓保护层混凝土的分界线绘制
		输入：
			d--保护层混凝土厚度+内层钢筋直径/2
		返回：
			innerList:内分界线节点列表[(x1,y1),(x2,y2),...,(xn,yn)]
		"""
		if self.inNode != None:
			zhole,yhole=None,None
			if len(self.inNode)==1:
				zhole,yhole=1,1
			elif len(self.inNode)==2:
				zhole,yhole=self._twoHoleDirect(self.inNode)
			innerListDict = []
			for eachNode, eachEle in zip(self.inNode, self.inEle):
				returnNodeList = self._middleLineNode(eachNode, barToEdgeDist, zhole, yhole, pos="inLine")
				innerListDict.append({(j1 + 1): returnNodeList[j1] for j1 in range(len(returnNodeList))})
			return innerListDict

	def _outBarLineNode(self, barToEdgeDist):
		"""
		计算外侧钢筋所在直线交点坐标
		输入：barToEdgeDist-钢筋中心到混凝土边缘最短距离
		输出: outBarLineNodeDict-钢筋中心交点坐标字典 {1:(x1,y1),2:(x2,y2),...,n:(xn,yn)}
		"""
		# 计算分界线节点列表[(x1, y1), (x2, y2), ..., (xn, yn)]
		returnNodeList = self._middleLineNode(self.outNode, barToEdgeDist, pos="outLine")
		outBarLineNodeDict = {(i1 + 1): returnNodeList[i1] for i1 in range(len(returnNodeList))}
		return outBarLineNodeDict



	def _barDivide(self,barD,barDist,nodeDict,lineEleDict):
		"""
		钢筋纤维的划分
		输入：
			barD-单个纵筋直径
			barDist-纵筋间距
			nodeDict-钢筋线节点字典 {1:(x1,y1),2:(x2,y2),...,(xn,yn)}
			lineEleDict-钢筋线单元字典 {1:(1,2),2:(2,3),3:(3,1)}
		返回：
			barFiberList:钢筋纤维单元列表 [(xb1,yb1,A1),(xb2,yb2,A2),...,(xbn,ybn,An)]
			xRetrunList:钢筋纤维横坐标列表[xb1,xb2,...,xbn]
			yReturnList:钢筋纤维纵坐标列表[yb1,yb2,...,ybn]
		"""
		area=np.pi*barD**2/4.0
		nLine = len(lineEleDict)
		barFiberList = []
		xReturnList=[]
		yReturnList=[]
		for i1 in range(1, nLine + 1):
			nodeI = lineEleDict[i1][0]
			nodeJ = lineEleDict[i1][1]
			nodeIx = nodeDict[nodeI][0]
			nodeIy = nodeDict[nodeI][1]
			nodeJx = nodeDict[nodeJ][0]
			nodeJy =nodeDict[nodeJ][1]
			length = math.sqrt((nodeJx - nodeIx) ** 2 + (nodeJy - nodeIy) ** 2)
			nEle = int(length /barDist)
			lineBarCoorList = []
			lineBarCoorList.append((nodeIx, nodeIy))
			for i2 in range(1, nEle):
				outxi = ((nEle - i2) * nodeIx + i2 * nodeJx) / nEle  # n等分点公式
				outyi = ((nEle - i2) * nodeIy + i2 * nodeJy) / nEle
				lineBarCoorList.append((outxi, outyi))
			for i3 in range(len(lineBarCoorList)):
				barFiberList.append((lineBarCoorList[i3][0],lineBarCoorList[i3][1],area))
				xReturnList.append(lineBarCoorList[i3][0])
				yReturnList.append(lineBarCoorList[i3][1])
		return barFiberList,xReturnList,yReturnList

	def barMesh(self,d0,outBarD,outBarDist,inBarD=None,inBarDist=None):
		"""
		钢筋纤维的划分
		输入：
			outBarD：外轮廓钢筋直径
			outBarDist：外轮廓钢筋间距
			inBarD：内轮廓钢筋直径
			inBarDist：内轮廓钢筋间距
		返回：
			barFiberInfo:钢筋纤维单元信息[(xc1,yc1,area1),(xc2,yc2,area2)]
		"""
		barFiberInfo=None
		outBarLineDict=self._outBarLineNode(d0+outBarD/2)  ##外层混凝土保护层线节点字典，与外轮廓节点一一对应
		outBarListEle=self.outEle

		#外侧钢筋的划分
		outBarFiber,outXList,outYList=self._barDivide(outBarD,outBarDist,outBarLineDict,outBarListEle)
		barFiberInfo=outBarFiber
		self.ax.scatter(outXList,outYList,s=self.barMarkSize,c=self.barColor,linewidth=self.lineWid,zorder = 2)
		if self.inNode != None:
			inBarLineDict = self._innerBarLineDict(d0+inBarD/2)
			inBarLineEle = self.inEle
			nEle=len(inBarLineEle)
			for i1 in range(nEle):
				inBarFiber, inXList, inYList = self._barDivide(inBarD, inBarDist, inBarLineDict[i1], inBarLineEle[i1])
				barFiberInfo=barFiberInfo+inBarFiber
				self.ax.scatter(inXList, inYList, s=self.barMarkSize, c=self.barColor,linewidth=self.lineWid, zorder=2)
		return barFiberInfo

	def multiBarMesh(self,d0,outBarDist1,outBarD1,outBarNodeDict1,outBarEleDict1,outBarDist2,outBarD2,outBarNodeDict2,outBarEleDict2,inBarD=None,inBarDist=None):
		"""
		钢筋纤维的划分
		输入：
			outBarD：外轮廓钢筋直径
			outBarDist：外轮廓钢筋间距
			inBarD：内轮廓钢筋直径
			inBarDist：内轮廓钢筋间距
			barNodeDict：钢筋不直节点
			barEleDict：钢筋分布连线
		返回：
			barFiberInfo:钢筋纤维单元信息[(xc1,yc1,area1),(xc2,yc2,area2)]
		"""

		barFiberInfo=None

		outBarFiber1, outXList1, outYList1 = self._barDivide(outBarD1, outBarDist1, outBarNodeDict1, outBarEleDict1)
		barFiberInfo1 = outBarFiber1
		self.ax.scatter(outXList1, outYList1, s=self.barMarkSize, c=self.barColor, linewidth=self.lineWid, zorder=2)

		outBarFiber2, outXList2, outYList2 = self._barDivide(outBarD2, outBarDist2, outBarNodeDict2, outBarEleDict2)
		barFiberInfo2 = outBarFiber2
		self.ax.scatter(outXList2, outYList2, s=self.barMarkSize, c=self.barColor, linewidth=self.lineWid, zorder=2)
		barFiberInfo = barFiberInfo1 + barFiberInfo2

		if self.inNode != None:
			inBarLineDict = self._innerBarLineDict(d0+inBarD/2)
			inBarLineEle = self.inEle
			nEle=len(inBarLineEle)
			for i1 in range(nEle):
				inBarFiber, inXList, inYList = self._barDivide(inBarD, inBarDist, inBarLineDict[i1], inBarLineEle[i1])
				barFiberInfo=barFiberInfo1+barFiberInfo2+inBarFiber
				self.ax.scatter(inXList, inYList, s=self.barMarkSize, c=self.barColor,linewidth=self.lineWid, zorder=2)
		return barFiberInfo

	def figureSize(self, outSideNode):
		"""
		计算图形窗口的宽与高
		输入：outSideNode-外侧轮廓节点字典{1:(x1,x2),2(x2,y2),...,n:(xn,yn)}
		输出：figSize-图形窗口宽与高列表 [w,h]
		"""
		dictValues = outSideNode.values()
		xValues = [each1[0] for each1 in dictValues]
		yValues = [each2[1] for each2 in dictValues]
		minX, maxX = min(xValues), max(xValues)
		minY, maxY = min(yValues), max(yValues)
		w = np.abs(maxX - minX)
		h = np.abs(maxY - minY)
		return [w, h]


class CircleSection():
	"""
	圆形截面
	"""
	def __init__(self,ax,d0,outD,inD=None):
		"""
		fig,ax--绘图环境
		"""
		self.ax=ax
		self.d0=d0
		self.outD=outD
		self.inD=inD

	def sectPlot(self):
		"""
		初始截面的绘制
		"""
		theta = np.arange(0, 2 * np.pi, 0.01)
		outxList =(self.outD/2.0)*np.cos(theta)
		outyList=(self.outD/2.0)*np.sin(theta)
		self.ax.plot(outxList,outyList,"r",linewidth=1,zorder=2)
		if self.inD!=None:
			inxList=(self.inD/2.0)*np.cos(theta)
			inyList=(self.inD/2.0)*np.sin(theta)
			self.ax.plot(inxList,inyList,"r",linewidth=1,zorder=2)

	def _triEleInfo(self,nodeNArray,eleNArray):
		"""
		计算生成的三角纤维单元的面积与形心坐标
		输入：
			nodeNArray:节点坐标列表[[x1,y1],[x2,y2]]
			eleNArray:单元列表[[I1,J1,K1],[I2,J2,K2]
		返回：
			inFoList:纤维单元信息列表[(xc1,yc1,area1),(xc2,yc2,area2)]
		"""
		inFoList=[]
		for each in eleNArray:
			I,J,K=each[0],each[1],each[2]
			x1 = nodeNArray[I][0]
			y1 = nodeNArray[I][1]
			x2 = nodeNArray[J][0]
			y2 = nodeNArray[J][1]
			x3 = nodeNArray[K][0]
			y3 = nodeNArray[K][1]
			area=0.5*(x1*y2-x2*y1+x2*y3-x3*y2+x3*y1-x1*y3)
			xc=(x1+x2+x3)/3.0
			yc=(y1+y2+y3)/3.0
			inFoList.append((xc,yc,area))
		return inFoList

	def coreMesh(self,eleSize):
		"""
		核心混凝土的划分
		输入：
			eleSize：核心区纤维单元大小
		返回：
			coreFiberInfo:核心混凝土纤维单元列表[(xc1,yc1,area1),(xc2,yc2,area2)]
		"""
		outDNew=self.outD-self.d0*2.0
		if self.inD!=None:
			inDNew=self.inD+self.d0*2.0
			geo = dmsh.Difference(dmsh.Circle([0, 0], outDNew/2.0), dmsh.Circle([0, 0.0],inDNew/2.0))
			points, elements= dmsh.generate(geo, eleSize)
			coreFiberInfo=self._triEleInfo(points,elements)
			self.ax.triplot(points[:, 0], points[:, 1], elements)
		else:
			geo = dmsh.Circle([0.0, 0.0],outDNew/2.0)
			points, elements = dmsh.generate(geo,eleSize)
			coreFiberInfo = self._triEleInfo(points, elements)
			self.ax.triplot(points[:, 0], points[:, 1], elements)
		return coreFiberInfo

	def _coverDivide(self,coverSize,pos="out"):
		"""
		保护层混凝土的分割
		coverSize-纤维单元大小
		pos-外轮廓("out"),内轮廓("in)"
		"""
		if pos=="out":
			D=self.outD
			DNew = self.outD - self.d0 * 2.0
			circumLength = np.pi * self.outD
			Area = (np.pi * self.outD ** 2) / 4.0
			NewArea = (np.pi *DNew ** 2) / 4.0
			nCover = int(circumLength / coverSize)
			coverArea = (Area - NewArea) / nCover
			R = self.outD / 2.0
			NewR = DNew / 2.0
		elif pos=="in":
			D = self.inD
			DNew = self.inD + self.d0 * 2.0
			circumLength = np.pi * D
			Area = (np.pi * D ** 2) / 4.0
			NewArea = (np.pi * DNew ** 2) / 4.0
			nCover = int(circumLength / coverSize)
			coverArea = (NewArea-Area) / nCover
			R = self.inD / 2.0
			NewR = DNew / 2.0
		Angle = 2 * np.pi / nCover
		NodeList = [(R * np.cos(Angle * i1), R * np.sin(Angle * i1)) for i1 in range(nCover)]
		NewNodeList = [(NewR * np.cos(Angle * i2), NewR * np.sin(Angle * i2)) for i2 in range(nCover)]
		fiberNCover = nCover
		fiberAngle = (2 * np.pi) / fiberNCover
		FiberRadius = (D + DNew) / 4.0
		FiberXList = [FiberRadius * np.cos((2*i3-1) *0.5*fiberAngle) for i3 in range(1, fiberNCover + 1)]
		FiberYList = [FiberRadius * np.sin((2*i4-1) * 0.5*fiberAngle) for i4 in range(1, fiberNCover + 1)]
		coverFiberInfo = [(xc, yc, coverArea) for xc, yc in zip(FiberXList, FiberYList)]
		return coverFiberInfo,FiberXList,FiberYList,NodeList,NewNodeList

	def coverMesh(self,coverSize):
		"""
		保护层混凝土的划分
		输入：
			coverSize：保护层混凝土单元的大小
		返回：
			coverFiberInfo：保护层 混凝土纤维列表[(xc1,yc1,area1),(xc2,yc2,area2)]
		"""
		coverFiberInfo=None
		outCoverFiberInfo,outFiberXList,outFiberYList,outNodeList,outNewNodeList=self._coverDivide(coverSize, pos="out")
		coverFiberInfo=outCoverFiberInfo
		outDNew=self.outD-2.0*self.d0
		theta = np.arange(0, 2 * np.pi, 0.01)
		outThetaX=(outDNew/2.0)*np.cos(theta)
		outThetaY=(outDNew/2.0)*np.sin(theta)
		self.ax.plot(outThetaX,outThetaY,"r",linewidth=1,zorder=2)
		# self.ax.scatter(outFiberXList,outFiberYList,s=10,c="k",zorder = 2)
		for i5 in range(len(outNodeList)):
			xList=[outNodeList[i5][0],outNewNodeList[i5][0]]
			yList=[outNodeList[i5][1],outNewNodeList[i5][1]]
			self.ax.plot(xList,yList,"r",linewidth=1,zorder=2)
		if self.inD!=None:
			inDNew = self.inD + 2.0 * self.d0
			inCoverFiberInfo, inFiberXList, inFiberYList, inNodeList, inNewNodeList\
				= self._coverDivide(coverSize, pos="in")
			coverFiberInfo=coverFiberInfo+inCoverFiberInfo
			inThetaX = (inDNew / 2.0) * np.cos(theta)
			inThetaY = (inDNew / 2.0) * np.sin(theta)
			self.ax.plot(inThetaX, inThetaY, "r", linewidth=1, zorder=2)
			# self.ax.scatter(inFiberXList,inFiberYList,s=10,c="k",zorder = 2)
			for i5 in range(len(inNodeList)):
				xList = [inNodeList[i5][0], inNewNodeList[i5][0]]
				yList = [inNodeList[i5][1], inNewNodeList[i5][1]]
				self.ax.plot(xList, yList, "r", linewidth=1, zorder=2)
		return coverFiberInfo

	def _barDivide(self,barD,barDist,pos="out"):
		"""
		纵向纤维截面
		"""
		area=(np.pi*barD**2)/4.0
		if pos=="out":
			newR=(self.outD-2.0*self.d0-barD)/2.0
		elif pos=="in":
			newR=(self.inD+2*self.d0+barD)/2.0
		circumLength = 2 * np.pi * newR
		nBar=int(circumLength/barDist)
		angle=(2*np.pi)/nBar
		fiberXList=[newR*np.cos(angle*i1) for i1 in range(1,nBar+1)]
		fiberYList=[newR*np.sin(angle*i2) for i2 in range(1,nBar+1)]
		barFiberInfo=[(xb,yb,area) for xb,yb in zip(fiberXList,fiberYList)]
		return barFiberInfo,fiberXList,fiberYList


	def barMesh(self,outBarD,outBarDist,inBarD=None,inBarDist=None):
		"""
		纵筋的纤维划分
		输入：
			outBarD：外轮廓纵筋的直径
			outBarDist：外轮廓纵筋的间距
			inBarD：内轮廓纵筋的直径
			inBarDist:内轮廓纵筋的间距
		返回:
			barFiberInfo:纵筋纤维列表[(xc1,yc1,area1),(xc2,yc2,area2)]
		"""
		barFiberInfo=None
		outFiberInfo,outFiberXList,outFiberYList=self._barDivide(outBarD, outBarDist, pos="out")
		barFiberInfo=outFiberInfo
		self.ax.scatter(outFiberXList,outFiberYList,s=15,c="k",zorder = 3)
		if self.inD!=None:
			inFiberInfo, inFiberXList, inFiberYList = self._barDivide(inBarD, inBarDist, pos="in")
			barFiberInfo=barFiberInfo+inFiberInfo
			self.ax.scatter(inFiberXList, inFiberYList, s=15, c="k", zorder=3)
		return barFiberInfo

	def figureSize(self, outSideNode):
		"""
		计算图形窗口的宽与高
		输入：outSideNode-外侧轮廓节点字典{1:(x1,x2),2(x2,y2),...,n:(xn,yn)}
		输出：figSize-图形窗口宽与高列表 [w,h]
		"""
		dictValues = outSideNode.values()
		xValues = [each1[0] for each1 in dictValues]
		yValues = [each2[1] for each2 in dictValues]
		minX, maxX = min(xValues), max(xValues)
		minY, maxY = min(yValues), max(yValues)
		w = np.abs(maxX - minX)
		h = np.abs(maxY - minY)
		return [w, h]

# if __name__=="__main__":
	#########---多边形截面内有一个洞---####################################################
	##########################---上塔柱截面---############################################

	#截面外部轮廓节点及其坐标,逆时针编码,从小到大
	# outSideNode={1:(3.5,3),2:(1.5,5),3:(-1.5,5),4:(-3.5,3),5:(-3.5,-3),6:(-1.5,-5),7:(1.5,-5),8:(3.5,-3)}
	# #截面外部轮廓单元及其节点与类型
	# outSideEle={1:(1,2),2:(2,3),3:(3,4),4:(4,5),5:(5,6),6:(6,7),7:(7,8),8:(8,1)}
	# inSideNode=[{1:(2.5,1),2:(1,1),3:(1,3.5),4:(-1,3.5),5:(-1,1),6:(-2.5,1),
	# 			7:(-2.5,-1),8:(-1,-1),9:(-1,-3.5),10:(1,-3.5),11:(1,-1),12:(2.5,-1)}]
	# inSideEle=[{1:(1,2),2:(2,3),3:(3,4),4:(4,5),5:(5,6),6:(6,7),7:(7,8),8:(8,9),9:(9,10),10:(10,11),11:(11,12),12:(12,1)}]
	######################################################################################
	##########################---中塔柱截面---#############################################
	# outSideNode={1:(3.5,3),2:(1.5,5),3:(-1.5,5),4:(-3.5,3),5:(-3.5,-3),6:(-1.5,-5),7:(1.5,-5),8:(3.5,-3)}
	# outSideEle = {1: (1, 2), 2: (2, 3), 3: (3, 4), 4: (4, 5), 5: (5, 6), 6: (6, 7), 7: (7, 8), 8: (8, 1)}
	# inSideNode=[{1:(1.9,2.4),2:(1.1,3.2),3:(-1.1,3.2),4:(-1.9,2.4),5:(-1.9,-2.4),6:(-1.1,-3.2),7:(1.1,-3.2),8:(1.9,-2.4)}]
	# inSideEle = [{1: (1, 2), 2: (2, 3), 3: (3, 4), 4: (4, 5), 5: (5, 6), 6: (6, 7), 7: (7, 8), 8: (8, 1)}]
	######################################################################################
	##########################---下塔柱截面---#############################################

	#########---多边形截面内有两个洞（z向）--###############################################
	# outSideNode = {1: (4.5,6.655), 2: (2.5, 8.655), 3: (-2.5,8.655), 4: (-4.5, 6.655), 5: (-4.5, -6.655), 6: (-2.5, -8.655), 7: (2.5, -8.655),
	# 			   8: (4.5, -6.655)}
	# outSideEle = {1: (1, 2), 2: (2, 3), 3: (3, 4), 4: (4, 5), 5: (5, 6), 6: (6, 7), 7: (7, 8), 8: (8, 1)}
	# inSideNode = [{1: (2.5, 5.855), 2: (1.7, 6.655), 3: (-1.7,6.655), 4: (-2.5, 5.855), 5: (-2.5, 1.3), 6: (-1.7, 0.5), 7: (1.7, 0.5),8: (2.5,1.3)},
	# 			  {1:(2.5,-1.3),2:(1.7,-0.5),3:(-1.7,-0.5),4:(-2.5,-1.3),5:(-2.5,-5.855),6:(-1.7,-6.655),7:(1.7,-6.655),8:(2.5,-5.855)}]
	# inSideEle = [{1: (1, 2), 2: (2, 3), 3: (3, 4), 4: (4, 5), 5: (5, 6), 6: (6, 7), 7: (7, 8), 8: (8, 1)},{1: (1, 2), 2: (2, 3), 3: (3, 4), 4: (4, 5), 5: (5, 6), 6: (6, 7), 7: (7, 8), 8: (8, 1)}]
	######################################################################################
	# ########---多边形截面内有两个洞（y向）--###############################################
	# outSideNode = {1: (-5, -5), 2: (5, -5), 3: (5, 5), 4: (-5, 5)}
	# outSideEle = {1: (1, 2), 2: (2, 3), 3: (3, 4), 4: (4, 1)}
	# inSideNode = [{1: (-3, -3), 2: (-1, -3), 3: (-1, 3), 4: (-3, 3)}, {1: (1, -3), 2: (3, -3), 3: (3, 3), 4: (1, 3)}]
	# inSideEle = [{1: (1, 2), 2: (2, 3), 3: (3, 4), 4: (4, 1)}, {1: (1, 2), 2: (2, 3), 3: (3, 4), 4: (4, 1)}]
	# #####################################################################################
	# fig = plt.figure(figsize=(5, 5))
	# ax = fig.add_subplot(111)
	# d0 = 0.4  # 保护层厚度
	# eleSize = 0.5  # 核心纤维的大小
	# coverSize = 0.5  # 保护层纤维大小
	# outBarDist = 0.4
	# outBarD = 0.032
	# inBarDist = 0.4
	# inBarD = 0.032
	# sectInstance = PolygonSection(ax, outSideNode, outSideEle, inSideNode, inSideEle)
	# sectInstance.sectPlot()
	# outLineList = sectInstance.coverLinePlot(d0)
	# inLineList = sectInstance.innerLinePlot(d0)
	# coreFiber=sectInstance.coreMesh(eleSize, outLineList, inLineList)
	# coverFiber=sectInstance.coverMesh(coverSize, d0)
	# barFiber=sectInstance.barMesh(outBarD, outBarDist, inBarD, inBarDist)
	# ax.tick_params(direction='in', labelsize=6)
	# if not os.path.exists('SectionFig'):
	# 	os.makedirs('SectionFig')
	# plt.savefig("SectionFig/PolygonSection.eps", dpi=300, bbox_inches="tight")
	# plt.savefig("SectionFig/PolygonSection.png", dpi=300, bbox_inches="tight")
	# plt.show()
	#
	# fig1 = plt.figure(figsize=(5, 5))
	# ax1 = fig1.add_subplot(111)
	# coreFiberXList=[each1[0] for each1 in coreFiber]
	# coreFiberYList = [each1[1] for each1 in coreFiber]
	# coreFiberAreaList = [each1[2] for each1 in coreFiber]
	# coverFiberXList = [each1[0] for each1 in coverFiber]
	# coverFiberYList = [each1[1] for each1 in coverFiber]
	# coverFiberAreaList = [each1[2] for each1 in coverFiber]
	# barFiberXList = [each1[0] for each1 in barFiber]
	# barFiberYList = [each1[1] for each1 in barFiber]
	# barFiberAreaList = [each1[2] for each1 in barFiber]
	#
	# ax1.scatter(coreFiberXList, coreFiberYList, s=5, c="b", zorder=3)
	# ax1.scatter(coverFiberXList, coverFiberYList, s=5, c="r", zorder=3)
	# ax1.scatter(barFiberXList, barFiberYList, s=5, c="k", zorder=3)
	# ax1.tick_params(direction='in', labelsize=6)
	# if not os.path.exists('SectionFig'):
	# 	os.makedirs('SectionFig')
	# plt.savefig("SectionFig/PolygonSectionFiber.eps", dpi=300, bbox_inches="tight")
	# plt.savefig("SectionFig/PolygonSectionFiber.png", dpi=300, bbox_inches="tight")
	# plt.show()
	# ######################################################################################


	# ########################################---圆形截面---################################
	# fig =	plt.figure(figsize=(5, 5))
	# ax = fig.add_subplot(111)
	# outbarD =	0.03  #	纵向钢筋直径
	# outbarDist = 0.15	 # 纵向钢筋间距
	# inBarD = 0.03
	# inBarDist	= 0.15
	# coverThick = 0.1	# 保护层混凝土厚度
	# coreEleSize =	0.1	 # 核心纤维的大小
	# coverEleSize = 0.15  # 保护层纤维大小
	# outDiameter =	2	# 截面外圆直径
	# innerDiameter	= 1	#截面内圆直径
	# circleInstance = CircleSection(ax, coverThick, outDiameter,innerDiameter)
	# circleInstance.sectPlot()
	# coreFiber=circleInstance.coreMesh(coreEleSize)
	# coverFiber = circleInstance.coverMesh(coverEleSize)
	# barFiber = circleInstance.barMesh(outbarD, outbarDist,inBarD,inBarDist)
	# ax.tick_params(direction='in', labelsize=6)
	# if not os.path.exists('SectionFig'):
	# 	os.makedirs('SectionFig')
	# plt.savefig("SectionFig/CricleSection.eps", dpi=300, bbox_inches="tight")
	# plt.savefig("SectionFig/CricleSection.png", dpi=300, bbox_inches="tight")
	# plt.show()
	#
	# fig1 = plt.figure(figsize=(5,	5))
	# ax1 = fig1.add_subplot(111)
	# coreFiberXList = [each1[0] for each1 in coreFiber]
	# coreFiberYList = [each1[1] for each1 in coreFiber]
	# coreFiberAreaList	= [each1[2]	for	each1 in coreFiber]
	# coverFiberXList =	[each1[0] for each1	in coverFiber]
	# coverFiberYList =	[each1[1] for each1	in coverFiber]
	# coverFiberAreaList = [each1[2] for each1 in coverFiber]
	# barFiberXList	= [each1[0]	for	each1 in barFiber]
	# barFiberYList	= [each1[1]	for	each1 in barFiber]
	# barFiberAreaList = [each1[2] for each1 in	barFiber]
	# ax1.tick_params(direction='in', labelsize=6)
	# ax1.scatter(coreFiberXList, coreFiberYList, s=5, c="b", zorder=3)
	# ax1.scatter(coverFiberXList, coverFiberYList,	s=5, c="r",	zorder=3)
	# ax1.scatter(barFiberXList, barFiberYList,	s=5, c="k",	zorder=3)
	# ax.tick_params(direction='in', labelsize=6)
	# if not os.path.exists('SectionFig'):
	# 	os.makedirs('SectionFig')
	# plt.savefig("SectionFig/CricleSectionFiber.eps", dpi=300, bbox_inches="tight")
	# plt.savefig("SectionFig/CricleSectionFiber.png", dpi=300, bbox_inches="tight")
	# plt.show()
