import cv2
import numpy as np
import os
from preprocessing import parse_arguments, get_mask, total_bound
from pyzbar import pyzbar

ap = parse_arguments()

imlist = []
for f in os.listdir(ap.inpath):
    img = cv2.imread(os.path.join(ap.inpath, f))
    imlist.append(img)

#get first image in folder
image = imlist[0]

colorimage = image.copy()

#access red channel
image_g = image[:,:,2]

#gaussian blur
blur = cv2.GaussianBlur(image_g, (25,25), 0)
ret, binary = cv2.threshold(blur, 0, 255, cv2.THRESH_OTSU)


#before showing, copy and resize
show = cv2.resize(binary, None, fx = 0.45, fy = 0.45, interpolation = cv2.INTER_AREA)

#show binary
cv2.imshow('Binary', show)
cv2.waitKey(0)

#get barcode from grayscale image
barcode = pyzbar.decode(image_g)[0]

#plot barcode location
(x, y, w, h) = barcode.rect
cv2.rectangle(image, (x, y), (x+w, y+h), (255,0,0),10)

print('')
print('Barcode:')
print(barcode.data)
#resize plotted image, then show
show = cv2.resize(image, None, fx = 0.45, fy = 0.45, interpolation = cv2.INTER_AREA)
cv2.imshow('I found your code!', show)
cv2.waitKey(0)

#get a mask around barcode
maskbin = get_mask(barcode, image, binary)

#grab contours, find bounding box for all contours:
contours, _ = cv2.findContours(maskbin, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
ul, br = total_bound(contours)
cv2.rectangle(image, ul, br, (0,255,0), 15)

#resize plotted image, then show
show = cv2.resize(image, None, fx = 0.45, fy = 0.45, interpolation = cv2.INTER_NEAREST)
cv2.imshow('I found your code and I found your tray!', show)
cv2.waitKey(0)

#get subimage only containing the contours, no tray
(x1,y1) = ul
(x2,y2) = br
dist = 300

#TODO: fix the temporary patch here. won't be neccessary for a pefect image.
maskbin = maskbin[y1 + dist:y2 - dist,x1 + dist:int(x2 - dist*1.5)]
show = cv2.resize(maskbin, None, fx = 0.45, fy = 0.45, interpolation = cv2.INTER_NEAREST)
cv2.imshow('I cut your tray!', show)
cv2.waitKey(0)




#next, we need to find the barcode
#then save that barcode value as the file name
#then mask the barcode from the image.
pip