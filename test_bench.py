import numpy as np
import cv2
from datetime import datetime

import preprocessing
import segmentation
import contourtools
import colors

b4 = datetime.now()
#parse arguments, load images from -inpath
ap = preprocessing.parse_arguments()
raw_images = preprocessing.get_images(ap.inpath)
#for img in raw_images:
#    img = cv2.GaussianBlur(img, (101,101), 1)
#preprocessing.read_barcode(raw_images[1])
#preprocessing.show_images(raw_images)
binaryimages = segmentation.segmentOtsu(raw_images, colormode='red')
linecolor = colors.FIVETHIRTYEIGHT_BLUE
contourcolor = colors.FIVETHIRTYEIGHT_GRAY


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
#cv2.imshow('contour', dilated2)
#cv2.waitKey(1)
contour = contours[0]

majpoints, minpoints = contourtools.get_axes(contour)
cog = contourtools.get_COG(contour)

cv2.line(dilated2, majpoints[0], majpoints[1], colors.CYAN, 2)

cv2.imshow('Major Axis', dilated2)
cv2.waitKey(1)
#print(majpoints)
#print(minpoints)

cv2.line(dilated2, minpoints[0], minpoints[1], colors.CORAL, 2)
cv2.putText(dilated2, text="c", org=cog,
            fontFace= cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=colors.GOLD,
            thickness=1, lineType=cv2.LINE_AA)

cv2.imshow('Minor too, plus a center of gravity', dilated2)
cv2.waitKey(0)

IS = contourtools.line_intersect(majpoints,minpoints)
dummy = contourtools.get_metrics(contour)

cv2.circle(dilated2, IS, 5, colors.YELLOW, -1)

cv2.imshow('minor and intersection', dilated2)
cv2.waitKey(0)

#print(dummy)

b4 = datetime.now()

contourtools.get_metrics(contour)

after = datetime.now()

diff = after - b4

print(str(diff))