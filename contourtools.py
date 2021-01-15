import cv2
import numpy as np
from math import sqrt, pi, dist
from scipy.spatial.distance import pdist, squareform
from numba import njit



# def get_fourier(cnt):

def get_metrics(cnt):
    '''takes in contour, coordinates getting metrics while saving compute time by not calling cv2.moments more than once'''
    #first, get moments
    M = cv2.moments(cnt)
    surface_area = M['m00']
    perimeter = cv2.arcLength(cnt, closed = True)
    major, minor = get_axes(cnt)
    circularity = (4*pi*surface_area)/(perimeter**2)
    length = dist(major[0],major[1])
    width = dist(minor[0],minor[1])
    aspect = length/width
    intersect = line_intersect(major, minor)
    cog = ((int(M['m10']/M['m00'])),(int(M['m01']/M['m00'])))
    dist_is_cog = dist(intersect, cog)

    return [surface_area, perimeter, major, minor, circularity, length, width, aspect, intersect, cog, dist_is_cog]






#     py_efd
def get_circularity(cnt,area,perim):
    return (4*pi*area)/(perim**2)

def get_COG(cnt):
    M = cv2.moments(cnt)
    cx= int(M['m10']/M['m00'])
    cy= int(M['m01']/M['m00'])
    return (cx,cy)


def get_axes(cnt):
    cnt = cnt.reshape(-1,2)
    #create a distance matrix reflexive on the contour you pass in, convert to square form 
    d_mat = squareform(pdist(cnt))

    #find largest distance, get location of it
    max = np.where(d_mat == d_mat.max())[0]

    #make points for major axis
    pt1 = (cnt[max[0]][0], cnt[max[0]][1])
    pt2 = (cnt[max[1]][0], cnt[max[1]][1])
    majorpoints = (pt1,pt2)
    minorpoints = core_minor_axis(cnt,max)

    return majorpoints, minorpoints


@njit
def core_minor_axis(cnt, max):
    pt1 = (cnt[max[0]][0], cnt[max[0]][1])
    pt2 = (cnt[max[1]][0], cnt[max[1]][1])
    points = (pt1,pt2)
    num = (points[1][1] - points[0][1])
    div = (points[1][0] - points[0][0])
    if div != 0:
        majslope = -1*(num)/(div)
    else:
        majslope = 0
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
                minslope = 0
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
    Ax1 = line1[0][0]
    Ay1 = line1[0][1]
    Ax2 = line1[1][0]
    Ay2 = line1[1][1]

    Bx1 = line2[0][0]
    By1 = line2[0][1]
    Bx2 = line2[1][0]
    By2 = line2[1][1]

    d = (By2 - By1) * (Ax2 - Ax1) - (Bx2 - Bx1) * (Ay2 - Ay1)
    if d:
        uA = ((Bx2 - Bx1) * (Ay1 - By1) - (By2 - By1) * (Ax1 - Bx1)) / d
        uB = ((Ax2 - Ax1) * (Ay1 - By1) - (Ay2 - Ay1) * (Ax1 - Bx1)) / d
    else:
        return
    if not(0 <= uA <= 1 and 0 <= uB <= 1):
        return
    x = int(Ax1 + uA * (Ax2 - Ax1))
    y = int(Ay1 + uA * (Ay2 - Ay1))
 
    return (x,y)