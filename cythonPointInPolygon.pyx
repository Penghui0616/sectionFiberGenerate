######################################################################################
#  Author: Junjun Guo
#  E-mail: guojj@tongji.edu.cn/guojj_ce@163.com
#    Date: 05/02/2020
#  Environemet: Successfully excucted in python 3.6
######################################################################################
cimport numpy as np
import numpy as np
from libc.math cimport sqrt,atan,abs,pi
cdef bint cythonis_in_2d_polygon(list point, list vertices):
    cdef double px,py,angle_sum
    cdef int size
    cdef int j
    px = point[0]
    py = point[1]
    angle_sum = 0

    size = len(vertices)
    if size < 3:
        raise ValueError("len of vertices < 3")
    j = size - 1
    cdef int i
    cdef double sx,xy,tx,ty
    cdef double k,b,dis,angle
    for i in range(0, size):
        sx = vertices[i][0]
        sy = vertices[i][1]
        tx = vertices[j][0]
        ty = vertices[j][1]

        # y = kx + b, -y + kx + b = 0
        k = (sy - ty) / (sx - tx + 0.000000000001)
        b = sy - k * sx
        dis = abs(k * px - 1 * py + b) / sqrt(k * k + 1)
        if dis < 0.000001:
            if sx <= px <= tx or tx <= px <= sx:
                return True

        angle = atan((sy - py)/(sx - px)) - atan((ty - py)/(tx - px))
        if angle >= pi:
            angle = angle - pi * 2
        elif angle <= -pi:
            angle = angle + pi * 2

        angle_sum += angle
        j = i

    return abs(angle_sum - pi * 2) < 0.00000000001
########################################################################################
def is_in_2d_polygon(point,vertices):
    boolValue=cythonis_in_2d_polygon(point, vertices)
    return boolValue
