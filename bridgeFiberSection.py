# -*- coding:utf-8 -*-
# @Time     : 2020/6/14 19:42
# @Author   : Penghui Zhang
# @Email    : penghui@tongji.edu.cn
# @File     : MC.py
# @Software : PyCharm

from fiberGenerate import *
import shutil
import os
import numpy as np

########################################---2.0m桩基截面---################################
fig =	plt.figure(figsize=(5, 5))
ax = fig.add_subplot(111)
outbarD =	0.032  #	纵向钢筋直径
outbarDist = 0.1217367153	 # 纵向钢筋间距
coverThick = 0.06	# 保护层混凝土厚度
coreEleSize =	0.1	 # 核心纤维的大小
coverEleSize = 0.15  # 保护层纤维大小
outDiameter =	2	# 截面外圆直径
circleInstance = CircleSection(ax, coverThick, outDiameter)
circleInstance.sectPlot()
coreFiber=circleInstance.coreMesh(coreEleSize)
coverFiber = circleInstance.coverMesh(coverEleSize)
barFiber = circleInstance.barMesh(outbarD, outbarDist)
ax.tick_params(direction='in', labelsize=6)
plt.ylabel('transverse (m)',fontdict={'family': 'Times New Roman', 'size': 12})
plt.xlabel('longitudinal (m)',fontdict={'family': 'Times New Roman', 'size': 12})
plt.title('Pile2.0m Section')
if not os.path.exists('SectionFig'):
	os.makedirs('SectionFig')
plt.savefig("SectionFig/pile2.0m.eps", dpi=600, bbox_inches="tight")
plt.savefig("SectionFig/pile2.0m.png", dpi=600, bbox_inches="tight")
if not os.path.exists('Pile2.0m'):
	os.makedirs('Pile2.0m')
np.savetxt("Pile2.0m/" + "coreDivide.txt", coreFiber, fmt="%0.6f %0.6f %0.6f")
np.savetxt("Pile2.0m/" + "coverDivide.txt", coverFiber, fmt="%0.6f %0.6f %0.6f")
np.savetxt("Pile2.0m/" + "barDivide.txt", barFiber, fmt="%0.6f %0.6f %0.6f")
plt.show()

fig1 = plt.figure(figsize=(5,	5))
ax1 = fig1.add_subplot(111)
coreFiberXList = [each1[0] for each1 in coreFiber]
coreFiberYList = [each1[1] for each1 in coreFiber]
coreFiberAreaList	= [each1[2]	for	each1 in coreFiber]
coverFiberXList =	[each1[0] for each1	in coverFiber]
coverFiberYList =	[each1[1] for each1	in coverFiber]
coverFiberAreaList = [each1[2] for each1 in coverFiber]
barFiberXList	= [each1[0]	for	each1 in barFiber]
barFiberYList	= [each1[1]	for	each1 in barFiber]
barFiberAreaList = [each1[2] for each1 in	barFiber]
ax1.tick_params(direction='in', labelsize=6)
ax1.scatter(coreFiberXList, coreFiberYList, s=5, c="b", zorder=3)
ax1.scatter(coverFiberXList, coverFiberYList,	s=5, c="r",	zorder=3)
ax1.scatter(barFiberXList, barFiberYList,	s=5, c="k",	zorder=3)
ax.tick_params(direction='in', labelsize=6)
plt.ylabel('transverse (m)',fontdict={'family': 'Times New Roman', 'size': 12})
plt.xlabel('longitudinal (m)',fontdict={'family': 'Times New Roman', 'size': 12})
plt.title('Pile2.0m Section')
if not os.path.exists('SectionFig'):
	os.makedirs('SectionFig')
plt.savefig("SectionFig/pile2.0mFiber.eps", dpi=600, bbox_inches="tight")
plt.savefig("SectionFig/pile2.0mFiber.png", dpi=600, bbox_inches="tight")
plt.show()

########################################---1.5m桩基截面---################################
fig =	plt.figure(figsize=(5, 5))
ax = fig.add_subplot(111)
outbarD =	0.028  #	纵向钢筋直径
outbarDist = 0.1525916432	 # 纵向钢筋间距
coverThick = 0.06	# 保护层混凝土厚度
coreEleSize =	0.1	 # 核心纤维的大小
coverEleSize = 0.1  # 保护层纤维大小
outDiameter = 1.5	# 截面外圆直径
circleInstance = CircleSection(ax, coverThick, outDiameter)
circleInstance.sectPlot()
coreFiber=circleInstance.coreMesh(coreEleSize)
coverFiber = circleInstance.coverMesh(coverEleSize)
barFiber = circleInstance.barMesh(outbarD, outbarDist)
ax.tick_params(direction='in', labelsize=6)
plt.ylabel('transverse (m)',fontdict={'family': 'Times New Roman', 'size': 12})
plt.xlabel('longitudinal (m)',fontdict={'family': 'Times New Roman', 'size': 12})
plt.title('Pile1.5m Section')
if not os.path.exists('SectionFig'):
	os.makedirs('SectionFig')
plt.savefig("SectionFig/pile1.5m.eps", dpi=600, bbox_inches="tight")
plt.savefig("SectionFig/pile1.5m.png", dpi=600, bbox_inches="tight")
if not os.path.exists('Pile1.5m'):
	os.makedirs('Pile1.5m')
np.savetxt("Pile1.5m/" + "coreDivide.txt", coreFiber, fmt="%0.6f %0.6f %0.6f")
np.savetxt("Pile1.5m/" + "coverDivide.txt", coverFiber, fmt="%0.6f %0.6f %0.6f")
np.savetxt("Pile1.5m/" + "barDivide.txt", barFiber, fmt="%0.6f %0.6f %0.6f")
plt.show()

