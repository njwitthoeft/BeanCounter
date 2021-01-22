import cv2
import numpy
import os
from preprocessing import parse_arguments

ap = parse_arguments()

imlist = []
for f in os.listdir(ap.inpath):
    img = cv2.imread(os.path.join(ap.inpath, f))
    imlist.append(img)

for i in imlist:
    cv2.imshow('Test', i)