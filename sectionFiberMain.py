######################################################################################
#  Author: Junjun Guo
#  E-mail: guojj@tongji.edu.cn/guojj_ce@163.com
#    Date: 05/02/2020
#  Environemet: Successfully excucted in python 3.6
######################################################################################
import matplotlib.pyplot as plt
try:
    from cythonSectionFiber import CircleSection,PolygonSection
    from cythonSectionFiber import figureSize

    print("*" * 50)
    print("cython version of sectionFiber works!")
    print("*" * 50)
except ModuleNotFoundError:
    from fiberGenerate import CircleSection,PolygonSection,figureSize

    print("*" * 50)
    print("python version of sectionFiber works!")
    print("*" * 50)
######################################################################################
def circleSection(outD,coverThick,outbarD,outbarDist,coreSize,coverSize,plot=False,inD=None,inBarD=None,inBarDist=None):
    """
    #####################################################################
    def circleSection(outD,coverThick,outbarD,outbarDist,coreSize,coverSize,plot=False,inD=None,inBarD=None,inBarDist=None)
    Input:
    ---outD # the diameter of the outside circle
    ---coverThick # the thinckness of the cover concrete
    ---outbarD # outside bar diameter
    ---outbarDist # outside bar space
    ---coreSize # the size of core concrete fiber
    ---coverSize # the size of cover concrete fiber
    ---plot #plot the fiber or not plot=True or False
    ---inD # the diameter of the inner circle,if not inD=None
    ---inBarD # inside bar diameter, if not inBarD=None
    ---inBarDist # inside bar space,if not inBarDist=None
    Output:
    ---coreFiber,coverFiber,barFiber #core concrete, cover concrete anb bar fibers information
       for eaxample coreFiber=[(y1,z1,area1),(y2,y2,area2),...], y1,z1 is the fiber coordinate values in loacal y-z plane
       area1 is the fiber area
    #####################################################################
    #######################---solid circle example---#####################
    outD=2  # the diameter of the outside circle
    coverThick=0.1  # the thinckness of the cover concrete
    outbarD=0.03  # outside bar diameter
    outbarDist=0.15  # outside bar space
    coreSize=0.2  # the size of core concrete fiber
    coverSize=0.2  # the size of cover concrete fiber
    plotState=False  # plot the fiber or not plot=True or False
    corFiber,coverFiber,barFiber=circleSection(outD, coverThick, outbarD, outbarDist, coreSize, coverSize,plotState)
    ######################################################################
    ##################---circle with a hole example---####################
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
    ######################################################################
    """
    circleInstance = CircleSection(coverThick, outD, inD)  # call the circle section generate class
    xListPlot, yListPlot = circleInstance.initSectionPlot()  # plot profile of the circle
    # generate core concrete fiber elements
    coreFiber, pointsPlot, trianglesPlot = circleInstance.coreMesh(coreSize)
    # generate cover concrete fiber elements
    coverFiber, coverXListPlot, coverYListPlot, xBorderPlot, yBorderPlot = circleInstance.coverMesh(coverSize)
    # generate the bar fiber elements
    barFiber, barXListPlot, barYListPlot = circleInstance.barMesh(outbarD, outbarDist, inBarD, inBarDist)
    if plot==True:
        outSideNode = {1: (-outD,-outD), 2: (outD,outD)}
        w, h = figureSize(outSideNode)
        fig = plt.figure(figsize=(w, h))
        ax = fig.add_subplot(111)
        for eachx, eachy in zip(xListPlot, yListPlot):
            ax.plot(eachx, eachy, "r", linewidth=1, zorder=2)

        ax.triplot(pointsPlot[:, 0], pointsPlot[:, 1], trianglesPlot)

        for coverx, covery in zip(coverXListPlot, coverYListPlot):
            ax.plot(coverx, covery, "r", linewidth=1, zorder=2)
        for borderx, bordery in zip(xBorderPlot, yBorderPlot):
            ax.plot(borderx, bordery, "r", linewidth=1, zorder=2)

        for barx, bary in zip(barXListPlot, barYListPlot):
            ax.scatter(barx, bary, s=10, c="k", zorder=3)
        plt.savefig("cricleSectionFiber.eps")
        plt.savefig("cricleSectionFiber.jpg")
        plt.show()
    else:
        pass
    return coreFiber,coverFiber,barFiber