fig1 = plt.figure(figsize=(5,	5))
ax1 = fig1.add_subplot(111)
coreFiberXList = [each1[0] for each1 in coreFiber]
coreFiberYList = [each1[1] for each1 in coreFiber]
coreFiberAreaList	= [each1[2]	for	each1 in coreFiber]
coverFiberXList =	[each1[0] for each1	in coverFiber]
coverFiberYList =	[each1[1] for each1	in coverFiber]
coverFiberAreaList = [each1[2] for each1 in coverFiber]
barFiberXList	= [each1[0]	for	each1 in barFiber]
barFiberYList	= [each1[1]	for	each1 in barFiber]
barFiberAreaList = [each1[2] for each1 in	barFiber]
ax1.tick_params(direction='in', labelsize=6)
ax1.scatter(coreFiberXList, coreFiberYList, s=5, c="b", zorder=3)
ax1.scatter(coverFiberXList, coverFiberYList,	s=5, c="r",	zorder=3)
ax1.scatter(barFiberXList, barFiberYList,	s=5, c="k",	zorder=3)
ax.tick_params(direction='in', labelsize=6)
plt.ylabel('transverse (m)',fontdict={'family': 'Times New Roman', 'size': 12})
plt.xlabel('longitudinal (m)',fontdict={'family': 'Times New Roman', 'size': 12})
plt.title('Pile1.5m Section')
if not os.path.exists('SectionFig'):
	os.makedirs('SectionFig')
plt.savefig("SectionFig/pile1.5mFiber.eps", dpi=600, bbox_inches="tight")
plt.savefig("SectionFig/pile1.5mFiber.png", dpi=600, bbox_inches="tight")
plt.show()

########################################---0.8m桩基截面---################################
fig =	plt.figure(figsize=(5, 5))
ax = fig.add_subplot(111)
outbarD =	0.02282542442  #	纵向钢筋直径
outbarDist = 0.1313185729	 # 纵向钢筋间距
coverThick = 0.06	# 保护层混凝土厚度
coreEleSize =	0.05	 # 核心纤维的大小
coverEleSize = 0.08  # 保护层纤维大小
outDiameter = 0.8	# 截面外圆直径
circleInstance = CircleSection(ax, coverThick, outDiameter)
circleInstance.sectPlot()
coreFiber=circleInstance.coreMesh(coreEleSize)
coverFiber = circleInstance.coverMesh(coverEleSize)
barFiber = circleInstance.barMesh(outbarD, outbarDist)
ax.tick_params(direction='in', labelsize=6)
plt.ylabel('transverse (m)',fontdict={'family': 'Times New Roman', 'size': 12})
plt.xlabel('longitudinal (m)',fontdict={'family': 'Times New Roman', 'size': 12})
plt.title('Pile0.8m Section')
if not os.path.exists('SectionFig'):
	os.makedirs('SectionFig')
plt.savefig("SectionFig/pile0.8m.eps", dpi=600, bbox_inches="tight")
plt.savefig("SectionFig/pile0.8m.png", dpi=600, bbox_inches="tight")
if not os.path.exists('Pile0.8m'):
	os.makedirs('Pile0.8m')
np.savetxt("Pile0.8m/" + "coreDivide.txt", coreFiber, fmt="%0.6f %0.6f %0.6f")
np.savetxt("Pile0.8m/" + "coverDivide.txt", coverFiber, fmt="%0.6f %0.6f %0.6f")
np.savetxt("Pile0.8m/" + "barDivide.txt", barFiber, fmt="%0.6f %0.6f %0.6f")
plt.show()

fig1 = plt.figure(figsize=(5,	5))
ax1 = fig1.add_subplot(111)
coreFiberXList = [each1[0] for each1 in coreFiber]
coreFiberYList = [each1[1] for each1 in coreFiber]
coreFiberAreaList	= [each1[2]	for	each1 in coreFiber]
coverFiberXList =	[each1[0] for each1	in coverFiber]
coverFiberYList =	[each1[1] for each1	in coverFiber]
coverFiberAreaList = [each1[2] for each1 in coverFiber]
barFiberXList	= [each1[0]	for	each1 in barFiber]
barFiberYList	= [each1[1]	for	each1 in barFiber]
barFiberAreaList = [each1[2] for each1 in	barFiber]
ax1.tick_params(direction='in', labelsize=6)
ax1.scatter(coreFiberXList, coreFiberYList, s=5, c="b", zorder=3)
ax1.scatter(coverFiberXList, coverFiberYList,	s=5, c="r",	zorder=3)
ax1.scatter(barFiberXList, barFiberYList,	s=5, c="k",	zorder=3)
ax.tick_params(direction='in', labelsize=6)
plt.ylabel('transverse (m)',fontdict={'family': 'Times New Roman', 'size': 12})
plt.xlabel('longitudinal (m)',fontdict={'family': 'Times New Roman', 'size': 12})
plt.title('Pile0.8m Section')
if not os.path.exists('SectionFig'):
	os.makedirs('SectionFig')
plt.savefig("SectionFig/pile0.8mFiber.eps", dpi=600, bbox_inches="tight")
plt.savefig("SectionFig/pile0.8mFiber.png", dpi=600, bbox_inches="tight")
plt.show()

