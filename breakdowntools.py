import cv2

beans = cv2.imread('beans.jpg')


'''Takes an image, and returns that image broken down to contain only one bean '''
def splitImage(img, numRows=10, numColumns=0):
    h, w, _ = img.shape

    #calculate the grid points by starting with the
    h_div = int(h/10)
    w_div = int(w/10)

    rects = []
    #create list of rectangle definitions ehhhhhhhhhhh
    for i in range(0, numRows):
        for j in range(0, numRows):
            ul = i*w_div,j*h_div
            lr = (i+1)*w_div,j+1*h_div
            try:
                chip = img[ul[1]:lr[1], ul[0],lr[0]]
            except:
                chip = img[ul[1]:h, ul[0]:w]
            cv2.imshow(chip)
            cv2.waitKey(0)
            rects.append((upperleft,lowerright))


    #in order to calculate the dividing lines, 
    #you can create the side grid points and contruct them using a nested for loop



splitImage(beans, 5, 5)