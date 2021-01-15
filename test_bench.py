import preprocessing
import segmentation
import contourtools
import numpy as np
from datetime import datetime
from math import dist
import cv2
from scipy.spatial.distance import pdist, squareform
from timeit import timeit

import colors

#parse arguments, load images from -inpath
ap = preprocessing.parse_arguments()
raw_images = preprocessing.get_images(ap.inpath)
for img in raw_images:
    img = cv2.GaussianBlur(img, (301,301), 1)
#preprocessing.read_barcode(raw_images[1])
#preprocessing.show_images(raw_images)
binaryimages = segmentation.segmentOtsu(raw_images, colormode='red')
linecolor = (255,0,0)
contourcolor = (0,255,0)


##just grabs an image and crops to get one example contour to work with
test = binaryimages[1]
kernel = np.ones((9,9),np.uint8)
kernel2 = np.ones((13,13),np.uint8)
eroded = cv2.morphologyEx(test, cv2.MORPH_ERODE, kernel2)
dilated = cv2.morphologyEx(eroded, cv2.MORPH_DILATE, kernel)
dilated = dilated[250:500,320:520]
dilated = cv2.bitwise_not(dilated)
contours, heirarchy = cv2.findContours(dilated, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
dilated = cv2.cvtColor(dilated, cv2.COLOR_GRAY2BGR)
dilated2 = cv2.drawContours(dilated, contours[0], -1, contourcolor, 3)
cv2.imshow('contour', dilated2)
cv2.waitKey(1)


#ncoord = np.array(contours[0], contours[0])

   


# print(contours[0][0][0])

#print(contours[0].shape)

#contours
contour = contours[0]

# print(contour.shape)

#contour = contour.reshape(-1,2)











    

#points = contourtools.get_major_axis(contour)



#print(contourtools.get_minor_axis(contour))

#d_mat = squareform(pdist(contour))
#max = np.where(d_mat == d_mat.max())[0]

b4 = datetime.now()

for i in range(10001):
    majpoints, minpoints = contourtools.get_axes(contour)


after = datetime.now()

diff = after - b4

print(diff/10000)




cv2.line(dilated2, majpoints[0], majpoints[1], linecolor, 3)

cv2.imshow('Major Axis', dilated2)
cv2.waitKey(1)
#print(majpoints)
#print(minpoints)

cv2.line(dilated2, minpoints[0], minpoints[1], linecolor, 3)

cv2.imshow('Minor too', dilated2)
cv2.waitKey(0)