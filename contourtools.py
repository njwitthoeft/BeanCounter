'''Manipulation of OpenCV contours'''
from math import sqrt, pi, dist

import cv2
import numpy as np

from scipy.spatial.distance import pdist, squareform
from numba import njit
from pyefd import elliptic_fourier_descriptors




# def get_fourier(cnt):

def get_metrics_list(cntlist):
    '''takes in a list and provides functions'''
    metriclist = []
    for contour in cntlist:
        metriclist.append(get_metrics(contour))
    return metriclist

def get_metrics(cnt, efd = True):
    '''takes in contour, coordinates getting metrics while saving compute time'''
    #first, get moments
    moment = cv2.moments(cnt)
    surface_area = moment['m00']
    perimeter = cv2.arcLength(cnt, closed = True)
    major, minor = get_axes(cnt)
    circularity = (4*pi*surface_area)/(perimeter**2)
    length = dist(major[0],major[1])
    width = dist(minor[0],minor[1])
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
    if efd:
        efd = elliptic_fourier_descriptors(np.squeeze(cnt), order=10)

    else:
        efd = [-1 for i in 10]
    #cv2.waitKey(0)

    return [surface_area, perimeter, major, minor, circularity,
            length, width, aspect, intersect, cog, dist_is_cog, efd]


def get_axes(cnt):
    '''Numpy finds farthest points, numba speeds up the minor axis'''
    cnt = cnt.reshape(-1,2)
    #create a distance matrix reflexive on the contour you pass in, convert to square form
    d_mat = squareform(pdist(cnt))

    #find largest distance, get location of it
    _max = np.where(d_mat == d_mat.max())[0]

    #make points for major axis
    pt1 = (cnt[_max[0]][0], cnt[_max[0]][1])
    pt2 = (cnt[_max[1]][0], cnt[_max[1]][1])
    majorpoints = (pt1,pt2)
    minorpoints = core_minor_axis(cnt,_max)

    return majorpoints, minorpoints


@njit
def core_minor_axis(cnt, _max):
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
            #print(minslope)
            if minslope < -1/(majslope) + 0.001:
                if minslope > -1/(majslope) - 0.001:
                    pointa = (point1[0], point1[1])
                    pointb = (point2[0], point2[1])
                    # replace dist with a homemade function, so numba can translate to get speedup
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
        return None
    if not(0 <= u_a <= 1 and 0 <= u_b <= 1):
        return None
    _x = int(ax_1 + u_a * (ax_2 - ax_1))
    _y = int(ay_1 + u_a * (ay_2 - ay_1))

    return (_x,_y)
