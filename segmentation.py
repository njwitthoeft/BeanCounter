import cv2
from breakdowntools import splitImage
from exceptions import WrongColormodeError

#beans = cv2.imread('beans.jpg')

#chips = splitImage(beans)

#for chip in chips:
 #   cv2.imshow(chip)
  #  cv2.waitKey(0)
def grayscale(img, colormode = 'all'):
    if colormode == 'all':
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    elif colormode == 'blue':
        gray = img[:,:,0]
    elif colormode == 'green':
        gray = img[:,:,1]
    elif colormode == 'red':
        gray = img[:,:,2]
    else:
        raise WrongColormodeError
    return gray


def segmentOtsu(chips, colormode = 'all'):
    '''Takes in a list of image chips and returns binary images'''
    binchips = []
    for chip in chips:              
        chipg = grayscale(chip, colormode)
        _, bin = cv2.threshold(chipg, 0,255, cv2.THRESH_OTSU)
        binchips.append(bin)
    return binchips


def segmentAdaptive(chips, ngbhd = 100, offset = 10, colormode = 'all'):
    binchips = []
    for chip in chips:
        chipg = grayscale(chip, colormode)
        _, bin = cv2.adaptiveThreshold(chipg, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, ngbhd, offset)
        binchips.append(bin)
    return binchips

# def segmentManual(chips, min, max, colormode = 'all'):
#     binchips = []
#     for chipg in chips:
#         chipg = grayscale(chip, colormode)
#         _, bin = cv2.threshold(chipg, )
