Generate sectional fibers based on python programming
## Circle section fiber generate

<img src="https://github.com/Junjun1guo/sectionFiberGenerate/raw/master/circle.png" width =40% height =40% div align="center">

```python
from fiberGenerate import CircleSection
import matplotlib.pyplot as plt
fig = plt.figure(figsize=(5, 5))
x = fig.add_subplot(111)
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
```

##  CircleHole section fiber generate
<img src="https://github.com/Junjun1guo/sectionFiberGenerate/raw/master/circleHole.png" width =40% height =40% div align="center">

```python
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
```

## Polygen section fiber generate
<img src="https://github.com/Junjun1guo/sectionFiberGenerate/raw/master/polygen.png" width =40% height =40% div align="center">

```python
from fiberGenerate import PolygonSection
import matplotlib.pyplot as plt
outSideNode={1:(3.5,3),2:(1.5,5),3:(-1.5,5),4:(-3.5,3),5:(-3.5,-3),6:(-1.5,-5),7:(1.5,-5),8:(3.5,-3)}
outSideEle = {1: (1, 2), 2: (2, 3), 3: (3, 4), 4: (4, 5), 5: (5, 6), 6: (6, 7), 7: (7, 8), 8: (8, 1)}
fig = plt.figure(figsize=(5, 5))
ax = fig.add_subplot(111)
d0 = 0.06  # the thinck of the cover concrete
coreSize = 0.2  # the size of the core concrete fiber elements
coverSize = 0.3  # the size of the cover concrete fiber elements
outBarDist = 0.2 # outside bar space 
outBarD = 0.032 # outside bar diameter
sectInstance = PolygonSection(ax, outSideNode, outSideEle)
sectInstance.sectPlot()
outLineList = sectInstance.coverLinePlot(d0)
coreFiber=sectInstance.coreMesh(coreSize, outLineList)
coverFiber=sectInstance.coverMesh(coverSize, d0)
barFiber=sectInstance.barMesh(outBarD, outBarDist)
plt.show()
```

## PolygenHole section fiber generate
<img src="https://github.com/Junjun1guo/sectionFiberGenerate/raw/master/polygenOneHole.png" width =40% height =40% div align="center">

```python
from fiberGenerate import PolygonSection
import matplotlib.pyplot as plt
outSideNode={1:(3.5,3),2:(1.5,5),3:(-1.5,5),4:(-3.5,3),5:(-3.5,-3),6:(-1.5,-5),7:(1.5,-5),8:(3.5,-3)}
outSideEle = {1: (1, 2), 2: (2, 3), 3: (3, 4), 4: (4, 5), 5: (5, 6), 6: (6, 7), 7: (7, 8), 8: (8, 1)}
inSideNode=[{1:(1.9,2.4),2:(1.1,3.2),3:(-1.1,3.2),4:(-1.9,2.4),5:(-1.9,-2.4),6:(-1.1,-3.2),7:(1.1,-3.2),8:(1.9,-2.4)}]
inSideEle = [{1: (1, 2), 2: (2, 3), 3: (3, 4), 4: (4, 5), 5: (5, 6), 6: (6, 7), 7: (7, 8), 8: (8, 1)}]
fig = plt.figure(figsize=(5, 5))
ax = fig.add_subplot(111)
d0 = 0.06  # the thinck of the cover concrete
coreSize = 0.2  # the size of the core concrete fiber elements
coverSize = 0.3  # the size of the cover concrete fiber elements
outBarDist = 0.2 # outside bar space 
outBarD = 0.032 # outside bar diameter
inBarD=0.032
inBarDist=0.2
sectInstance = PolygonSection(ax, outSideNode, outSideEle,inSideNode,inSideEle)
sectInstance.sectPlot()
outLineList = sectInstance.coverLinePlot(d0)
inLineList = sectInstance.innerLinePlot(d0)
coreFiber=sectInstance.coreMesh(coreSize, outLineList,inLineList)
coverFiber=sectInstance.coverMesh(coverSize, d0)
barFiber=sectInstance.barMesh(outBarD, outBarDist,inBarDist,outBarDist)
plt.show()
```

## PolygenTwoHole section fiber generate
<img src="https://github.com/Junjun1guo/sectionFiberGenerate/raw/master/polygenTwoHole.png" width =40% height =40% div align="center">

```python
from fiberGenerate import PolygonSection
import matplotlib.pyplot as plt
outSideNode = {1: (4.5,6.655), 2: (2.5, 8.655), 3: (-2.5,8.655), 4: (-4.5, 6.655), 5: (-4.5, -6.655), 6: (-2.5, -8.655), 7: (2.5, -8.655),
            8: (4.5, -6.655)}
outSideEle = {1: (1, 2), 2: (2, 3), 3: (3, 4), 4: (4, 5), 5: (5, 6), 6: (6, 7), 7: (7, 8), 8: (8, 1)}
inSideNode = [{1: (2.5, 5.855), 2: (1.7, 6.655), 3: (-1.7,6.655), 4: (-2.5, 5.855), 5: (-2.5, 1.3), 6: (-1.7, 0.5), 7: (1.7, 0.5),8: (2.5,1.3)},
            {1:(2.5,-1.3),2:(1.7,-0.5),3:(-1.7,-0.5),4:(-2.5,-1.3),5:(-2.5,-5.855),6:(-1.7,-6.655),7:(1.7,-6.655),8:(2.5,-5.855)}]
inSideEle = [{1: (1, 2), 2: (2, 3), 3: (3, 4), 4: (4, 5), 5: (5, 6), 6: (6, 7), 7: (7, 8), 8: (8, 1)},{1: (1, 2), 2: (2, 3), 3: (3, 4), 4: (4, 5), 5: (5, 6), 6: (6, 7), 7: (7, 8), 8: (8, 1)}]
fig = plt.figure(figsize=(5, 5))
ax = fig.add_subplot(111)
d0 = 0.06  # the thinck of the cover concrete
coreSize = 0.2  # the size of the core concrete fiber elements
coverSize = 0.3  # the size of the cover concrete fiber elements
outBarDist = 0.2 # outside bar space 
outBarD = 0.032 # outside bar diameter
inBarD=0.032
inBarDist=0.2
sectInstance = PolygonSection(ax, outSideNode, outSideEle,inSideNode,inSideEle)
sectInstance.sectPlot()
outLineList = sectInstance.coverLinePlot(d0)
inLineList = sectInstance.innerLinePlot(d0)
coreFiber=sectInstance.coreMesh(coreSize, outLineList,inLineList)
coverFiber=sectInstance.coverMesh(coverSize, d0)
barFiber=sectInstance.barMesh(outBarD, outBarDist,inBarDist,outBarDist)
plt.show()
```
