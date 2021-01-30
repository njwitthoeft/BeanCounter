'''Tools to preprocess'''

import argparse
import os
import cv2
import numpy as np

from exceptions import BarcodeNotFoundError

def parse_arguments():
    '''Setup an argparse instance with -inpath, -efd, -debug'''
    parser = argparse.ArgumentParser(description='Get statistics from an image folder')
    parser.add_argument('-inpath', type=dir_path, help='input folder path')
    parser.add_argument('-efd', default=0, help='number of elliptical fourier descriptors to save')
    parser.add_argument('-debug', default=False, help='save debug images')
    return parser.parse_args()

def dir_path(string):
    '''Check for valid path'''
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)

def get_images(directory):
    '''Return image list from directory name'''
    i=0
    images = []
    for image in os.listdir(dir):
        temp_img = cv2.imread(os.path.join(directory,image))
        images.append(temp_img)
        i += 1
        print(i)
    return images

def show_images(images):
    '''Display images using cv2.imshow'''
    for image in images:
        cv2.imshow('image', image)
        cv2.waitKey(0)

def read_barcode(raw_img):
    '''Read barcode and return barcode and bar object'''
    try:
        my_bar = pyzbar.decode(raw_img)
        bar_id = my_bar.data.decode("utf-8")
    except Exception as exc:
        raise BarcodeNotFoundError from exc
    return bar_id, my_bar

#TODO: remove contour filtering once possible
def imgappend(image):
    '''return contours from image path'''
    chip = cv2.imread(os.path.join(path,image))
    binary = segmentation.segment_otsu(chip)
    contours, __ = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    #temporary
    contours = [contour for contour in contours if cv2.contourArea(contour) > 1000]
    return contours

def get_mask(barcode, image, binary, dist=750):
    (x,y,w,h) = barcode.rect

    #expand rectangle
    x1 = x - dist
    y1 = y - dist
    x2 = x + w + dist*2
    y2 = y + h + dist
    #generate mask based on barcode location
    mask = np.ones(image.shape[:2],np.uint8)
    mask[y1:y2,x1:x2] = 0
    res = cv2.bitwise_and(binary,binary, mask = mask)
    ret, res = cv2.threshold(res, 0, 255, cv2.THRESH_OTSU)
    return res

def total_bound(cnts):
    boxes = []
    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        boxes.append([x,y, x+w,y+h])

    boxes = np.asarray(boxes)
    left, top = np.min(boxes, axis=0)[:2]
    right, bottom = np.max(boxes, axis=0)[2:]
    upperleft = (left,top)
    bottomright = (right, bottom)
    return upperleft, bottomright