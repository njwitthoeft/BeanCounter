import argparse
import os
import cv2
import zbar
from exceptions import BarcodeNotFoundError

#setup an argparse instance to take the path of image folder containinh
def parse_arguments():
    parser = argparse.ArgumentParser(description='Get statistics from an image folder')
    parser.add_argument('-inpath', type=dir_path, help='input folder path')
    parser.add_argument('-efd', default=0, help='number of elliptical fourier descriptors to save, if 0 then calculate')
    parser.add_argument('-debug', default=False, help='save debug images')
    return parser.parse_args()

#check path for validity and raise error is there is an issue
def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)

def get_images(dir):
    images = []
    for image in os.listdir(dir):
        temp_img = cv2.imread(os.path.join(dir,image))
        images.append(temp_img)
    return images

def show_images(images):
    for image in images:
        cv2.imshow('image', image)
        cv2.waitKey(0)

def read_barcode(raw_img):
    try:
        bar = zbar.decode(raw_img)
        bar_id = bar.data.decode("utf-8")
    except:
        raise BarcodeNotFoundError()
    return bar_id, bar