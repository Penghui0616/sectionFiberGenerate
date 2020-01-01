#-*-coding: UTF-8-*-
import subprocess
import dmsh
import optimesh
import meshio
import matplotlib.pyplot as plt
import numpy as np
from scipy.linalg import solve
import math
######################################################################################
class FiberSection():
	"""
	生成纤维截面
	"""
	def __init__(self, fig,ax,outNode,outEle,inNode=None,inEle=None):
		"""
		:param outNode:外部轮廓节点
		:param outEle: 外部轮廓单元（逆时针）
		:param inNode: 内部轮廓节点，每个轮廓是一个字典
		:param inEle: 内部轮廓单元
		"""
		self.outNode=outNode
		self.outEle=outEle
		self.inNode=inNode
		self.inEle=inEle
		self.fig=fig
		self.ax=ax
		self.outNewNodeDict=None  #新生成的外侧保护层混凝土线节点字典
		self.inNewNodeDict=None	  #新生成的内侧保护层混凝土线节点字典列表
	def _lineNodeList(self,nodeDict,eleDict):
		"""
		返回每个线单元两端节点的X，Y坐标列表
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
		未划分的初始截面绘制
		"""
		###外部轮廓线绘制
		lineList=self._lineNodeList(self.outNode, self.outEle)
		for each1 in lineList:
			self.ax.plot(each1[0],each1[1], "r",zorder = 0)
		if self.inNode != None:
			for eachNode,eachEle in zip(self.inNode,self.inEle):
				lineList1=self._lineNodeList(eachNode, eachEle)
				for each2 in lineList1:
					self.ax.plot(each2[0],each2[1], "r",zorder = 0)
		else:
			pass

	def _middleLineNode(self,nodeDict,d0,pos="outLine"):
		"""
		计算分界线各节点的列表
		nodeDict-节点字典 {1:(2.3,4.3)}
		d0-保护层厚度
		pos-外侧分界线（"outLinee"),内侧分界线("inLine")
		"""
		NodeKeys = list(nodeDict.keys())
		NodeKeys.append(NodeKeys[0])
		NodeKeys.append(NodeKeys[1])
		IterNode = []
		for i1 in range(len(nodeDict)):
			IterNode.append((NodeKeys[i1],NodeKeys[i1 + 1],NodeKeys[i1 + 2]))
		NodeList = []
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
			if pos=="outLine":
				c11 = c1_1 if abs(c1_1) < abs(c1_2) else c1_2
			else:
				c11 = c1_2 if abs(c1_1) < abs(c1_2) else c1_1
			c2_1 = c2 - math.sqrt(a2 ** 2 + b2 ** 2) * d0
			c2_2 = c2 + math.sqrt(a2 ** 2 + b2 ** 2) * d0
			if pos=="outLine":
				c22 = c2_1 if abs(c2_1) < abs(c2_2) else c2_2
			else:
				c22 = c2_2 if abs(c2_1) < abs(c2_2) else c2_1
			A = np.array([[a1, b1], [a2, b2]])
			B = np.array([-c11, -c22])
			newNode = list(solve(A, B))
			NodeList.append((newNode[0], newNode[1]))
		NodeList.insert(0,NodeList[-1])
		del NodeList[-1]
		return NodeList

	def coverLinePlot(self,d0):
		"""
		通过轮廓线及保护层厚度计算核心混凝土与保护层混凝土交界线
		d0--保护层混凝土厚度
		"""
		returnNodeList=self._middleLineNode(self.outNode, d0, pos="outLine")
		outNodeDict={(i1+1):returnNodeList[i1] for i1 in range(len(returnNodeList))}
		self.outNewNodeDict=outNodeDict  ##外层混凝土保护层线节点字典，与外轮廓节点一一对应
		outEleDict=self.outEle
		coverlineList = self._lineNodeList(outNodeDict, outEleDict)
		for each2 in coverlineList:
			self.ax.plot(each2[0], each2[1], "b",zorder = 0)
		return returnNodeList

	def innerLinePlot(self,d0):
		"""
		内层洞周围核心混凝土与保护层混凝土的分界线
		d0--保护层混凝土厚度
		"""
		if self.inNode != None:
			innerList=[]
			innerListDict=[]
			for eachNode,eachEle in zip(self.inNode,self.inEle):
				returnNodeList = self._middleLineNode(eachNode, d0, pos="inLine")
				innerList.append(returnNodeList)
				innerListDict.append({(j1+1):returnNodeList[j1] for j1 in range(len(returnNodeList))})
				inNodeDict = {(i1 + 1): returnNodeList[i1] for i1 in range(len(returnNodeList))}
				inEleDict = eachEle
				inlineList = self._lineNodeList(inNodeDict, inEleDict)

				for each2 in inlineList:
					self.ax.plot(each2[0], each2[1], "b",zorder = 0)
			self.inNewNodeDict=innerListDict
			return innerList

	def coreMesh(self,eleSize,outLineList,inLineList=None):
		"""
		核心混凝土的划分
		eleSize-每个三角形的边长
		"""
		n=len(inLineList)
		if inLineList==None:
			geo = dmsh.Difference(
				dmsh.Polygon(outLineList)
			)
		elif n==1:
			geo = dmsh.Difference(
				dmsh.Polygon(outLineList),
				dmsh.Polygon(inLineList[0]),
			)
		points, elements = dmsh.generate(geo, eleSize)
		self.ax.triplot(points[:, 0], points[:, 1], elements,zorder = 0)

	def _coverDivide(self,outNodeDict,inNodeDict,eleDict,size,d0):
		"""
		每个保护层混凝土的划分
		size-分割单元尺寸
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
		dcover-划分单元的大小
		d0-保护层厚度
		"""
		nodeOutDict=self.outNode
		eleOutDict=self.outEle
		nodeNewOutDict=self.outNewNodeDict# 新生成的外侧保护层混凝土线节点字典
		nodeNewInDict=self.inNewNodeDict# 新生成的内侧保护层混凝土线节点字典列表
		nodeInDict=self.inNode
		eleInDict=self.inEle
		fiberInfo,outNodeInfo,inNodeInfo=self._coverDivide(nodeOutDict,nodeNewOutDict,eleOutDict,size,d0)
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
			self.ax.plot([inNodeInfo[i1][0],outNodeInfo[i1][0]],[inNodeInfo[i1][1],outNodeInfo[i1][1]],"r",zorder = 0)
		for i2 in range(len(outNodeInfo)-1):
			self.ax.plot([inNodeInfo[i2][0], inNodeInfo[i2+1][0]], [inNodeInfo[i2][1], inNodeInfo[i2+1][1]], "r",zorder = 0)
		for i3 in range(len(outNodeInfo)-1):
			self.ax.plot([outNodeInfo[i3][0], outNodeInfo[i3+1][0]], [outNodeInfo[i3][1], outNodeInfo[i3+1][1]], "r",zorder = 0)
		##内部保护层混凝土的划分
		if self.inNode != None:
			nInhole=len(self.inNode)
			inxList = []
			inyList = []
			inareaList = []
			for i4 in range(nInhole):
				Innerfiber, innerOut, innerIn = self._coverDivide(nodeInDict[i4],nodeNewInDict[i4],eleInDict[i4], size,d0)
				innerOut.append(innerOut[0])
				innerIn.append(innerIn[0])
				for each2 in Innerfiber:
					inxList.append(each2[0])
					inyList.append(each2[1])
					inareaList.append(each2[2])
				for i5 in range(len(innerOut)-1):
					self.ax.plot([innerOut[i5][0], innerIn[i5][0]], [innerOut[i5][1], innerIn[i5][1]], "r",zorder = 0)
				for i6 in range(len(innerOut)-1):
					self.ax.plot([innerIn[i6][0], innerIn[i6 + 1][0]], [innerIn[i6][1], innerIn[i6 + 1][1]],"r",zorder = 0)
				for i7 in range(len(innerIn)-1):
					self.ax.plot([innerOut[i7][0], innerOut[i7 + 1][0]],[innerOut[i7][1],innerOut[i7 + 1][1]], "r",zorder = 0)
			# self.ax.scatter(inxList,inyList,s=2,c="r")

	def _barDivide(self,barD,barDist,nodeDict,lineEleDict):
		"""
		钢筋纤维的划分
		barD-单个纵筋直径
		barDist-纵筋间距
		nodeDict-钢筋线节点字典
		lineEleDict-钢筋线单元字典
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



	def barMesh(self,outBarD,outBarDist,inBarD,inBarDist):
		"""
		内外层钢筋的划分
		outBarD-外侧钢筋直径
		outBarDist-外侧钢筋间距
		inBarD-内侧钢筋直径
		inBarDist-内侧钢筋间距
		"""
		outBarLineDict=self.outNewNodeDict  # 新生成的外侧保护层混凝土线节点字典
		outBarListEle=self.outEle
		inBarLineDict=self.inNewNodeDict # 新生成的内侧保护层混凝土线节点字典列表
		inBarLineEle=self.inEle
		#外侧钢筋的划分
		outBarFiber,outXList,outYList=self._barDivide(outBarD,outBarDist,outBarLineDict,outBarListEle)
		self.ax.scatter(outXList,outYList,s=10,c="k",zorder = 2)
		if self.inNode != None:
			nEle=len(inBarLineEle)
			for i1 in range(nEle):
				inBarFiber, inXList, inYList = self._barDivide(inBarD, inBarDist, inBarLineDict[i1], inBarLineEle[i1])
				self.ax.scatter(inXList, inYList, s=10, c="k", zorder=2)

if __name__=="__main__":
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
	outSideNode={1:(3.5,3),2:(1.5,5),3:(-1.5,5),4:(-3.5,3),5:(-3.5,-3),6:(-1.5,-5),7:(1.5,-5),8:(3.5,-3)}
	outSideEle = {1: (1, 2), 2: (2, 3), 3: (3, 4), 4: (4, 5), 5: (5, 6), 6: (6, 7), 7: (7, 8), 8: (8, 1)}
	inSideNode=[{1:(1.9,2.4),2:(1.1,3.2),3:(-1.1,3.2),4:(-1.9,2.4),5:(-1.9,-2.4),6:(-1.1,-3.2),7:(1.1,-3.2),8:(1.9,-2.4)}]
	inSideEle = [{1: (1, 2), 2: (2, 3), 3: (3, 4), 4: (4, 5), 5: (5, 6), 6: (6, 7), 7: (7, 8), 8: (8, 1)}]
	######################################################################################
	##########################---下塔柱截面---#############################################

	#########---多边形截面内有两个洞--#####################################################


	######################################################################################
	fig,ax = plt.subplots()
	d0=0.2  #保护层厚度
	eleSize=0.3  #核心纤维的大小
	coverSize=0.3 #保护层纤维大小
	outBarDist=0.3
	outBarD=0.032
	inBarDist=0.3
	inBarD=0.032
	sectInstance=FiberSection(fig,ax,outSideNode,outSideEle,inSideNode,inSideEle)
	sectInstance.sectPlot()
	outLineList=sectInstance.coverLinePlot(d0)
	inLineList=sectInstance.innerLinePlot(d0)
	sectInstance.coreMesh(eleSize,outLineList,inLineList)
	# print(len(sectInstance.inNewNodeDict))
	# print(sectInstance.outNewNodeDict)
	sectInstance.coverMesh(coverSize,d0)
	sectInstance.barMesh(outBarD,outBarDist,inBarD,inBarDist)

	plt.show()