######################################################################################
######################################################################################
######################################################################################
def polygonSection(outSideNode,outSideEle,coverThick,coreSize,coverSize,outBarD,outBarDist,\
                   plot=False,inSideNode=None,inSideEle=None,inBarD=None,inBarDist=None):
    """
    Input:
    ---outSideNode # the outside vertexes consecutively numbering and coordinate values in local y-z plane in dict container
    ---outSideEle  # the outside vertexes loop consecutively numbering in dict container
    ---coverThick  # the thinck of the cover concrete
    ---coreSize  # the size of the core concrete fiber elements
    ---coverSize   # the size of the cover concrete fiber elements
    ---outBarD  # outside bar diameter
    ---outBarDist  # outside bar space
    ---plot=True # plot the fiber or not plot=True or False
    ---inSideNode #the inside vertexes consecutively numbering and coordinate values in local y-z plane in list container
    ---inSideEle # the inside vertexes loop consecutively numbering in list container
    ---inBarD #inside bar diameter
    ---inBarDist #inside bar space
    Output:
    ---coreFiber,coverFiber,barFiber #core concrete, cover concrete anb bar fibers information
       for eaxample coreFiber=[(y1,z1,area1),(y2,y2,area2),...], y1,z1 is the fiber coordinate values in loacal y-z plane
       area1 is the fiber area

    #####################################################################
    ################---solid polygon section example---##################
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
    #####################################################################
    ############---polygon with one hole section example---##############
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
    #####################################################################
    ############---polygon with three holes section example---###########
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
    ######################################################################
    """
    sectInstance = PolygonSection(outSideNode, outSideEle, inSideNode, inSideEle)
    originalNodeListPlot = sectInstance.sectPlot()  # [([x1,x2],[y1,y2]),([].[])]
    outLineList, coverlineListPlot = sectInstance.coverLinePlot(coverThick)
    if inSideNode==None:
        sectInstance = PolygonSection(outSideNode, outSideEle)
        originalNodeListPlot = sectInstance.sectPlot()  # [([x1,x2],[y1,y2]),([].[])]
        outLineList, coverlineListPlot = sectInstance.coverLinePlot(coverThick)
        coreFiber, pointsPlot, trianglesPlot = sectInstance.coreMesh(coreSize, outLineList)
        coverFiber, outNodeReturnPlot, inNodeReturnPlot = sectInstance.coverMesh(coverSize, coverThick)
        barFiber, barXListPlot, barYListPlot = sectInstance.barMesh(outBarD, outBarDist, coverThick)
    else:
        sectInstance = PolygonSection(outSideNode, outSideEle, inSideNode, inSideEle)
        originalNodeListPlot = sectInstance.sectPlot()
        outLineList, coverlineListPlot = sectInstance.coverLinePlot(coverThick)
        inLineList, innerLineListPlot = sectInstance.innerLinePlot(coverThick)
        coreFiber, pointsPlot, trianglesPlot = sectInstance.coreMesh(coreSize, outLineList, inLineList)
        coverFiber, outNodeReturnPlot, inNodeReturnPlot = sectInstance.coverMesh(coverSize, coverThick)
        barFiber, barXListPlot, barYListPlot = sectInstance.barMesh(outBarD, outBarDist, coverThick, inBarD, inBarDist)
    if inSideNode==None and plot==True:
        w, h = figureSize(outSideNode)
        fig = plt.figure(figsize=(w, h))
        ax = fig.add_subplot(111)
        coverColor = "r"
        coreColor = "b"
        lineWid = 1
        barMarkSize = 20
        barColor = "k"
        for each1 in originalNodeListPlot:
            ax.plot(each1[0], each1[1], coverColor, lineWid, zorder=0)
        for each2 in coverlineListPlot:
            ax.plot(each2[0], each2[1], coverColor, lineWid, zorder=1)
        ax.triplot(pointsPlot[:, 0], pointsPlot[:, 1], trianglesPlot, c=coreColor, lw=lineWid)
        for i1 in range(len(outNodeReturnPlot) - 1):
            ax.plot([inNodeReturnPlot[i1][0], outNodeReturnPlot[i1][0]],
                    [inNodeReturnPlot[i1][1], outNodeReturnPlot[i1][1]],
                    coverColor, linewidth=lineWid, zorder=0)
        ax.scatter(barXListPlot, barYListPlot, s=barMarkSize, c=barColor, linewidth=lineWid, zorder=2)
        plt.savefig("polygonSectionFiber.eps")
        plt.savefig("polygonSectionFiber.jpg")
        plt.show()
    elif inSideNode!=None and plot==True:
        w, h = figureSize(outSideNode)
        fig = plt.figure(figsize=(w, h))
        ax = fig.add_subplot(111)
        coverColor = "r"
        coreColor = "b"
        lineWid = 1
        barMarkSize = 20
        barColor = "k"
        for each1 in originalNodeListPlot:
            ax.plot(each1[0], each1[1], coverColor, lineWid, zorder=0)
        for each2 in coverlineListPlot:
            ax.plot(each2[0], each2[1], coverColor, lineWid, zorder=1)
        for each3 in innerLineListPlot:
            ax.plot(each3[0], each3[1], coverColor, lineWid, zorder=1)
        ax.triplot(pointsPlot[:, 0], pointsPlot[:, 1], trianglesPlot, c=coreColor, lw=lineWid)
        for i1 in range(len(outNodeReturnPlot) - 1):
            ax.plot([inNodeReturnPlot[i1][0], outNodeReturnPlot[i1][0]],
                    [inNodeReturnPlot[i1][1], outNodeReturnPlot[i1][1]],
                    coverColor, linewidth=lineWid, zorder=0)
        ax.scatter(barXListPlot, barYListPlot, s=barMarkSize, c=barColor, linewidth=lineWid, zorder=2)
        plt.savefig("polygonSectionFiber.eps")
        plt.savefig("polygonSectionFiber.jpg")
        plt.show()

    else:
        pass
    return coreFiber,coverFiber,barFiber
