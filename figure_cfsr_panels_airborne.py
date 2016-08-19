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

''' set tile '''
title  = 'Integrated water vapor transport $[kg m^{-1} s^{-1}]$\n '
title += 'Mean sea level pressure [hPa]\n'
title += 'Equivalent potential temperature [K] at 1000 hPa'

# homedir = '/media/raul/RauLdisk'
#homedir = '/Volumes/RauLdisk'
homedir = '/localdata'
cf = cfsr.plot(ax     = grid,
              field   = ['iwv_flux',range(250, 1500, 250)],
              contour = ['thetaeq',range(304, 340, 2)],
              dates   = dates,
              homedir = homedir,
              title   = '')

''' add title at correct position '''
ax = grid.axes_all[1]
ax.text(0.5,1.2,title,ha='center',
        transform=ax.transAxes)

''' adjust y and x labels '''
for n in [0,3]:
    yticks = grid.axes_all[n].yaxis.get_major_ticks()
    yticks[0].label1.set_visible(False)
    yticks[-1].label1.set_visible(False)

for n in [3,4,5]:
    xticks = grid.axes_all[n].xaxis.get_major_ticks()
    for p in range(0,len(xticks),2):
        xticks[p].label1.set_visible(False)

axes = grid.axes_all[::3]
for ax in axes:
    yticks = ax.yaxis.get_major_ticks()
    yticks[0].label1.set_visible(False)
    yticks[-1].label1.set_visible(False)
    ylabs = [str(n)+'$^\circ$' for n in range(20,55,5)]
    ylabs[-1] = ylabs[-1]+'N'
    ax.set_yticklabels(ylabs)
    for tk in yticks:
        tk.label1.set_rotation(90)    
    xticks = ax.xaxis.get_major_ticks()
    xlabs = [str(n)+'$^\circ$' for n in range(150,115,-5)]
    xlabs[1] = xlabs[1]+'W'
    ax.set_xticklabels(xlabs)


''' add units to some contours '''
ax = grid.axes_all[0]
ax.text(0.54,0.83,'hPa',transform=ax.transAxes,rotation=24,weight='bold')
ax.text(0.40,0.28,'K',transform=ax.transAxes,rotation=25,
        color='r',weight='bold')

    
#plt.show()

fname='/home/raul/Desktop/fig_cfsr_panels_airborne.png'
plt.savefig(fname, dpi=300, format='png',papertype='letter',
            bbox_inches='tight')

