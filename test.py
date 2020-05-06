from cythonSectionFiber import CircleSection,PolygonSection
import matplotlib.pyplot as plt
from cythonSectionFiber import figureSize
import cProfile
def callFun():
    outSideNode = {1: (4.5, 6.655), 2: (2.5, 8.655), 3: (-2.5, 8.655), 4: (-4.5, 6.655), 5: (-4.5, -6.655),
                   6: (-2.5, -8.655), 7: (2.5, -8.655),
                   8: (4.5, -6.655)}
    outSideEle = {1: (1, 2), 2: (2, 3), 3: (3, 4), 4: (4, 5), 5: (5, 6), 6: (6, 7), 7: (7, 8), 8: (8, 1)}
    inSideNode = [{1: (2.5, 5.855), 2: (1.7, 6.655), 3: (-1.7, 6.655), 4: (-2.5, 5.855), 5: (-2.5, 1.3), 6: (-1.7, 0.5),
                   7: (1.7, 0.5), 8: (2.5, 1.3)},
                  {1: (2.5, -1.3), 2: (1.7, -0.5), 3: (-1.7, -0.5), 4: (-2.5, -1.3), 5: (-2.5, -5.855),
                   6: (-1.7, -6.655), 7: (1.7, -6.655), 8: (2.5, -5.855)}]
    inSideEle = [{1: (1, 2), 2: (2, 3), 3: (3, 4), 4: (4, 5), 5: (5, 6), 6: (6, 7), 7: (7, 8), 8: (8, 1)},
                 {1: (1, 2), 2: (2, 3), 3: (3, 4), 4: (4, 5), 5: (5, 6), 6: (6, 7), 7: (7, 8), 8: (8, 1)}]
    w, h = figureSize(outSideNode)
    fig = plt.figure(figsize=(w, h))
    ax = fig.add_subplot(111)
    coverColor="r"
    coreColor="b"
    lineWid=1
    barMarkSize=20
    barColor="k"
    coverThick = 0.1 # the thinck of the cover concrete
    coreSize = 0.05  # the size of the core concrete fiber elements
    coverSize = 0.2  # the size of the cover concrete fiber elements
    outBarDist = 0.2  # outside bar space
    outBarD = 0.032  # outside bar diameter
    inBarD = 0.032
    inBarDist = 0.2
    sectInstance = PolygonSection(outSideNode, outSideEle, inSideNode, inSideEle)
    originalNodeListPlot=sectInstance.sectPlot()    #[([x1,x2],[y1,y2]),([].[])]
    for each1 in originalNodeListPlot:
        ax.plot(each1[0], each1[1], coverColor, lineWid, zorder=0)
    outLineList,coverlineListPlot = sectInstance.coverLinePlot(coverThick)
    for each2 in coverlineListPlot:
        ax.plot(each2[0], each2[1], coverColor, lineWid, zorder=1)
    inLineList,innerLineListPlot = sectInstance.innerLinePlot(coverThick)
    for each3 in innerLineListPlot:
        ax.plot(each3[0], each3[1], coverColor, lineWid, zorder=1)
    coreFiber,pointsPlot,trianglesPlot= sectInstance.coreMesh(coreSize, outLineList, inLineList)
    ax.triplot(pointsPlot[:, 0], pointsPlot[:, 1], trianglesPlot, c=coreColor, lw=lineWid)
    coverFiber,outNodeReturnPlot,inNodeReturnPlot = sectInstance.coverMesh(coverSize, coverThick)
    for i1 in range(len(outNodeReturnPlot) - 1):
        ax.plot([inNodeReturnPlot[i1][0], outNodeReturnPlot[i1][0]], [inNodeReturnPlot[i1][1], outNodeReturnPlot[i1][1]],
                     coverColor, linewidth=lineWid, zorder=0)
    barFiber,barXListPlot,barYListPlot= sectInstance.barMesh(outBarD, outBarDist, coverThick, inBarD, inBarDist)
    ax.scatter(barXListPlot,barYListPlot, s=barMarkSize, c=barColor, linewidth=lineWid, zorder=2)
    plt.show()

def callCircleFun():
    fig = plt.figure(figsize=(5, 5))
    ax = fig.add_subplot(111)
    outbarD = 0.03  # outside bar diameter
    outbarDist = 0.15  # outside bar space
    inBarD = 0.03  # inside bar diameter
    inBarDist = 0.15  # inside bar space
    d0 = 0.1  # the thinckness of the cover concrete
    coreSize = 0.1  # the size of core concrete fiber
    coverSize = 0.15  # the size of cover concrete fiber
    outD = 20  # the diameter of the outside circle
    inD = 1  # the diameter of the inner circle
    circleInstance = CircleSection(d0, outD, inD)  # call the circle section generate class
    xListPlot,yListPlot=circleInstance.initSectionPlot()  # plot profile of the circle
    for eachx,eachy in zip(xListPlot,yListPlot):
        ax.plot(eachx, eachy, "r", linewidth=1, zorder=2)
    # generate core concrete fiber elements
    coreFiber,pointsPlot,trianglesPlot = circleInstance.coreMesh(coreSize)
    ax.triplot(pointsPlot[:, 0], pointsPlot[:, 1], trianglesPlot)
    # generate cover concrete fiber elements
    coverFiber,coverXListPlot,coverYListPlot,xBorderPlot,yBorderPlot = circleInstance.coverMesh(coverSize)
    for coverx,covery in zip(coverXListPlot,coverYListPlot):
        ax.plot(coverx,covery, "r", linewidth=1, zorder=2)
    for borderx,bordery in zip(xBorderPlot,yBorderPlot):
        ax.plot(borderx, bordery, "r", linewidth=1, zorder=2)
    # generate the bar fiber elements
    barFiber,barXListPlot,barYListPlot = circleInstance.barMesh(outbarD, outbarDist, inBarD, inBarDist)
    for barx,bary in zip(barXListPlot,barYListPlot):
        ax.scatter(barx, bary, s=10, c="k", zorder=3)
    plt.show()
cProfile.run("callFun()",sort="cumtime")