########################################---引桥桥墩截面---################################
outSideNode = {1: (0.8,1.6), 2: (-0.8,1.6), 3: (-0.8,-1.6), 4: (0.8,-1.6)}
outSideEle = {1: (1, 2), 2: (2, 3), 3: (3, 4), 4: (4, 1)}
outSideX=max([outSideNode[i1+1][0] for i1 in range(len(outSideNode))])
outSideY=max([outSideNode[i1+1][1] for i1 in range(len(outSideNode))])
fig = plt.figure(figsize=(outSideX*2,outSideY*2))
ax = fig.add_subplot(111)
d0 = 0.11  # 保护层厚度
eleSize = 0.2  # 核心纤维的大小
coverSize = 0.3  # 保护层纤维大小
outBarDist = 0.1846153846 #外层钢筋间距
outBarD = 0.04 #外层钢筋直径
sectInstance = PolygonSection(ax, outSideNode, outSideEle)
sectInstance.sectPlot()
outLineList = sectInstance.coverLinePlot(d0)
coreFiber=sectInstance.coreMesh(eleSize, outLineList)
coverFiber=sectInstance.coverMesh(coverSize, d0)
barFiber=sectInstance.barMesh(d0, outBarD, outBarDist)
ax.tick_params(direction='in', labelsize=8)
plt.ylabel('transverse (m)',fontdict={'family': 'Times New Roman', 'size': 12})
plt.xlabel('longitudinal (m)',fontdict={'family': 'Times New Roman', 'size': 12})
plt.title('Approach Pier Section')
if not os.path.exists('SectionFig'):
	os.makedirs('SectionFig')
plt.savefig("SectionFig/ApprochPier.eps", dpi=600, bbox_inches="tight")
plt.savefig("SectionFig/ApprochPier.png", dpi=600, bbox_inches="tight")
if not os.path.exists('ApprochPier'):
	os.makedirs('ApprochPier')
np.savetxt("ApprochPier"+"/coreDivide.txt",coreFiber,fmt="%0.6f %0.6f %0.6f")
np.savetxt("ApprochPier"+"/coverDivide.txt",coverFiber,fmt="%0.6f %0.6f %0.6f")
np.savetxt("ApprochPier"+"/barDivide.txt",barFiber,fmt="%0.6f %0.6f %0.6f")
plt.show()

fig1 = plt.figure(figsize=(outSideX*2,outSideY*2))
ax1 = fig1.add_subplot(111)
coreFiberXList = [each1[0] for each1 in coreFiber]
coreFiberYList = [each1[1] for each1 in coreFiber]
coreFiberAreaList	= [each1[2]	for	each1 in coreFiber]
coverFiberXList =	[each1[0] for each1	in coverFiber]
coverFiberYList =	[each1[1] for each1	in coverFiber]
coverFiberAreaList = [each1[2] for each1 in coverFiber]
barFiberXList	= [each1[0]	for	each1 in barFiber]
barFiberYList	= [each1[1]	for	each1 in barFiber]
barFiberAreaList = [each1[2] for each1 in	barFiber]
ax1.tick_params(direction='in', labelsize=6)
ax1.scatter(coreFiberXList, coreFiberYList, s=5, c="b", zorder=3)
ax1.scatter(coverFiberXList, coverFiberYList,	s=5, c="r",	zorder=3)
ax1.scatter(barFiberXList, barFiberYList,	s=5, c="k",	zorder=3)
ax.tick_params(direction='in', labelsize=6)
plt.ylabel('transverse (m)',fontdict={'family': 'Times New Roman', 'size': 12})
plt.xlabel('longitudinal (m)',fontdict={'family': 'Times New Roman', 'size': 12})
plt.title('Approach Pier Section')
if not os.path.exists('SectionFig'):
	os.makedirs('SectionFig')
plt.savefig("SectionFig/ApprochPierFiber.eps", dpi=600, bbox_inches="tight")
plt.savefig("SectionFig/ApprochPierFiber.png", dpi=600, bbox_inches="tight")
plt.show()

####################################################################################


########################################---边墩截面---################################
outSideNode = {1: (1.25,2.25), 2: (-1.25,2.25), 3: (-1.25,-2.25), 4: (1.25,-2.25)}
outSideEle = {1: (1, 2), 2: (2, 3), 3: (3, 4), 4: (4, 1)}
outSideX=max([outSideNode[i1+1][0] for i1 in range(len(outSideNode))])
outSideY=max([outSideNode[i1+1][1] for i1 in range(len(outSideNode))])
fig = plt.figure(figsize=(outSideX*2,outSideY*2))
ax = fig.add_subplot(111)
d0 = 0.04  # 保护层厚度
eleSize = 0.2  # 核心纤维的大小
coverSize = 0.3  # 保护层纤维大小

#外层钢筋分布信息1
outBarD1 = 0.032 #外层钢筋直径
outBarDist1 = 0.13#外层钢筋间距
outBarNodeDict1 = {1: (1.2, 2.1), 2: (-1.2, 2.1), 3: (-1.2, -2.1), 4: (1.2, -2.1)}
outBarEleDict1 = {1: (1, 2), 2: (2, 3), 3: (3, 4), 4: (4, 1)}
#外层钢筋分布信息2
outBarD2 = 0.032 #外层钢筋直径
outBarDist2 = 0.13#外层钢筋间距
outBarNodeDict2 = {1: (1.1, 2.2), 2: (-1.23, 2.2), 3: (1.1, -2.2), 4: (-1.23, -2.2)}
outBarEleDict2 = {1: (1, 2), 2: (3, 4)}

sectInstance = PolygonSection(ax, outSideNode, outSideEle)
sectInstance.sectPlot()
outLineList = sectInstance.coverLinePlot(d0)
coreFiber=sectInstance.coreMesh(eleSize, outLineList)
coverFiber=sectInstance.coverMesh(coverSize, d0)
barFiber=sectInstance.multiBarMesh(d0,outBarDist1,outBarD1,outBarNodeDict1,outBarEleDict1,outBarDist2,outBarD2,outBarNodeDict2,outBarEleDict2)

ax.tick_params(direction='in', labelsize=8)
plt.ylabel('transverse (m)',fontdict={'family': 'Times New Roman', 'size': 12})
plt.xlabel('longitudinal (m)',fontdict={'family': 'Times New Roman', 'size': 12})
plt.title('Side Pier Section')
if not os.path.exists('SectionFig'):
	os.makedirs('SectionFig')
plt.savefig("SectionFig/SidePier.eps", dpi=600, bbox_inches="tight")
plt.savefig("SectionFig/SidePier.png", dpi=600, bbox_inches="tight")
if not os.path.exists('SidePier'):
	os.makedirs('SidePier')
