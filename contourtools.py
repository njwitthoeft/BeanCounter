import cv2
import warnings
from numpy import where as np_where
from math import sqrt
from scipy.spatial.distance import pdist, squareform
from numba import njit
#from timeit import timeit

# def get_contours(image):
# ###contains contour methods, written in such a way that these can be easily multithreaded
# def get_aspect(cnt):
#     h,w =get_shape(cnt)

# def get_shape(cnt):
#     findMaxDistance()
#     findPerpendiculrPairs(cnt)

# def get_circularity(cnt):
#     pass

# def get_DIWxCOG(cnt):

# def get_eccentricity(cnt):

# def get_fourier(cnt):
#     py_efd


def get_major_axis(cnt):
    '''Takes in a standard cv2 contour object, returns the two points of of the line'''
    #get contour reshaped into 2d array
    cnt = cnt.reshape(-1,2)

    #create a distance matrix reflexive on the contour you pass in, convert to square form 
    d_mat = squareform(pdist(cnt))

    #find largest distance, get location of it
    max = np_where(d_mat == d_mat.max())[0]

    #get that into a set of points to return, which are the two points farthest away from each other
    point1 = (cnt[max[0]][0], cnt[max[0]][1])
    point2 = (cnt[max[1]][0], cnt[max[1]][1])
    return (point1, point2)






def get_axes(cnt):
    cnt = cnt.reshape(-1,2)
    #create a distance matrix reflexive on the contour you pass in, convert to square form 
    d_mat = squareform(pdist(cnt))

    #find largest distance, get location of it
    max = np_where(d_mat == d_mat.max())[0]

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