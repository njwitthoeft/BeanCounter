# import cv2
# from math import floor
# from multiprocessing import process, current_process
# from timeit import timeit



# beans = cv2.imread('beans.jpg')
# beanslist = [beans for i in range(100)]

# #####-------------------------------------------------------------------##########
# '''Takes an image, and returns that image broken down to contain only one bean '''
# def splitImage(img, numRows=10, numColumns=10):
#     h, w, _ = img.shape
#     #calculate chip dimensions
#     h_div = floor(h/numRows)
#     w_div = floor(w/numColumns)

#     chiparr = []
#     for i in range(0, numRows+1):
#         for j in range(0, numRows+1):
#             ul = i*w_div,j*h_div
#             lr = (i+1)*w_div,(j+1)*h_div
#             chip = img[ul[1]:lr[1], ul[0]:lr[0]]
#             if((chip.shape[0] < 100) or (chip.shape[1] < 100)):
#                  break
#             chiparr.append(chip)
#     return chiparr
# #####------------------------------------------------------------------###########

# splitImage(beans)







'''def splitImage(img, numRows=10, numColumns=10):

    h, w, _ = img.shape
    #calculate chip dimensions
    h_div = floor(h/numRows)
    w_div = floor(w/numColumns)

    chiparr = []
    for i in range(0, numRows+1):
        for j in range(0, numRows+1):
            chiparr.append((int(i*w_div),int(j*h_div)))
    return chiparr

    ul = i*w_div,j*h_div
    lr = (i+1)*w_div,(j+1)*h_div
#             chip = img[ul[1]:lr[1], ul[0]:lr[0]]
#             if((chip.shape[0] < 100) or (chip.shape[1] < 100)):
#                  break
#             chiparr.append(chip)
def getUpperLeftCorners(img, numRows=10, numColumns=10):
    h, w, _ = img.shape
    #calculate chip dimensions
    h_div = floor(h/numRows)
    w_div = floor(w/numColumns)

    chiparr = []
    for i in range(0, numRows+1):
        for j in range(0, numRows+1):
            chiparr.append((int(i*w_div),int(j*h_div)))
    return chiparr

 getUpperLeftCorners(beans)'''
 