np.savetxt("SidePier"+"/coreDivide.txt",coreFiber,fmt="%0.6f %0.6f %0.6f")
np.savetxt("SidePier"+"/coverDivide.txt",coverFiber,fmt="%0.6f %0.6f %0.6f")
np.savetxt("SidePier"+"/barDivide.txt",barFiber,fmt="%0.6f %0.6f %0.6f")
plt.show()

fig1 = plt.figure(figsize=(outSideX*2,outSideY*2))
ax1 = fig1.add_subplot(111)
coreFiberXList = [each1[0] for each1 in coreFiber]
coreFiberYList = [each1[1] for each1 in coreFiber]
coreFiberAreaList	= [each1[2]	for	each1 in coreFiber]
coverFiberXList =	[each1[0] for each1	in coverFiber]
coverFiberYList =	[each1[1] for each1	in coverFiber]
coverFiberAreaList = [each1[2] for each1 in coverFiber]
barFiberXList	= [each1[0]	for	each1 in barFiber]
barFiberYList	= [each1[1]	for	each1 in barFiber]
barFiberAreaList = [each1[2] for each1 in	barFiber]
ax1.tick_params(direction='in', labelsize=6)
ax1.scatter(coreFiberXList, coreFiberYList, s=5, c="b", zorder=3)
ax1.scatter(coverFiberXList, coverFiberYList,	s=5, c="r",	zorder=3)
ax1.scatter(barFiberXList, barFiberYList,	s=5, c="k",	zorder=3)
ax.tick_params(direction='in', labelsize=6)
plt.ylabel('transverse (m)',fontdict={'family': 'Times New Roman', 'size': 12})
plt.xlabel('longitudinal (m)',fontdict={'family': 'Times New Roman', 'size': 12})
plt.title('Side Pier Section')
if not os.path.exists('SectionFig'):
	os.makedirs('SectionFig')
plt.savefig("SectionFig/SidePierFiber.eps", dpi=600, bbox_inches="tight")
plt.savefig("SectionFig/SidePierFiber.png", dpi=600, bbox_inches="tight")
plt.show()
####################################################################################


########################################---桥塔1截面---################################
outSideNode = {1: (2.559,2.1), 2: (-2.559, 2.1), 3: (-2.559, 1.6), 4: (-3.059,1.6), 5: (-3.059,-1.6), 6: (-2.559,-1.6),\
               7: (-2.559,-2.1), 8: (2.559,-2.1), 9: (2.559,-1.6), 10: (3.059,-1.6), 11: (3.059,1.6), 12: (2.559,1.6)}
outSideEle = {1: (1, 2), 2: (2, 3), 3: (3, 4), 4: (4, 5), 5: (5, 6), 6: (6, 7), 7: (7, 8), 8: (8, 9), 9: (9, 10),\
              10: (10, 11), 11: (11, 12), 12: (12, 1)}
inSideNode = [{1: (1.809, 1.35), 2: (-1.809, 1.35), 3: (-2.309, 0.85), 4: (-2.309, -0.85), 5: (-1.809, -1.35),\
               6: (1.809, -1.35), 7: (2.309, -0.85), 8: (2.309, 0.85)}]
inSideEle = [{1: (1, 2), 2: (2, 3), 3: (3, 4), 4: (4, 5), 5: (5, 6), 6: (6, 7), 7: (7, 8), 8: (8, 1)}]
outSideX=max([outSideNode[i1+1][0] for i1 in range(len(outSideNode))])
outSideY=max([outSideNode[i1+1][1] for i1 in range(len(outSideNode))])
fig = plt.figure(figsize=(outSideX,outSideY))
ax = fig.add_subplot(111)
d0 = 0.06  # 保护层厚度
eleSize = 0.2  # 核心纤维的大小
coverSize = 0.2  # 保护层纤维大小
inBarDist = 0.14 #内层钢筋间距
inBarD = 0.025 #内层钢筋直径

#外层钢筋分布信息1
outBarD1 = 0.036 #外层钢筋直径
outBarDist1 = 0.14#外层钢筋间距
outBarNodeDict1 = {1: (2.975, 1.516), 2: (2.475, 1.516), 3: (2.475, 2.016), 4: (-2.475, 2.016), 5: (-2.475, 1.516),
                   6: (-2.975, 1.516),7: (-2.975, -1.516), 8: (-2.475, -1.516), 9: (-2.475, -2.016), 10: (2.475, -2.016),
                   11: (2.475, -1.516), 12: (2.975, -1.516)}
outBarEleDict1 = {1: (1, 2), 2: (2, 3), 3: (3, 4), 4: (4, 5), 5: (6, 5), 6: (5, 2), 7: (7, 8), 8: (8, 9), 9: (9, 10),
                  10: (10, 11), 11: (12, 11), 12: (11, 8)}
#外层钢筋分布信息2
outBarD2 = 0.04 #外层钢筋直径
outBarDist2 = 0.14#外层钢筋间距
outBarNodeDict2 = {1: (2.975, 1.33), 2: (2.975, -1.47), 3: (2.475, 1.33), 4: (2.475, -1.47), 5: (-2.475, 1.33),
                   6: (-2.475, -1.47),7: (-2.975, 1.33), 8: (-2.975, -1.47)}
outBarEleDict2 = {1: (1, 2), 2: (3, 4), 3: (5, 6), 4: (7, 8)}

