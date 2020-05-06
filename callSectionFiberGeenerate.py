from sectionFiberMain import circleSection,polygonSection

outSideNode = {1: (0, 0), 2: (7, 0), 3: (7, 3), 4: (0, 3)}
# the outside vertexes loop consecutively numbering in dict container
outSideEle = {1: (1, 2), 2: (2, 3), 3: (3, 4), 4: (4, 1)}
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