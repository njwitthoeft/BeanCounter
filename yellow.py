import cv2
import numpy as np
import os
import colors
import pandas as pd
from preprocessing import parse_arguments, get_mask, total_bound
from pyzbar import pyzbar
from math import pi
from scipy.spatial.distance import pdist, squareform
import contourtools







ap = parse_arguments()

outdf = pd.DataFrame(columns=['filename','id','calibdist', 'surface_area','perim','circ', 'length', 'width', 'aspect'])
outlist = []
imlist = []
fnames = []
for f in os.listdir(ap.inpath):
    img = cv2.imread(os.path.join(ap.inpath, f))
    imlist.append(img)
    fnames.append(f)

kernel = np.ones((25,25)) 
for idx2, image in enumerate(imlist):
    colorimage=image.copy()
    x1 = 1
    y1 = 500
    x2 = 950
    y2 = 3800
    #generate 
    mask = np.ones(image.shape[:2],np.uint8)
    mask[y1:y2,x1:x2] = 0
    image_g = image[:,:,2]
    image_g = cv2.bitwise_and(image_g, image_g, mask=mask)
    blur = cv2.GaussianBlur(image_g, (25,25), 0)
    ret, binary = cv2.threshold(blur, 0, 255, cv2.THRESH_OTSU) 
    binary = cv2.erode(binary, kernel)
    binary = cv2.dilate(binary, kernel)
    show = cv2.resize(binary, None, fx = 0.25, fy = 0.25, interpolation = cv2.INTER_AREA)
    cv2.imshow('Binary', show)
    cv2.waitKey(0)
    ##more with contours
    contours, heirarchy = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    #directly filter contours
    newcontours = []
    newcontourpoints = []
    for cnt in contours:
        moment = cv2.moments(cnt)
        surface_area = moment['m00']
        perimeter = cv2.arcLength(cnt, closed = True)
        circularity = (4*pi*surface_area)/(perimeter**2)
        cX = int(moment["m10"] / moment["m00"])
        cY = int(moment["m01"] / moment["m00"])
        if(circularity < 0.8   or surface_area > 15000 or surface_area < 3000):
            pass
        else:
            newcontours.append(cnt)
            newcontourpoints.append((cX,cY))

    ## after gettinf all centroids into a safe place, filter for points which are not close to anything else,

    _d_mat = squareform(pdist(newcontourpoints))

    #get median min distance

    #find largest distance, get location of it
    
    _max = np.where(_d_mat == _d_mat.max())[0]
    maxd = _d_mat.max()
    print(f'maximum length, used for calibration {maxd}') 
    _pt1 = (newcontourpoints[_max[0]][0], newcontourpoints[_max[0]][1])
    _pt2 = (newcontourpoints[_max[1]][0], newcontourpoints[_max[1]][1])

    ##for each point, find a mean distance from all other points. 
   
    tick = 0
    maxl = 0
    for i in range(len(newcontourpoints)):
        tick += (np.mean(_d_mat[i]))
        if(np.mean(_d_mat[i]) > maxl):
            maxl=np.mean(_d_mat[i])
            
    mean = tick/len(newcontourpoints)
    print('mean: ' + str(tick/len(newcontourpoints)))
    print('max: '+ str(maxl))

   
    #print(len(newcontours))
    disp = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)
    disp = cv2.drawContours(disp, newcontours, -1, colors.MAROON, 9)
    for idx, cnt in enumerate(newcontours):
        cv2.putText(disp, str(idx), newcontourpoints[idx], cv2.FONT_HERSHEY_SIMPLEX, 3, colors.BLUE, 5 )
    
    cv2.line(disp, _pt1, _pt2, colors.CORAL, 9)
    if(maxl/mean > 1.5):
        cv2.line(disp, _pt1, _pt2, colors.BLUE, 9)
    for point in newcontourpoints:
        cv2.circle(disp, point, 7, colors.GOLD, -1)
    disp = cv2.resize(disp, None, fx = 0.25, fy = 0.25, interpolation = cv2.INTER_AREA)

    cv2.imshow('Contours', disp)
    cv2.waitKey(0)

    for idx, cnt in enumerate(newcontours):
        data = list(contourtools.get_metrics(cnt))
        meta = list([fnames[idx2], idx, maxd])
        print(data)
        print(meta)
        line = meta + data 
        outlist.append(line)


outdf = pd.DataFrame(outlist)



outdf.to_csv(r'C:\Users\njwit\Desktop\seedpreliminary.csv')
print(outdf)                 
colorimage = image.copy()

#access red channel
image_g = image[:,:,2]

#gaussian blur
blur = cv2.GaussianBlur(image_g, (25,25), 0)
ret, binary = cv2.threshold(blur, 0, 255, cv2.THRESH_OTSU)


#before showing, copy and resize
show = cv2.resize(binary, None, fx = 0.25, fy = 0.25, interpolation = cv2.INTER_AREA)

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