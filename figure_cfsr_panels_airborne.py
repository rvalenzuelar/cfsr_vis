# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 13:46:59 2016

@author: raul
"""

'''
    Plot CFSR analyses for given dates
    
    Raul Valenzuela
    raul.valenzuela@colorado.edu

'''


import plotCFSR as cfsr
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid
from datetime import datetime
from matplotlib import rcParams

rcParams['axes.labelsize'] = 15
rcParams['xtick.labelsize'] = 15
rcParams['ytick.labelsize'] = 15
rcParams['xtick.direction'] = 'in'
rcParams['ytick.direction'] = 'in'

#dates = [
#    datetime(2001, 1, 23, 12, 0),
#    datetime(2001, 1, 23, 18, 0),
#    datetime(2001, 1, 24, 0, 0),
#    datetime(2001, 1, 24, 6, 0),
#    datetime(2001, 1, 24, 12, 0),
#    datetime(2001, 1, 24, 18, 0),
#]

#dates = [
#    datetime(2001, 2, 17, 6, 0),
#    datetime(2001, 2, 17, 12, 0),
#    datetime(2001, 2, 17, 18, 0),
#    datetime(2001, 2, 18, 0, 0),
#    datetime(2001, 2, 18, 6, 0),
#    datetime(2001, 2, 18, 12, 0),
#]

dates = [
    datetime(2001, 1, 23, 12, 0),
    datetime(2001, 1, 23, 18, 0),
    datetime(2001, 1, 24, 0, 0),
    datetime(2001, 2, 17, 12, 0),
    datetime(2001, 2, 17, 18, 0),
    datetime(2001, 2, 18, 0, 0),
]


scale=1.3
fig = plt.figure(figsize=(8*scale, 8*scale))
grid = ImageGrid(fig, 111,
                 nrows_ncols=(2, 3),
                 axes_pad=0,
                 add_all=True,
                 share_all=True,
                 label_mode="L",
                 cbar_location="top",
                 cbar_mode="single",
                 cbar_size='2%',
                 aspect=True)

# homedir = '/media/raul/RauLdisk'
#homedir = '/Volumes/RauLdisk'
homedir = '/localdata'
cf = cfsr.plot(ax=grid,
          field=['iwv_flux',range(250, 1500, 250)],
          contour=['thetaeq',range(304, 340, 2)],
          dates=dates,
          homedir=homedir)


grid[1].text(0.5,1.1,cf.title,transform=grid[1].transAxes,
            ha='center',va='bottom',fontsize=15)

for n in [0,3]:
    yticks = grid.axes_all[n].yaxis.get_major_ticks()
    yticks[0].label1.set_visible(False)
    yticks[-1].label1.set_visible(False)

for n in [3,4,5]:
    xticks = grid.axes_all[n].xaxis.get_major_ticks()
    for p in range(0,len(xticks),2):
        xticks[p].label1.set_visible(False)


ax = grid.axes_all[0]
ax.text(0.54,0.83,'hPa',transform=ax.transAxes,rotation=24,weight='bold')
ax.text(0.40,0.28,'K',transform=ax.transAxes,rotation=25,
        color='r',weight='bold')

    
#plt.show()

fname='/home/raul/Desktop/cfsr_panels_airborne.png'
plt.savefig(fname, dpi=300, format='png',papertype='letter',
            bbox_inches='tight')

