'''A good/bad example of multiprocessing'''
import os
import multiprocessing

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import cv2
import tqdm
import pyefd

import preprocessing
import contourtools
import colors
import plottools
import segmentation


ap = preprocessing.parse_arguments()
path = ap.inpath

def imgappend(image):
    '''return contours from image path'''
    chip = cv2.imread(os.path.join(path,image))
    binary = segmentation.segment_otsu(chip)
    contours, __ = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    #temporary
    contours = [contour for contour in contours if cv2.contourArea(contour) > 1000]
    return contours

with multiprocessing.Pool(multiprocessing.cpu_count()-1) as contours_pool:
    r = list(tqdm.tqdm(contours_pool.imap(imgappend,sorted(os.listdir(path))),
                        total = len(os.listdir(path)),leave = True,
                        unit = ' imgs',desc='Image Analysis',colour=colors.to_hex(colors.MAROON)))


with multiprocessing.Pool(multiprocessing.cpu_count()-1) as analytics_pool:
    information = list(tqdm.tqdm(analytics_pool.imap(contourtools.get_metrics_list, r),
                                total= len(r), leave= True, unit= ' imgs',
                                desc = 'Shape Analysis',colour=colors.to_hex(colors.GOLD)))


ls_efd = []
#find a way to get efds as well. Probably relies on pandas multiindex
for cntlist in tqdm.tqdm(r, total = len(r), 
                            unit= ' imgs', desc='efd calculation',
                            colour = colors.to_hex(colors.LAVENDER)):
    ls_efd.append(contourtools.efd(cntlist))


df_main = pd.DataFrame()
for infolist in tqdm.tqdm(information, total = len(information),
                            unit = ' imgs', desc='Data Summation',
                            colour=colors.to_hex(colors.MAROON)):
    df = pd.DataFrame(infolist, columns = ['Surface Area', 'Perimeter','Circularity', 'Length', 'Width',
                                         'Aspect', 'dist_is_cog', 'is0', 'is1', 'cog1', 'cog2', 'm00', 'm01', 'm10', 'm11', 'n00', 'n01', 'n10', 'n11'])
    df_main = df_main.append(df)


print(f"this many in ls_efd {len(ls_efd)}")
print(f"this many is ls_efd[0]: {len(ls_efd[0])}")

numbeanstot = int(len(df_main)) # 756
numbeansperimage = int(numbeanstot/len(os.listdir(path))) # 36
numsheets = int(numbeanstot/numbeansperimage) # 21



matplotlib.rc('axes',edgecolor=f'{colors.to_hex(colors.LAVENDER)}')

for efdlist in tqdm.tqdm(range(len(ls_efd)), desc=' Saving Sheets', leave=True,unit= ' imgs', colour=colors.to_hex(colors.GOLD)):
    fig1, fig1_axes = plt.subplots(ncols = 6, nrows = 6, constrained_layout = True)
    for row in range(10):
        for column in range(10):
            currpos = row*6 + column
            ax = fig1_axes[row][column]
            ax.set_xlim(-125,125)
            ax.set_ylim(-125,125)
            yt, xt, color, linewidth = plottools.plot_efd_alt(ls_efd[efdlist][currpos])
            ax.plot(yt,xt, f"{colors.to_hex(colors.BLACK)}", linewidth)
            ax.set_aspect('equal', 'box')
            ax.get_yaxis().set_ticks([])
            ax.get_xaxis().set_ticks([])
    plt.suptitle(f"Seedlot {efdlist+1}")
    plt.savefig(os.path.join(path, f"{efdlist+1}.png"), dpi=600)
    plt.close(fig1)
