import plotCFSR as cfsr
from mpl_toolkits.axes_grid1 import ImageGrid
import matplotlib.pyplot as plt
from datetime import datetime

dates = [
    datetime(2003, 1, 12, 6, 0),
    datetime(2003, 1, 22, 18, 0),
    datetime(2003, 2, 15, 18, 0),
    datetime(2004, 1, 9, 12, 0),
    datetime(2004, 2, 2, 12, 0),
    datetime(2004, 2, 16, 12, 0),
    datetime(2004, 2, 25, 6, 0)
]

fig = plt.figure(figsize=(8, 8.5))
grid = ImageGrid(fig, 111,
                 nrows_ncols=(3, 3),
                 axes_pad=0,
                 add_all=True,
                 share_all=False,
                 label_mode="L",
                 cbar_location="top",
                 cbar_mode="single",
                 cbar_size='2%',
                 aspect=True)
cfsr.plot(field='thetaeq', dates=dates, ax=grid)

fig = plt.figure(figsize=(8, 8.5))
grid = ImageGrid(fig, 111,
                 nrows_ncols=(3, 3),
                 axes_pad=0,
                 add_all=True,
                 share_all=False,
                 label_mode="L",
                 cbar_location="top",
                 cbar_mode="single",
                 cbar_size='2%',
                 aspect=True)
cfsr.plot(field='iwv_flux', dates=dates, ax=grid)

fig = plt.figure(figsize=(8, 8.5))
grid = ImageGrid(fig, 111,
                 nrows_ncols=(3, 3),
                 axes_pad=0,
                 add_all=True,
                 share_all=False,
                 label_mode="L",
                 cbar_location="top",
                 cbar_mode="single",
                 cbar_size='2%',
                 aspect=True)
cfsr.plot(field='geothick', dates=dates, ax=grid)