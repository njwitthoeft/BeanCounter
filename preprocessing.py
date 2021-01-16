'''Tools to preprocess'''

import argparse
import os
import cv2
import pyzbar
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