######################################################################################
# if __name__ == "__main__":
    ###################---solid circle---################
    ####################################################
    # outD=2  # the diameter of the outside circle
    # coverThick=0.1  # the thinckness of the cover concrete
    # outbarD=0.03  # outside bar diameter
    # outbarDist=0.15  # outside bar space
    # coreSize=0.2  # the size of core concrete fiber
    # coverSize=0.2  # the size of cover concrete fiber
    # plotState=True  # plot the fiber or not plot=True or False
    # corFiber,coverFiber,barFiber=circleSection(outD, coverThick, outbarD, outbarDist, coreSize, coverSize,plotState)
    ###################---circle with a hole ---################
    ####################################################
    # outD = 2  # the diameter of the outside circle
    # coverThick = 0.06  # the thinckness of the cover concrete
    # outbarD = 0.03  # outside bar diameter
    # outbarDist = 0.15  # outside bar space
    # coreSize = 0.1  # the size of core concrete fiber
    # coverSize = 0.1  # the size of cover concrete fiber
    # plotState = True  # plot the fiber or not plot=True or False
    # inD =1 # the diameter of the inside circle
    # inBarD=0.03 # inside bar diameter
    # inBarDist=0.15 # inside bar space
    # corFiber, coverFiber, barFiber = circleSection(outD, coverThick, outbarD, outbarDist, coreSize, coverSize,
    #                                                plotState,inD,inBarD,inBarDist)
    ############---solid polygon section ---############
    ####################################################
    # the outside vertexes consecutively numbering and coordinate values in local y-z plane in dict container
    # outSideNode = {1: (3.5, 3), 2: (1.5, 5), 3: (-1.5, 5), 4: (-3.5, 3), 5: (-3.5, -3), 6: (-1.5, -5), 7: (1.5, -5),
    #                8: (3.5, -3)}
    # # the outside vertexes loop consecutively numbering in dict container
    # outSideEle = {1: (1, 2), 2: (2, 3), 3: (3, 4), 4: (4, 5), 5: (5, 6), 6: (6, 7), 7: (7, 8), 8: (8, 1)}
    # coverThick = 0.06  # the thinck of the cover concrete
    # coreSize = 0.2  # the size of the core concrete fiber elements
    # coverSize = 0.3  # the size of the cover concrete fiber elements
    # outBarD = 0.032  # outside bar diameter
    # outBarDist = 0.2  # outside bar space
    # plotState=True  # plot the fiber or not plot=True or False
    # coreFiber,coverFiber,barFiber=polygonSection(outSideNode, outSideEle, coverThick, coreSize, coverSize,\
    #                                             outBarD, outBarDist,plotState)
    #####################################################################
    ############---polygon with one hole section example---##############
    ## the outside vertexes consecutively numbering and coordinate values in local y-z plane in dict container
    # outSideNode = {1: (3.5, 3), 2: (1.5, 5), 3: (-1.5, 5), 4: (-3.5, 3), 5: (-3.5, -3), 6: (-1.5, -5), 7: (1.5, -5),
    #                8: (3.5, -3)}
    # # the outside vertexes loop consecutively numbering in dict container
    # outSideEle = {1: (1, 2), 2: (2, 3), 3: (3, 4), 4: (4, 5), 5: (5, 6), 6: (6, 7), 7: (7, 8), 8: (8, 1)}
    # # the inside vertexes consecutively numbering and coordinate values in local y-z plane in list container
    # inSideNode = [
    #     {1: (1.9, 2.4), 2: (1.1, 3.2), 3: (-1.1, 3.2), 4: (-1.9, 2.4), 5: (-1.9, -2.4), 6: (-1.1, -3.2), 7: (1.1, -3.2),
    #      8: (1.9, -2.4)}]
    # # the inside vertexes loop consecutively numbering in dict container
    # inSideEle = [{1: (1, 2), 2: (2, 3), 3: (3, 4), 4: (4, 5), 5: (5, 6), 6: (6, 7), 7: (7, 8), 8: (8, 1)}]
    # coverThick = 0.06  # the thinck of the cover concrete
    # coreSize = 0.2  # the size of the core concrete fiber elements
    # coverSize = 0.3  # the size of the cover concrete fiber elements
    # outBarD = 0.032  # outside bar diameter
    # outBarDist = 0.2  # outside bar space
    # plotState=True  # plot the fiber or not plot=True or False
    # inBarD=0.032  # inside bar diameter
    # inBarDist=0.2  # inside bar space
    # coreFiber,coverFiber,barFiber=polygonSection(outSideNode, outSideEle, coverThick, coreSize, coverSize,\
    #                                     outBarD, outBarDist,plotState,inSideNode,inSideEle,inBarD,inBarDist)
    #####################################################################
    # ############---polygon with three holes section example---###########
    # outSideNode = {1: (0, 0), 2: (7, 0), 3: (7,3), 4: (0, 3)}
    # # the outside vertexes loop consecutively numbering in dict container
    # outSideEle = {1: (1, 2), 2: (2, 3), 3: (3, 4), 4: (4,1)}
    # # the inside vertexes consecutively numbering and coordinate values in local y-z plane in list container
    # inSideNode = [
    #     {1: (1, 1), 2: (2, 1), 3: (2, 2), 4: (1, 2)},
    #     {1: (3, 1), 2: (4, 1), 3: (4, 2), 4: (3, 2)},
    #     {1: (5, 1), 2: (6, 1), 3: (6, 2), 4: (5, 2)}]
    # # the inside vertexes loop consecutively numbering in dict container
    # inSideEle = [{1: (1, 2), 2: (2, 3), 3: (3, 4), 4: (4, 1)},
    #              {1: (1, 2), 2: (2, 3), 3: (3, 4), 4: (4, 1)},
    #              {1: (1, 2), 2: (2, 3), 3: (3, 4), 4: (4, 1)}]
    # coverThick = 0.06  # the thinck of the cover concrete
    # coreSize = 0.2  # the size of the core concrete fiber elements
    # coverSize = 0.3  # the size of the cover concrete fiber elements
    # outBarD = 0.032  # outside bar diameter
    # outBarDist = 0.2  # outside bar space
    # plotState = False  # plot the fiber or not plot=True or False
    # inBarD = 0.032  # inside bar diameter
    # inBarDist = 0.2  # inside bar space
    # coreFiber, coverFiber, barFiber = polygonSection(outSideNode, outSideEle, coverThick, coreSize, coverSize, \
    #                                                  outBarD, outBarDist, plotState, inSideNode, inSideEle, inBarD,
    #                                                  inBarDist)
    #####################################################################
    # print(help(polygonSection))






