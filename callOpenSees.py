#-*-coding: UTF-8-*-
import subprocess
import dmsh
import optimesh
import meshio
import matplotlib.pyplot as pt
import numpy as np


# p = subprocess.Popen("OpenSees.exe", stdin=subprocess.PIPE,
#                      stdout=subprocess.PIPE,
#                      stderr=subprocess.PIPE)
# p.stdin.write("source AnJiuCableStayedBridge.tcl\n".encode())
######################################################################################
geo = dmsh.Difference(
    dmsh.Polygon([[10, 10], [10, -10], [-10, -10],[-10,10]]),
    dmsh.Polygon([[4, 4], [4, -4], [-4, -4],[-4,4]]),
)
points,elements = dmsh.generate(geo,0.4)
pt.triplot(points[:, 0], points[:, 1], elements)
pt.show()

################################################################