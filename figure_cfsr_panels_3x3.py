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

rcParams['xtick.direction'] = 'in'
rcParams['ytick.direction'] = 'in'

dates = [
    datetime(2003, 1, 12, 12, 0),
    datetime(2003, 1, 22, 12, 0),
    datetime(2003, 2, 15, 18, 0),
    datetime(2004, 1, 9, 12, 0),
    datetime(2004, 2, 2, 6, 0),
    datetime(2004, 2, 16, 6, 0),
    datetime(2004, 2, 25, 6, 0)
]

scale=1.2
fig = plt.figure(figsize=(8*scale, 8*scale))
grid = ImageGrid(fig, 111,
                 nrows_ncols=(3, 3),
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
cfsr.plot(ax=grid,
          field=['iwv_flux',range(250, 1500, 250)],
          contour=['thetaeq',None],
          dates=dates,
          homedir=homedir)

grid.axes_all[-1].axis('off')
grid.axes_all[-2].axis('off')

labticksize=11

yticks = grid.axes_all[0].yaxis.get_major_ticks()
yticks[0].label1.set_visible(False)
yticks[-1].label1.set_visible(False)
for tick in yticks:
    tick.label.set_fontsize(labticksize)

yticks = grid.axes_all[3].yaxis.get_major_ticks()
yticks[0].label1.set_visible(False)
yticks[-1].label1.set_visible(False)
for tick in yticks:
    tick.label.set_fontsize(labticksize)
    
yticks = grid.axes_all[6].yaxis.get_major_ticks()
yticks[0].label1.set_visible(False)
yticks[-1].label1.set_visible(False)
for tick in yticks:
    tick.label.set_fontsize(labticksize)
    
xticks = grid.axes_all[6].xaxis.get_major_ticks()
for tick in xticks:
    tick.label.set_fontsize(labticksize)

ax = grid.axes_all[0]
ax.text(0.38,0.81,'hPa',transform=ax.transAxes,rotation=-40,weight='bold')
ax.text(0.35,0.38,'K',transform=ax.transAxes,rotation=30,
        color='r',weight='bold')

    
plt.show()
#
#fname='/home/raul/Desktop/cfsr_panels.png'
#plt.savefig(fname, dpi=300, format='png',papertype='letter',
#            bbox_inches='tight')

