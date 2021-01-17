'''Test framework'''
import numpy as np
import cv2

import preprocessing
import segmentation
import contourtools
import colors

#parse arguments, load images from -inpath
ap = preprocessing.parse_arguments()
raw_images = preprocessing.get_images(ap.inpath)
binaryimages = segmentation.segment_otsu(raw_images, colormode='red')
##just grabs an image and crops to get one example contour to work with
sheet = binaryimages[1]
kernel = np.ones((9,9),np.uint8)
kernel2 = np.ones((13,13),np.uint8)
sheet = cv2.morphologyEx(sheet, cv2.MORPH_ERODE, kernel2)
sheet = cv2.morphologyEx(sheet, cv2.MORPH_DILATE, kernel)
chip = sheet[250:500,320:520]
chip = cv2.bitwise_not(chip)
contours, heirarchy = cv2.findContours(chip, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
chip = cv2.cvtColor(chip, cv2.COLOR_GRAY2BGR)
chip = cv2.drawContours(chip, contours[0], -1, colors.MAROON, 3)
contour = contours[0]

majpoints, minpoints = contourtools.get_axes(contour)

cv2.line(chip, majpoints[0], majpoints[1], colors.CYAN, 2)

cv2.imshow('Major Axis', chip)
cv2.waitKey(1)

cv2.line(chip, minpoints[0], minpoints[1], colors.CORAL, 2)


cv2.imshow('Minor too, plus a center of gravity', chip)
cv2.waitKey(0)

IS = contourtools.line_intersect(majpoints,minpoints)
dummy = contourtools.get_metrics(contour)

cv2.circle(chip, IS, 5, colors.YELLOW, -1)

cv2.imshow('minor and intersection', chip)
cv2.waitKey(0)