sectInstance = PolygonSection(ax, outSideNode, outSideEle, inSideNode, inSideEle)
sectInstance.sectPlot()
outLineList = sectInstance.coverLinePlot(d0)
inLineList = sectInstance.innerLinePlot(d0)
coreFiber=sectInstance.coreMesh(eleSize, outLineList, inLineList)
coverFiber=sectInstance.coverMesh(coverSize, d0)
barFiber=sectInstance.multiBarMesh(d0,outBarDist1,outBarD1,outBarNodeDict1,outBarEleDict1,outBarDist2,outBarD2,outBarNodeDict2,outBarEleDict2,inBarD,inBarDist)
ax.tick_params(direction='in', labelsize=6)
plt.ylabel('transverse (m)',fontdict={'family': 'Times New Roman', 'size': 12})
plt.xlabel('longitudinal (m)',fontdict={'family': 'Times New Roman', 'size': 12})
plt.title('Tower-1 Section')
if not os.path.exists('SectionFig'):
	os.makedirs('SectionFig')
plt.savefig("SectionFig/Tower-1.eps", dpi=600, bbox_inches="tight")
plt.savefig("SectionFig/Tower-1.png", dpi=600, bbox_inches="tight")
if not os.path.exists('Tower-1'):
	os.makedirs('Tower-1')
np.savetxt("Tower-1"+"/coreDivide.txt",coreFiber,fmt="%0.6f %0.6f %0.6f")
np.savetxt("Tower-1"+"/coverDivide.txt",coverFiber,fmt="%0.6f %0.6f %0.6f")
np.savetxt("Tower-1"+"/barDivide.txt",barFiber,fmt="%0.6f %0.6f %0.6f")
plt.show()


fig1 = plt.figure(figsize=(outSideX,outSideY))
ax1 = fig1.add_subplot(111)
coreFiberXList = [each1[0] for each1 in coreFiber]
coreFiberYList = [each1[1] for each1 in coreFiber]
coreFiberAreaList	= [each1[2]	for	each1 in coreFiber]
coverFiberXList =	[each1[0] for each1	in coverFiber]
coverFiberYList =	[each1[1] for each1	in coverFiber]
coverFiberAreaList = [each1[2] for each1 in coverFiber]
barFiberXList	= [each1[0]	for	each1 in barFiber]
barFiberYList	= [each1[1]	for	each1 in barFiber]
barFiberAreaList = [each1[2] for each1 in	barFiber]
ax1.tick_params(direction='in', labelsize=6)
ax1.scatter(coreFiberXList, coreFiberYList, s=3, c="b", zorder=3)
ax1.scatter(coverFiberXList, coverFiberYList,	s=3, c="r",	zorder=3)
ax1.scatter(barFiberXList, barFiberYList,	s=3, c="k",	zorder=3)
ax.tick_params(direction='in', labelsize=6)
plt.ylabel('transverse (m)',fontdict={'family': 'Times New Roman', 'size': 12})
plt.xlabel('longitudinal (m)',fontdict={'family': 'Times New Roman', 'size': 12})
plt.title('Tower-1 Section')
if not os.path.exists('SectionFig'):
	os.makedirs('SectionFig')
plt.savefig("SectionFig/Tower-1Fiber.eps", dpi=600, bbox_inches="tight")
plt.savefig("SectionFig/Tower-1Fiber.png", dpi=600, bbox_inches="tight")
plt.show()

####################################################################################


########################################---桥塔2截面---################################
outSideNode = {1: (3.096,2.1), 2: (-3.096, 2.1), 3: (-3.096, 1.6), 4: (-3.596,1.6), 5: (-3.596,-1.6), 6: (-3.096,-1.6),\
               7: (-3.096,-2.1), 8: (3.096,-2.1), 9: (3.096,-1.6), 10: (3.596,-1.6), 11: (3.596,1.6), 12: (3.096,1.6)}
outSideEle = {1: (1, 2), 2: (2, 3), 3: (3, 4), 4: (4, 5), 5: (5, 6), 6: (6, 7), 7: (7, 8), 8: (8, 9), 9: (9, 10),\
              10: (10, 11), 11: (11, 12), 12: (12, 1)}
inSideNode = [{1: (2.096, 1.1), 2: (-2.096, 1.1), 3: (-2.596, 0.6), 4: (-2.596, -0.6), 5: (-2.096, -1.1),\
               6: (2.096, -1.1), 7: (2.596, -0.6), 8: (2.596, 0.6)}]
inSideEle = [{1: (1, 2), 2: (2, 3), 3: (3, 4), 4: (4, 5), 5: (5, 6), 6: (6, 7), 7: (7, 8), 8: (8, 1)}]
outSideX=max([outSideNode[i1+1][0] for i1 in range(len(outSideNode))])
outSideY=max([outSideNode[i1+1][1] for i1 in range(len(outSideNode))])
fig = plt.figure(figsize=(outSideX,outSideY))
ax = fig.add_subplot(111)
d0 = 0.06  # 保护层厚度
eleSize = 0.25  # 核心纤维的大小
coverSize = 0.2  # 保护层纤维大小
inBarDist = 0.14 #内层钢筋间距
inBarD = 0.025 #内层钢筋直径

#外层钢筋分布信息1
outBarD1 = 0.036 #外层钢筋直径
outBarDist1 = 0.14#外层钢筋间距
outBarNodeDict1 = {1: (3.512, 1.516), 2: (3.012, 1.516), 3: (3.012, 2.016), 4: (-3.012, 2.016), 5: (-3.012, 1.516),
                   6: (-3.512, 1.516),7: (-3.512, -1.516), 8: (-3.012, -1.516), 9: (-3.012, -2.016), 10: (3.012, -2.016),
                   11: (3.012, -1.516), 12: (3.512, -1.516)}
outBarEleDict1 = {1: (1, 2), 2: (2, 3), 3: (3, 4), 4: (4, 5), 5: (6, 5), 6: (5, 2), 7: (7, 8), 8: (8, 9), 9: (9, 10),
                  10: (10, 11), 11: (12, 11), 12: (11, 8)}
