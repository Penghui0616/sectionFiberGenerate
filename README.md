# sectionFiberGenerate
Generate sectional fibers based on python programming
## Circle section fiber generate
<img src="https://github.com/Junjun1guo/sectionFiberGenerate/raw/master/circle.png" width =40% height =40% div align="center">

```python
from fiberGenerate import CircleSection
import matplotlib.pyplot as plt
fig = plt.figure(figsize=(5,5))
ax = fig.add_subplot(111)
outbarD=0.03 #outside bar diameter 
outbarDist=0.15 #outside bar space
inBarD=0.03 #inside bar diameter
inBarDist=0.15 #inside bar space
d0=0.1 #the thinckness of the cover concrete
eleSize=0.15  #the size of core concrete fiber 
coverSize=0.15 #the size of cover concrete fiber
outD=3 #the diameter of the outside circle
inD=1 # the diameter of the inner circle

circleInstance=CircleSection(ax,d0,outD,inD) #call the circle section generate class
circleInstance.sectPlot() #plot profile of the circle
coreFiber=circleInstance.coreMesh(eleSize) #generate core concrete fiber elements
coverFiber=circleInstance.coverMesh(coverSize) #generate cover concrete fiber elements
barFiber=circleInstance.barMesh(outbarD, outbarDist,inD,inBarDist) #generate the bar fiber elements
plt.plot()
```

##  CircleHole section fiber generate
<img src="https://github.com/Junjun1guo/sectionFiberGenerate/raw/master/circleHole.png" width =40% height =40% div align="center">

## Polygen section fiber generate
<img src="https://github.com/Junjun1guo/sectionFiberGenerate/raw/master/polygen.png" width =40% height =40% div align="center">

## PolygenHole section fiber generate
<img src="https://github.com/Junjun1guo/sectionFiberGenerate/raw/master/polygenOneHole.png" width =40% height =40% div align="center">

## PolygenTwoHole section fiber generate
<img src="https://github.com/Junjun1guo/sectionFiberGenerate/raw/master/polygenTwoHole.png" width =40% height =40% div align="center">
