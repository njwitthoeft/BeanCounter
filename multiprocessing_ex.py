'''A good example of multiprocessing'''
import os
import multiprocessing

import pandas as pd
import cv2
import tqdm

import preprocessing
import contourtools
import colors


ap = preprocessing.parse_arguments()
path = ap.inpath


def imgappend(image):
    '''return contours from image path'''
    chip = cv2.imread(os.path.join(path,image))
    _, binary = cv2.threshold(chip[:,:,0], 0,255, cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(cv2.bitwise_not(binary), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    cleancontours = []
    for contour in contours:
        if cv2.contourArea(contour) > 50:
            cleancontours.append(contour)
    return cleancontours

with multiprocessing.Pool(multiprocessing.cpu_count()-1) as contours_pool:
    r = list(tqdm.tqdm(contours_pool.imap(imgappend,os.listdir(path)),
                        total = len(os.listdir(path)),leave = True,
                        unit = ' imgs',desc='Image Analysis',colour=colors.to_hex(colors.MAROON)))


with multiprocessing.Pool(multiprocessing.cpu_count()-1) as analytics_pool:
    information = list(tqdm.tqdm(analytics_pool.imap(contourtools.get_metrics_list, r),
                                total= len(r), leave= True, unit= ' imgs',
                                desc = 'Feature Extraction',colour=colors.to_hex(colors.GOLD)))


df_main = pd.DataFrame()

for infolist in tqdm.tqdm(information, total = len(information),
                            leave=True, unit = ' imgs', desc='Data Summation',
                            colour=colors.to_hex(colors.CYAN)):
    df = pd.DataFrame(infolist, columns = ['Surface Area', 'Perimeter',
                                'Major Axis', 'Minor Axis', 'Circularity', 'Length',
                                'Width', 'Aspect', 'Intersect', 'Center of Gravity', 'D_IS_COG'])
    df_main = df_main.append(df)

print(df_main[['Surface Area', 'Perimeter','Circularity', 'Length',
                                'Width', 'Aspect']].head(10).to_string())
