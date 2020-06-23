Generate sectional fibers based on python programming

## Install    [the package in PyPI](https://pypi.org/project/sectionFiberDivide/)
pip install sectionFiberDivide  

After installation through python script, then download gmsh ([download gmsh](https://gmsh.info/)) that satifies your operation system. And copy gmsh.exe to your working directory. 

The followings are some basic examples, you can also obtain these examples using help(circleSection) and help(polygonSection).

## Circle section fiber generate

<img src="https://github.com/Junjun1guo/sectionFiberGenerate/raw/master/circle.png" width =40% height =40% div align="center">

```python
from sectionFiberDivide import circleSection
outD=2  # the diameter of the outside circle
coverThick=0.1  # the thinckness of the cover concrete
outbarD=0.03  # outside bar diameter
outbarDist=0.15  # outside bar space
coreSize=0.2  # the size of core concrete fiber
coverSize=0.2  # the size of cover concrete fiber
plotState=False  # plot the fiber or not plot=True or False
corFiber,coverFiber,barFiber=circleSection(outD, coverThick, outbarD, outbarDist, coreSize, coverSize,plotState)
```

##  CircleHole section fiber generate
<img src="https://github.com/Junjun1guo/sectionFiberGenerate/raw/master/circleHole.png" width =40% height =40% div align="center">

```python
from sectionFiberDivide import circleSection
outD = 2  # the diameter of the outside circle
coverThick = 0.06  # the thinckness of the cover concrete
outbarD = 0.03  # outside bar diameter
outbarDist = 0.15  # outside bar space
coreSize = 0.1  # the size of core concrete fiber
coverSize = 0.1  # the size of cover concrete fiber
plotState = True  # plot the fiber or not plot=True or False
inD =1 # the diameter of the inside circle
inBarD=0.03 # inside bar diameter
inBarDist=0.15 # inside bar space
corFiber, coverFiber, barFiber = circleSection(outD, coverThick, outbarD, outbarDist, coreSize, coverSize,
                                                   plotState,inD,inBarD,inBarDist)
```

## Polygen section fiber generate
<img src="https://github.com/Junjun1guo/sectionFiberGenerate/raw/master/polygen.png" width =40% height =40% div align="center">

```python
from sectionFiberDivide import polygonSection
# the outside vertexes consecutively numbering and coordinate values in local y-z plane in dict container
outSideNode = {1: (3.5, 3), 2: (1.5, 5), 3: (-1.5, 5), 4: (-3.5, 3), 5: (-3.5, -3), 6: (-1.5, -5), 7: (1.5, -5),
                   8: (3.5, -3)}
# the outside vertexes loop consecutively numbering in dict container
outSideEle = {1: (1, 2), 2: (2, 3), 3: (3, 4), 4: (4, 5), 5: (5, 6), 6: (6, 7), 7: (7, 8), 8: (8, 1)}
coverThick = 0.06  # the thinck of the cover concrete
coreSize = 0.2  # the size of the core concrete fiber elements
coverSize = 0.3  # the size of the cover concrete fiber elements
outBarD = 0.032  # outside bar diameter
outBarDist = 0.2  # outside bar space
plotState=True  # plot the fiber or not plot=True or False
coreFiber,coverFiber,barFiber=polygonSection(outSideNode, outSideEle, coverThick, coreSize, coverSize,\
                                                outBarD, outBarDist,plotState)
```

## PolygenHole section fiber generate
<img src="https://github.com/Junjun1guo/sectionFiberGenerate/raw/master/polygenOneHole.png" width =40% height =40% div align="center">

```python
from sectionFiberDivide import polygonSection
# the outside vertexes consecutively numbering and coordinate values in local y-z plane in dict container
outSideNode = {1: (3.5, 3), 2: (1.5, 5), 3: (-1.5, 5), 4: (-3.5, 3), 5: (-3.5, -3), 6: (-1.5, -5), 7: (1.5, -5),
                   8: (3.5, -3)}
# the outside vertexes loop consecutively numbering in dict container
outSideEle = {1: (1, 2), 2: (2, 3), 3: (3, 4), 4: (4, 5), 5: (5, 6), 6: (6, 7), 7: (7, 8), 8: (8, 1)}
# the inside vertexes consecutively numbering and coordinate values in local y-z plane in list container
inSideNode = [
        {1: (1.9, 2.4), 2: (1.1, 3.2), 3: (-1.1, 3.2), 4: (-1.9, 2.4), 5: (-1.9, -2.4), 6: (-1.1, -3.2), 7: (1.1, -3.2),
         8: (1.9, -2.4)}]
# the inside vertexes loop consecutively numbering in dict container
inSideEle = [{1: (1, 2), 2: (2, 3), 3: (3, 4), 4: (4, 5), 5: (5, 6), 6: (6, 7), 7: (7, 8), 8: (8, 1)}]
coverThick = 0.06  # the thinck of the cover concrete
coreSize = 0.2  # the size of the core concrete fiber elements
coverSize = 0.3  # the size of the cover concrete fiber elements
outBarD = 0.032  # outside bar diameter
outBarDist = 0.2  # outside bar space
plotState=True  # plot the fiber or not plot=True or False
inBarD=0.032  # inside bar diameter
inBarDist=0.2  # inside bar space
coreFiber,coverFiber,barFiber=polygonSection(outSideNode, outSideEle, coverThick, coreSize, coverSize,\
                                        outBarD, outBarDist,plotState,inSideNode,inSideEle,inBarD,inBarDist)
```

## PolygenThreeHole section fiber generate
<img src="https://github.com/Junjun1guo/sectionFiberGenerate/raw/branch-cythonVersion/polygonThrewHoles.jpg" width =40% height =40% div align="center">

```python
from sectionFiberDivide import polygonSection
outSideNode = {1: (0, 0), 2: (7, 0), 3: (7,3), 4: (0, 3)}
# the outside vertexes loop consecutively numbering in dict container
outSideEle = {1: (1, 2), 2: (2, 3), 3: (3, 4), 4: (4,1)}
# the inside vertexes consecutively numbering and coordinate values in local y-z plane in list container
inSideNode = [
        {1: (1, 1), 2: (2, 1), 3: (2, 2), 4: (1, 2)},
        {1: (3, 1), 2: (4, 1), 3: (4, 2), 4: (3, 2)},
        {1: (5, 1), 2: (6, 1), 3: (6, 2), 4: (5, 2)}]
# the inside vertexes loop consecutively numbering in dict container
inSideEle = [{1: (1, 2), 2: (2, 3), 3: (3, 4), 4: (4, 1)},
                 {1: (1, 2), 2: (2, 3), 3: (3, 4), 4: (4, 1)},
                 {1: (1, 2), 2: (2, 3), 3: (3, 4), 4: (4, 1)}]
coverThick = 0.06  # the thinck of the cover concrete
coreSize = 0.2  # the size of the core concrete fiber elements
coverSize = 0.3  # the size of the cover concrete fiber elements
outBarD = 0.032  # outside bar diameter
outBarDist = 0.2  # outside bar space
plotState = False  # plot the fiber or not plot=True or False
inBarD = 0.032  # inside bar diameter
inBarDist = 0.2  # inside bar space
coreFiber, coverFiber, barFiber = polygonSection(outSideNode, outSideEle, coverThick, coreSize, coverSize, \
                                                     outBarD, outBarDist, plotState, inSideNode, inSideEle, inBarD,
                                                     inBarDist)
```


## Multi-layer Reinforcement
<img src="Pictures/TowerSection.png" width =40% height =40% div align="center">

```python
########################################---A Tower Section---################################
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
d0 = 0.06  # the thinck of the cover concrete
eleSize = 0.2  # the size of the core concrete fiber elements
coverSize = 0.2  # the size of the cover concrete fiber elements
inBarDist = 0.14 # inside bar space
inBarD = 0.025 # inside bar diameter

#outside bar arrangement information 1
outBarD1 = 0.036 # outside bar diameter
outBarDist1 = 0.14 # outside bar space
outBarNodeDict1 = {1: (2.975, 1.516), 2: (2.475, 1.516), 3: (2.475, 2.016), 4: (-2.475, 2.016), 5: (-2.475, 1.516),
                   6: (-2.975, 1.516),7: (-2.975, -1.516), 8: (-2.475, -1.516), 9: (-2.475, -2.016), 10: (2.475, -2.016),
                   11: (2.475, -1.516), 12: (2.975, -1.516)}
outBarEleDict1 = {1: (1, 2), 2: (2, 3), 3: (3, 4), 4: (4, 5), 5: (6, 5), 6: (5, 2), 7: (7, 8), 8: (8, 9), 9: (9, 10),
                  10: (10, 11), 11: (12, 11), 12: (11, 8)}
#outside bar arrangement information 2
outBarD2 = 0.04 # outside bar diameter
outBarDist2 = 0.14 # outside bar space
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