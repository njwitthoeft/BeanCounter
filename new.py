import cv2
import numpy as np
import os
from preprocessing import parse_arguments

ap = parse_arguments()

imlist = []
for f in os.listdi


image = imlist[0].copy()r(ap.inpath):
    img = cv2.imread(os.path.join(ap.inpath, f))
    imlist.append(img)


cv2.adaptiveThreshold()


# convert the input image into 
# grayscale color space 
operatedImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 

  
# modify the data type 
# setting to 32-bit floating point 
operatedImage = np.float32(operatedImage) 
  
# apply the cv2.cornerHarris method 
# to detect the corners with appropriate 
# values as input parameters 
dest = cv2.cornerHarris(operatedImage, 21, 31, 0.07) 
  
# Results are marked through the dilated corners 
dest = cv2.dilate(dest, None) 
  
# Reverting back to the original image, 
# with optimal threshold value 
image[dest > 0.01 * dest.max()]=[0, 0, 255] 
  
# the window showing output image with corners 
cv2.imshow('Corners',image)
cv2.waitKey(0)


image = imlist[0]

gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

##shi thomasi

corners = cv2.goodFeaturesToTrack(gray_img,4,0.1,1000)

for i in corners:
    x,y, = i.ravel()
    cv2.circle(image, (x,y), 3, (255,0,0), -1)

cv2.imshow('Corner Idea', image)
cv2.waitKey(0)