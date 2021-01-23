'''Generate false data for performance testing'''
import os
import cv2
import argparse

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

ap = parse_arguments()


beans = cv2.imread('beans.jpg')
cv2.imshow('Said Beans',beans)
cv2.waitKey(0)


for i in range(51):
    filepath = os.path.join(ap.inpath,str(i)+'.jpg')
    cv2.imwrite(filepath,beans)
    