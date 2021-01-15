import preprocessing
import segmentation
import numpy as np
import cv2
from scipy.spatial.distance import pdist, squareform

#parse arguments, load images from -inpath
ap = preprocessing.parse_arguments()
raw_images = preprocessing.get_images(ap.inpath)
for img in raw_images:
    img = cv2.GaussianBlur(img, (301,301), 1)
#preprocessing.read_barcode(raw_images[1])
#preprocessing.show_images(raw_images)
binaryimages = segmentation.segmentOtsu(raw_images, colormode='red')


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
dilated2 = cv2.drawContours(dilated, contours[0], -1, (0,255,0), 3)
cv2.imshow('contour', dilated2)
cv2.waitKey(0)


#ncoord = np.array(contours[0], contours[0])

# print(contours[0][0][0])

d = pdist(contours[0])

#print(d)
for i in contours[0]:
    print(i[0])
    print(type(i[0])