#外层钢筋分布信息2
outBarD2 = 0.04 #外层钢筋直径
outBarDist2 = 0.14#外层钢筋间距
outBarNodeDict2 = {1: (3.512, 1.33), 2: (3.512, -1.47), 3: (3.262, 1.33), 4: (3.262, -1.47), 5: (3.012, 1.33),
                   6: (3.012, -1.47),7: (-3.012, 1.33), 8: (-3.012, -1.47), 9: (-3.262, 1.33), 10: (-3.262, -1.47),
                   11: (-3.512, 1.33),12: (-3.512, -1.47)}
outBarEleDict2 = {1: (1, 2), 2: (3, 4), 3: (5, 6), 4: (7, 8), 5: (9, 10), 6: (11, 12)}

sectInstance = PolygonSection(ax, outSideNode, outSideEle, inSideNode, inSideEle)
sectInstance.sectPlot()
outLineList = sectInstance.coverLinePlot(d0)
inLineList = sectInstance.innerLinePlot(d0)
coreFiber=sectInstance.coreMesh(eleSize, outLineList, inLineList)
coverFiber=sectInstance.coverMesh(coverSize, d0)
barFiber=sectInstance.multiBarMesh(d0,outBarDist1,outBarD1,outBarNodeDict1,outBarEleDict1,outBarDist2,outBarD2,outBarNodeDict2,outBarEleDict2,inBarD,inBarDist)
ax.tick_params(direction='in', labelsize=6)
plt.ylabel('transverse (m)',fontdict={'family': 'Times New Roman', 'size': 12})
plt.xlabel('longitudinal (m)',fontdict={'family': 'Times New Roman', 'size': 12})
plt.title('Tower-2 Section')
if not os.path.exists('SectionFig'):
	os.makedirs('SectionFig')
plt.savefig("SectionFig/Tower-2.eps", dpi=600, bbox_inches="tight")
plt.savefig("SectionFig/Tower-2.png", dpi=600, bbox_inches="tight")
if not os.path.exists('Tower-2'):
	os.makedirs('Tower-2')
np.savetxt("Tower-2"+"/coreDivide.txt",coreFiber,fmt="%0.6f %0.6f %0.6f")
np.savetxt("Tower-2"+"/coverDivide.txt",coverFiber,fmt="%0.6f %0.6f %0.6f")
np.savetxt("Tower-2"+"/barDivide.txt",barFiber,fmt="%0.6f %0.6f %0.6f")
plt.show()

fig1 = plt.figure(figsize=(outSideX,outSideY))
ax1 = fig1.add_subplot(111)
coreFiberXList = [each1[0] for each1 in coreFiber]
coreFiberYList = [each1[1] for each1 in coreFiber]
coreFiberAreaList	= [each1[2]	for	each1 in coreFiber]
coverFiberXList =	[each1[0] for each1	in coverFiber]
coverFiberYList =	[each1[1] for each1	in coverFiber]
coverFiberAreaList = [each1[2] for each1 in coverFiber]
barFiberXList	= [each1[0]	for	each1 in barFiber]
barFiberYList	= [each1[1]	for	each1 in barFiber]
barFiberAreaList = [each1[2] for each1 in	barFiber]
ax1.tick_params(direction='in', labelsize=6)
ax1.scatter(coreFiberXList, coreFiberYList, s=3, c="b", zorder=3)
ax1.scatter(coverFiberXList, coverFiberYList,	s=3, c="r",	zorder=3)
ax1.scatter(barFiberXList, barFiberYList,	s=3, c="k",	zorder=3)
ax.tick_params(direction='in', labelsize=6)
plt.ylabel('transverse (m)',fontdict={'family': 'Times New Roman', 'size': 12})
plt.xlabel('longitudinal (m)',fontdict={'family': 'Times New Roman', 'size': 12})
plt.title('Tower-2 Section')
if not os.path.exists('SectionFig'):
	os.makedirs('SectionFig')
plt.savefig("SectionFig/Tower-2Fiber.eps", dpi=600, bbox_inches="tight")
plt.savefig("SectionFig/Tower-2Fiber.png", dpi=600, bbox_inches="tight")
plt.show()
####################################################################################

########################################---桥塔3截面---################################
outSideNode = {1: (3.271,2.128), 2: (-3.271,2.128), 3: (-3.271,1.628), 4: (-3.771,1.628), 5: (-3.771,-1.628), 6: (-3.271,-1.628),\
               7: (-3.271,-2.128), 8: (3.271,-2.128), 9: (3.271,-1.628), 10: (3.771,-1.628), 11: (3.771,1.628), 12: (3.271,1.628)}
outSideEle = {1: (1, 2), 2: (2, 3), 3: (3, 4), 4: (4, 5), 5: (5, 6), 6: (6, 7), 7: (7, 8), 8: (8, 9), 9: (9, 10),\
              10: (10, 11), 11: (11, 12), 12: (12, 1)}
inSideNode = [{1: (2.021, 0.878), 2: (-2.021, 0.878), 3: (-2.521, 0.378), 4: (-2.521, -0.378), 5: (-2.021, -0.878),\
               6: (2.021, -0.878), 7: (2.521, -0.378), 8: (2.521, 0.378)}]
inSideEle = [{1: (1, 2), 2: (2, 3), 3: (3, 4), 4: (4, 5), 5: (5, 6), 6: (6, 7), 7: (7, 8), 8: (8, 1)}]
outSideX=max([outSideNode[i1+1][0] for i1 in range(len(outSideNode))])
outSideY=max([outSideNode[i1+1][1] for i1 in range(len(outSideNode))])
fig = plt.figure(figsize=(outSideX,outSideY))
ax = fig.add_subplot(111)
d0 = 0.06  # 保护层厚度
eleSize = 0.3  # 核心纤维的大小
coverSize = 0.2  # 保护层纤维大小
inBarDist = 0.14 #内层钢筋间距
inBarD = 0.025 #内层钢筋直径

