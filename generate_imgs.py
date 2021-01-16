'''Generate false data for performance testing'''
import os
import cv2

beans = cv2.imread('/home/nick/Desktop/test/1.jpg')
cv2.imshow('beans',beans)
cv2.waitKey(0)


for i in range(51):
    filepath = os.path.join('/home/nick/Desktop/test2',str(i)+'.jpg')
    cv2.imwrite(filepath,beans)
    