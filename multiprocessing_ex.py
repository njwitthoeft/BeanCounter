'''A good example of multiprocessing'''
import os
import multiprocessing
from math import sqrt
import time

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import cv2
import tqdm
from pyefd import plot_efd


import preprocessing
import contourtools
import colors
import plottools


ap = preprocessing.parse_arguments()
path = ap.inpath


def imgappend(image):
    '''return contours from image path'''
    chip = cv2.imread(os.path.join(path,image))
    _, binary = cv2.threshold(chip[:,:,0], 0,255, cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(cv2.bitwise_not(binary), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    cleancontours = []
    for contour in contours:
        if cv2.contourArea(contour) > 1000:
            cleancontours.append(contour)
    return cleancontours


with multiprocessing.Pool(multiprocessing.cpu_count()-1) as contours_pool:
    r = list(tqdm.tqdm(contours_pool.imap(imgappend,sorted(os.listdir(path))),
                        total = len(os.listdir(path)),leave = True,
                        unit = ' imgs',desc='Image Analysis',colour=colors.to_hex(colors.MAROON)))


with multiprocessing.Pool(multiprocessing.cpu_count()-1) as analytics_pool:
    information = list(tqdm.tqdm(analytics_pool.imap(contourtools.get_metrics_list, r),
                                total= len(r), leave= True, unit= ' imgs',
                                desc = 'Shape Analysis',colour=colors.to_hex(colors.GOLD)))


print(information)



# df_test = pd.DataFrame(information, columns = ['Surface Area', 'Perimeter',
#                                 'Major Axis', 'Minor Axis', 'Circularity', 'Length',
#                                 'Width', 'Aspect', 'Intersect', 'Center of Gravity', 'D_IS_COG', 
#                                 'EFD'])

# print(df_test.head(5))


df_main = pd.DataFrame()
for infolist in tqdm.tqdm(information, total = len(information),
                            leave=True, unit = ' imgs', desc='Data Summation',
                            colour=colors.to_hex(colors.MAROON)):
    df = pd.DataFrame(infolist, columns = ['Surface Area', 'Perimeter',
                                'Major Axis', 'Minor Axis', 'Circularity', 'Length',
                                'Width', 'Aspect', 'Intersect', 'Center of Gravity', 'D_IS_COG', 
                                'EFD'])
    df_main = df_main.append(df)



numbeanstot = int(len(df_main['EFD']))
numbeansperimage = int(numbeanstot/len(os.listdir(path)))
numsheets = int(numbeanstot/numbeansperimage)

#print(numbeanstot) #756
#print(numbeansperimage) #36
#print(numsheets) # 21
sheets = []
matplotlib.rc('axes',edgecolor=f'{colors.to_hex(colors.LAVENDER)}')

for sheet in tqdm.tqdm(range(numsheets), desc=' Saving Sheets', leave=True,unit= ' imgs', colour=colors.to_hex(colors.GOLD)) :
    fig1, fig1_axes = plt.subplots(ncols = 6, nrows = 6, constrained_layout = True)
    bot = sheet*numbeansperimage
    top = (sheet+1)*numbeansperimage
    list_a = df_main['EFD'][bot:top]
    for row in range(6):
        for column in range(6):
            currpos = row*6 + column
            ax = fig1_axes[row][column]
            ax.set_xlim(-125,125)
            ax.set_ylim(-125,125)
            yt, xt, color, linewidth = plottools.plot_efd_alt(list_a[currpos])
            ax.plot(yt,xt, f"{colors.to_hex(colors.BLACK)}", linewidth)
            ax.set_aspect('equal', 'box')
            ax.get_yaxis().set_ticks([])
            ax.get_xaxis().set_ticks([])
    plt.suptitle(f"Seedlot {sheet+1}")
    plt.savefig(os.path.join(path, f"{sheet+1}.png"), dpi=600)
    plt.close(fig1)