#外层钢筋分布信息1
outBarD1 = 0.036 #外层钢筋直径
outBarDist1 = 0.14#外层钢筋间距
outBarNodeDict1 = {1: (3.687, 1.544), 2: (3.187, 1.544), 3: (3.187, 2.044), 4: (-3.187, 2.044), 5: (-3.187, 1.544),
                   6: (-3.687, 1.544),7: (-3.687, -1.544), 8: (-3.187, -1.544), 9: (-3.187, -2.044), 10: (3.187, -2.044),
                   11: (3.187, -1.544), 12: (3.687, -1.544)}
outBarEleDict1 = {1: (1, 2), 2: (2, 3), 3: (3, 4), 4: (4, 5), 5: (6, 5), 6: (5, 2), 7: (7, 8), 8: (8, 9), 9: (9, 10),
                  10: (10, 11), 11: (12, 11), 12: (11, 8)}
#外层钢筋分布信息2
outBarD2 = 0.04 #外层钢筋直径
outBarDist2 = 0.14#外层钢筋间距
outBarNodeDict2 = {1: (3.687, 1.33), 2: (3.687, -1.47), 3: (3.437, 1.33), 4: (3.437, -1.47), 5: (3.187, 1.33),
                   6: (3.187, -1.47),7: (-3.187, 1.33), 8: (-3.187, -1.47), 9: (-3.437, 1.33), 10: (-3.437, -1.47),
                   11: (-3.687, 1.33),12: (-3.687, -1.47)}
outBarEleDict2 = {1: (1, 2), 2: (3, 4), 3: (5, 6), 4: (7, 8), 5: (9, 10), 6: (11, 12)}

sectInstance = PolygonSection(ax, outSideNode, outSideEle, inSideNode, inSideEle)
sectInstance.sectPlot()
outLineList = sectInstance.coverLinePlot(d0)
inLineList = sectInstance.innerLinePlot(d0)
coreFiber=sectInstance.coreMesh(eleSize, outLineList, inLineList)
coverFiber=sectInstance.coverMesh(coverSize, d0)
barFiber=sectInstance.multiBarMesh(d0,outBarDist1,outBarD1,outBarNodeDict1,outBarEleDict1,outBarDist2,outBarD2,outBarNodeDict2,outBarEleDict2,inBarD,inBarDist)
ax.tick_params(direction='in', labelsize=6)
plt.ylabel('transverse (m)',fontdict={'family': 'Times New Roman', 'size': 12})
plt.xlabel('longitudinal (m)',fontdict={'family': 'Times New Roman', 'size': 12})
plt.title('Tower-3 Section')
if not os.path.exists('SectionFig'):
	os.makedirs('SectionFig')
plt.savefig("SectionFig/Tower-3.eps", dpi=600, bbox_inches="tight")
plt.savefig("SectionFig/Tower-3.png", dpi=600, bbox_inches="tight")
if not os.path.exists('Tower-3'):
	os.makedirs('Tower-3')
np.savetxt("Tower-3"+"/coreDivide.txt",coreFiber,fmt="%0.6f %0.6f %0.6f")
np.savetxt("Tower-3"+"/coverDivide.txt",coverFiber,fmt="%0.6f %0.6f %0.6f")
np.savetxt("Tower-3"+"/barDivide.txt",barFiber,fmt="%0.6f %0.6f %0.6f")
plt.show()

fig1 = plt.figure(figsize=(outSideX,outSideY))
ax1 = fig1.add_subplot(111)
coreFiberXList = [each1[0] for each1 in coreFiber]
coreFiberYList = [each1[1] for each1 in coreFiber]
coreFiberAreaList	= [each1[2]	for	each1 in coreFiber]
coverFiberXList =	[each1[0] for each1	in coverFiber]
coverFiberYList =	[each1[1] for each1	in coverFiber]
coverFiberAreaList = [each1[2] for each1 in coverFiber]
barFiberXList	= [each1[0]	for	each1 in barFiber]
barFiberYList	= [each1[1]	for	each1 in barFiber]
barFiberAreaList = [each1[2] for each1 in	barFiber]
ax1.tick_params(direction='in', labelsize=6)
ax1.scatter(coreFiberXList, coreFiberYList, s=3, c="b", zorder=3)
ax1.scatter(coverFiberXList, coverFiberYList,	s=3, c="r",	zorder=3)
ax1.scatter(barFiberXList, barFiberYList,	s=3, c="k",	zorder=3)
ax.tick_params(direction='in', labelsize=6)
plt.ylabel('transverse (m)',fontdict={'family': 'Times New Roman', 'size': 12})
plt.xlabel('longitudinal (m)',fontdict={'family': 'Times New Roman', 'size': 12})
plt.title('Tower-3 Section')
if not os.path.exists('SectionFig'):
	os.makedirs('SectionFig')
plt.savefig("SectionFig/Tower-3Fiber.eps", dpi=600, bbox_inches="tight")
plt.savefig("SectionFig/Tower-3Fiber.png", dpi=600, bbox_inches="tight")
plt.show()
####################################################################################


########################################---桥塔4截面---################################
outSideNode = {1: (3.75,2.75), 2: (-3.75,2.75), 3: (-3.75,2.25), 4: (-4.25,2.25), 5: (-4.25,-2.25), 6: (-3.75,-2.25),\
               7: (-3.75,-2.75), 8: (3.75,-2.75), 9: (3.75,-2.25), 10: (4.25,-2.25), 11: (4.25,2.25), 12: (3.75,2.25)}
outSideEle = {1: (1, 2), 2: (2, 3), 3: (3, 4), 4: (4, 5), 5: (5, 6), 6: (6, 7), 7: (7, 8), 8: (8, 9), 9: (9, 10),\
              10: (10, 11), 11: (11, 12), 12: (12, 1)}
inSideNode = [{1: (2.25, 1.25), 2: (-2.25, 1.25), 3: (-2.75, 0.75), 4: (-2.75, -0.75), 5: (-2.25, -1.25),\
               6: (2.25, -1.25), 7: (2.75, -0.75), 8: (2.75, 0.75)}]
