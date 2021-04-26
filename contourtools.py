'''Manipulation of OpenCV contours'''
from math import sqrt, pi

import cv2
import numpy as np

from scipy.spatial.distance import pdist, squareform
from numba import njit


def get_metrics_list(cntlist):
    return [get_metrics(cnt) for cnt in cntlist]

def get_metrics(cnt):
    '''takes in contour, coordinates getting metrics while saving compute time
        
        :param list[tuples] cnt: ''A cv2 or scikit-image contour'''
    #first, get moments
    moment = cv2.moments(cnt)
    surface_area = moment['m00']
    perimeter = cv2.arcLength(cnt, closed = True)
    major, minor = get_axes(cnt)
    circularity = (4*pi*surface_area)/(perimeter**2)
    pointa = major[0]
    pointb = major[1]
    length = sqrt(((pointa[0] - pointb[0])**2) + ((pointa[1] - pointb[1])**2))
    # length = dist(major[0],major[1])
    pointa = minor[0]
    pointb = minor[1]
    width = sqrt(((pointa[0] - pointb[0])**2) + ((pointa[1] - pointb[1])**2))
    #width = dist(minor[0],minor[1])
    aspect = length/width if width != 0 else -1
    intersect = line_intersect(major, minor)
    try:
        cog = ((int(moment['m10']/moment['m00'])),(int(moment['m01']/moment['m00'])))
    except:
        cog = (1, 1)
    try:
        dist_is_cog = dist(intersect, cog)
    except: 
        dist_is_cog = 0.0

    arr = [surface_area, perimeter, circularity, length, width, aspect]
                #intersect[0], intersect[1], cog[0], cog[1], major[0][0], major[0][1], major[1][0], major[1][1],
                #minor[0][0], minor[0][1], minor[1][0], minor[1][1]]
    
    return arr

def get_axes(cnt):
    '''Numpy finds farthest points, numba speeds up the minor axis'''
    cnt = cnt.reshape(-1,2)

    #create a distance matrix reflexive on the contour you pass in, convert to square form
    _d_mat = squareform(pdist(cnt))

    #find largest distance, get location of it
    _max = np.where(_d_mat == _d_mat.max())[0]

    #make points for major axis
    _pt1 = (cnt[_max[0]][0], cnt[_max[0]][1])
    _pt2 = (cnt[_max[1]][0], cnt[_max[1]][1])

    majorpoints = (_pt1,_pt2)
    minorpoints = minor_axis(cnt,_max)

    return majorpoints, minorpoints


@njit
def minor_axis(cnt, _max):
    '''seems verbose, but allows numba to run in nopython, speedind this up a lot'''
    pt1 = (cnt[_max[0]][0], cnt[_max[0]][1])
    pt2 = (cnt[_max[1]][0], cnt[_max[1]][1])
    points = (pt1,pt2)
    num = (points[1][1] - points[0][1])
    div = (points[1][0] - points[0][0])

    if div != 0:
        majslope = -1*(num)/(div)
    else:
        majslope = 10000

    maxdist = 0
    maxp1 = (0,0)
    maxp2 = (0,0)

    for point1 in cnt:

        for point2 in cnt:
            min_num = (point2[1] - point1[1])
            min_div = (point2[0] - point1[0])

            if min_div != 0:
                minslope = -1*(min_num)/(min_div)
            else:
                minslope = 10000

            if minslope < -1/(majslope) + 0.01:

                if minslope > -1/(majslope) - 0.01:
                    pointa = (point1[0], point1[1])
                    pointb = (point2[0], point2[1])

                    # numba has no translation for math.dist, but does for math.sqrt
                    distance = sqrt(((pointa[0] - pointb[0])**2) + ((pointa[1] - pointb[1])**2))

                    if distance > maxdist:
                        maxdist = distance
                        maxp1 = pointa
                        maxp2 = pointb

    return (maxp1,maxp2)


def line_intersect(line1,line2):
    """ returns a (x, y) tuple or None if there is no intersection """
    ax_1 = line1[0][0]
    ay_1 = line1[0][1]
    ax_2 = line1[1][0]
    ay_2 = line1[1][1]

    bx_1 = line2[0][0]
    by_1 = line2[0][1]
    bx_2 = line2[1][0]
    by_2 = line2[1][1]

    _d = (by_2 - by_1) * (ax_2 - ax_1) - (bx_2 - bx_1) * (ay_2 - ay_1)
    if _d:
        u_a = ((bx_2 - bx_1) * (ay_1 - by_1) - (by_2 - by_1) * (ax_1 - bx_1)) / _d
        u_b = ((ax_2 - ax_1) * (ay_1 - by_1) - (ay_2 - ay_1) * (ax_1 - bx_1)) / _d
    else:
        return (-1,-1)
    if not(0 <= u_a <= 1 and 0 <= u_b <= 1):
        return (-1,-1)
    _x = int(ax_1 + u_a * (ax_2 - ax_1))
    _y = int(ay_1 + u_a * (ay_2 - ay_1))

    return (_x,_y)
