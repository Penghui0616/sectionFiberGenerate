Generate sectional fibers based on python programming

## Install
pip install sectionFiberDivide

After installation through python script, then download gmsh that satifies your operation system. And copy gmsh.ext to your working directory. 

The followings are some basic examples, you can also obtain these examples using help(circleSection) and help(polygonSection).

## Circle section fiber generate

<img src="https://github.com/Junjun1guo/sectionFiberGenerate/raw/master/circle.png" width =40% height =40% div align="center">

```python
from sectionFiberMain import circleSection,polygonSection
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
from sectionFiberMain import circleSection,polygonSection
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
from sectionFiberMain import circleSection,polygonSection
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
from sectionFiberMain import circleSection,polygonSection
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
from sectionFiberMain import circleSection,polygonSection
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