inSideEle = [{1: (1, 2), 2: (2, 3), 3: (3, 4), 4: (4, 5), 5: (5, 6), 6: (6, 7), 7: (7, 8), 8: (8, 1)}]
outSideX=max([outSideNode[i1+1][0] for i1 in range(len(outSideNode))])
outSideY=max([outSideNode[i1+1][1] for i1 in range(len(outSideNode))])
fig = plt.figure(figsize=(outSideX,outSideY))
ax = fig.add_subplot(111)
d0 = 0.06  # 保护层厚度
eleSize = 0.35  # 核心纤维的大小
coverSize = 0.2  # 保护层纤维大小
inBarDist = 0.14 #内层钢筋间距
inBarD = 0.025 #内层钢筋直径

#外层钢筋分布信息1
outBarD1 = 0.036 #外层钢筋直径
outBarDist1 = 0.14#外层钢筋间距
outBarNodeDict1 = {1: (4.166, 2.166), 2: (3.666, 2.166), 3: (3.666, 2.666), 4: (-3.666, 2.666), 5: (-3.666, 2.166),
                   6: (-4.166, 2.166),7: (-4.166, -2.166), 8: (-3.666, -2.166), 9: (-3.666, -2.666), 10: (3.666, -2.666),
                   11: (3.666, -2.166), 12: (4.166, -2.166)}
outBarEleDict1 = {1: (1, 2), 2: (2, 3), 3: (3, 4), 4: (4, 5), 5: (6, 5), 6: (5, 2), 7: (7, 8), 8: (8, 9), 9: (9, 10),
                  10: (10, 11), 11: (12, 11), 12: (11, 8)}
#外层钢筋分布信息2
outBarD2 = 0.04 #外层钢筋直径
outBarDist2 = 0.14#外层钢筋间距
outBarNodeDict2 = {1: (4.166, 2.030), 2: (4.166, -2.170), 3: (3.916, 2.030), 4: (3.916, -2.170), 5: (3.666, 2.030),
                   6: (3.666, -2.170),7: (-3.666, 2.030), 8: (-3.666, -2.170), 9: (-3.916, 2.030), 10: (-3.916, -2.170),
                   11: (-4.166, 2.030),12: (-4.166, -2.170)}
outBarEleDict2 = {1: (1, 2), 2: (3, 4), 3: (5, 6), 4: (7, 8), 5: (9, 10), 6: (11, 12)}

sectInstance = PolygonSection(ax, outSideNode, outSideEle, inSideNode, inSideEle)
sectInstance.sectPlot()
outLineList = sectInstance.coverLinePlot(d0)
inLineList = sectInstance.innerLinePlot(d0)
coreFiber=sectInstance.coreMesh(eleSize, outLineList, inLineList)
coverFiber=sectInstance.coverMesh(coverSize, d0)
barFiber=sectInstance.multiBarMesh(d0,outBarDist1,outBarD1,outBarNodeDict1,outBarEleDict1,outBarDist2,outBarD2,outBarNodeDict2,outBarEleDict2,inBarD,inBarDist)
ax.tick_params(direction='in', labelsize=6)
plt.ylabel('transverse (m)',fontdict={'family': 'Times New Roman', 'size': 12})
plt.xlabel('longitudinal (m)',fontdict={'family': 'Times New Roman', 'size': 12})
plt.title('Tower-4 Section')
if not os.path.exists('SectionFig'):
	os.makedirs('SectionFig')
plt.savefig("SectionFig/Tower-4.eps", dpi=600, bbox_inches="tight")
plt.savefig("SectionFig/Tower-4.png", dpi=600, bbox_inches="tight")
if not os.path.exists('Tower-4'):
	os.makedirs('Tower-4')
np.savetxt("Tower-4"+"/coreDivide.txt",coreFiber,fmt="%0.6f %0.6f %0.6f")
np.savetxt("Tower-4"+"/coverDivide.txt",coverFiber,fmt="%0.6f %0.6f %0.6f")
np.savetxt("Tower-4"+"/barDivide.txt",barFiber,fmt="%0.6f %0.6f %0.6f")
plt.show()

fig1 = plt.figure(figsize=(outSideX,outSideY))
ax1 = fig1.add_subplot(111)
coreFiberXList = [each1[0] for each1 in coreFiber]
coreFiberYList = [each1[1] for each1 in coreFiber]
coreFiberAreaList	= [each1[2]	for	each1 in coreFiber]
coverFiberXList =	[each1[0] for each1	in coverFiber]
coverFiberYList =	[each1[1] for each1	in coverFiber]
coverFiberAreaList = [each1[2] for each1 in coverFiber]
barFiberXList	= [each1[0]	for	each1 in barFiber]
barFiberYList	= [each1[1]	for	each1 in barFiber]
barFiberAreaList = [each1[2] for each1 in	barFiber]
ax1.tick_params(direction='in', labelsize=6)
ax1.scatter(coreFiberXList, coreFiberYList, s=3, c="b", zorder=3)
ax1.scatter(coverFiberXList, coverFiberYList,	s=3, c="r",	zorder=3)
ax1.scatter(barFiberXList, barFiberYList,	s=3, c="k",	zorder=3)
ax.tick_params(direction='in', labelsize=6)
plt.ylabel('transverse (m)',fontdict={'family': 'Times New Roman', 'size': 12})
plt.xlabel('longitudinal (m)',fontdict={'family': 'Times New Roman', 'size': 12})
plt.title('Tower-4 Section')
if not os.path.exists('SectionFig'):
	os.makedirs('SectionFig')
plt.savefig("SectionFig/Tower-4Fiber.eps", dpi=600, bbox_inches="tight")
plt.savefig("SectionFig/Tower-4Fiber.png", dpi=600, bbox_inches="tight")
plt.show()
####################################################################################