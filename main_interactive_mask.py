
#standard imports
from math import pi
import os
import fnmatch

#open-source libraries
import cv2
import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist, squareform
from pyzbar import pyzbar
from tqdm import tqdm

#my libraries, each corresponds to a file in the project
from preprocessing import parse_arguments, get_mask, total_bound
import contourtools
import colors


#parse command line to find input folder, this is the -inpath "/PATHGOESHERE" argument
ap = parse_arguments()

#make three empty lists
#stores data about contours
outlist = []

#stores the actual image, in memory
imlist = []

#stores the filename of the image
fnames = []
##########



#for each image in the directory, add the image to one list and the file name to another
for f in tqdm(fnmatch.filter(os.listdir(ap.inpath), "*.jpg"), desc = "Loading Images"):
    img = cv2.imread(os.path.join(ap.inpath, f))
    imlist.append(img)
    fnames.append(f)

#set a kernelm, this will be used for morphological operations
kernel = np.ones((25,25))

############################################################################
###interactive masking feature, should be moved to its own module eventually
refPt = []
masking = False



def click_and_mask(event, x, y, flags, param):
    global refPt, masking, image

    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x,y)]
        masking = True

    elif event == cv2.EVENT_LBUTTONUP:
        refPt.append((x,y))
        masking = False
        cv2.rectangle(image, refPt[0], refPt[1], colors.GREEN, 2)
        cv2.imshow("Click and Drag to Select Mask, press M to confirm, press R to reset", image)
###############################################################################
# load the image, clone it, and setup the mouse callback function
if ap.mask:
    image = cv2.resize(imlist[0].copy(), None, fx = 0.25, fy = 0.25, interpolation = cv2.INTER_AREA)
    clone = image.copy()
    cv2.namedWindow("Click and Drag to Select Mask, press M to confirm, press R to reset")
    cv2.setMouseCallback("Click and Drag to Select Mask, press M to confirm, press R to reset", click_and_mask)
    # keep looping until the 'q' key is pressed
    while True:
        # display the image and wait for a keypress
        cv2.imshow("Click and Drag to Select Mask, press M to confirm, press R to reset", image)
        key = cv2.waitKey(1) & 0xFF
        # if the 'r' key is pressed, reset the cropping region
        if key == ord("r"):
            image = clone.copy()
        # if the 'm' key is pressed, break from the loop
        elif key == ord("m"):
            break
    # if there are two reference points, then crop the region of interest
    # from teh image and display it
    if len(refPt) == 2:
        # instead of cropping, use the coords to make a mask, note the trasnformation needed to scale to full size images
        mask = np.ones(image.shape[:2],np.uint8)
        mask[refPt[0][1]:refPt[1][1],refPt[0][0]:refPt[1][0]] = 0
        mask = cv2.bitwise_not(mask*255) 
        image_gray = image[:,:,2]
        image_gray = cv2.bitwise_and(image_gray, image_gray, mask=mask)

        cv2.imshow("Masked Image", image_gray)
        cv2.waitKey(0)
    # close all open windows
    cv2.destroyAllWindows()
    gmask = cv2.resize(mask, None, fx = 4, fy = 4, interpolation = cv2.INTER_NEAREST)

else:
    pass
###now we have a valid mask which we will use for all of the above



#######################################################################################

#for each image in the image list
for idx2, image in enumerate(tqdm(imlist, desc = 'Manual Inspection')):
   
    colorimage=image.copy()
   
    #select only the red channel of the image, use that as a greyscale
    image_g = image[:,:,2]

    #blur the image
    image_g = cv2.GaussianBlur(image_g, (25,25), 0)
    #use otsu's thresholding to automatically binarize the image
    _ , binary = cv2.threshold(image_g, 0, 255, cv2.THRESH_OTSU) 

    #now use morph operations to simplify the shapes
    binary = cv2.erode(binary, kernel)
    binary = cv2.dilate(binary, kernel)


    #mask the binary
    binary = cv2.bitwise_and(binary, binary, mask=gmask)
    #make a smaller image to show the results, this is an optional stepa dn should be a cli option
    #show = cv2.resize(binary, None, fx = 0.25, fy = 0.25, interpolation = cv2.INTER_AREA)
    #cv2.imshow('Binary', show)
    #cv2.waitKey(0)
    
    #find all contours in the image
    contours, heirarchy = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    
    #filter contours by their properties
    newcontours = []
    newcontourpoints = []
    for cnt in contours:
        moment = cv2.moments(cnt)
        surface_area = moment['m00']
        perimeter = cv2.arcLength(cnt, closed = True)
        circularity = (4*pi*surface_area)/(perimeter**2)
        #this is the center point
        try:
            cX = int(moment["m10"] / moment["m00"])
            cY = int(moment["m01"] / moment["m00"])
        except Exception:
            cX = 1
            cY = 1
        if(circularity < 0.8   or surface_area > 15000 or surface_area < 3000):
            #if any of the following apply, do not add to the "good" contours list
            pass
        
        else:
            newcontours.append(cnt)
            newcontourpoints.append((cX,cY))

    #now ignoring the contours and workign with the contour centroids
    #this creates a matrix of pariwise distances for each point
    _d_mat = squareform(pdist(newcontourpoints))
    
    #gets points where pairwise distance is longest
    _max = np.where(_d_mat == _d_mat.max())[0]
    #gets the actual distance between farthest pairwise points
    maxd = _d_mat.max()

    #save point one and two to be able to plot them later
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

    #there us a cool property where the ratio of the max to the mean is consistent for
    #correctly segmented images but is larger for incorrectly processed images
   

    # make an image for display, first put it in color
    disp = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)
    #then put all the contours on the display image
    disp = cv2.drawContours(disp, newcontours, -1, colors.MAROON, 9)
    
    #then label each imaage with the contour numbers
    for idx, cnt in enumerate(newcontours):
        cv2.putText(disp, str(idx), newcontourpoints[idx], cv2.FONT_HERSHEY_SIMPLEX, 3, colors.BLUE, 5 )

    #put a coral line between the two furthest points
    cv2.line(disp, _pt1, _pt2, colors.CORAL, 9)
    
    #use the cool property to determine if the image has issues
    if(maxl/mean > 1.5):
        #if it does, put a red line over the coral line
        cv2.line(disp, _pt1, _pt2, colors.RED, 9)

    #for each contour, put a center point in the contour
    for point in newcontourpoints:
        cv2.circle(disp, point, 7, colors.GOLD, -1)

    #make the display image quarter-sized, then show the image    
    disp = cv2.resize(disp, None, fx = 0.25, fy = 0.25, interpolation = cv2.INTER_AREA)
    cv2.imshow('Contours', disp)
    cv2.waitKey(0)
    if ap.debug:
        if(not os.path.exists(os.path.join( ap.inpath, "debug"))):
            os.mkdir(os.path.join(ap.inpath, "debug"))
        cv2.imwrite(os.path.join(ap.inpath, "debug", f"{fnames[idx2][:-4]}_debug.jpg"),disp)


    # using the new contours that we just displayed, make a list of properties
    # then add that list to the list of good contours
    for idx, cnt in enumerate(newcontours):
        data = list(contourtools.get_metrics(cnt))
        meta = list([fnames[idx2], idx, maxd])            
        line = meta + data 
        outlist.append(line)

#convert the list of lists to a datafreame
outdf = pd.DataFrame(outlist, columns=['filename','id','calibdist',
                            'surface_area','perim','circ',
                            'length', 'width', 'aspect'])
#save the dataframe as a csv in an appropriate path
outdf.to_csv(f"{os.path.join(ap.inpath, r'results.csv')}", index=False)