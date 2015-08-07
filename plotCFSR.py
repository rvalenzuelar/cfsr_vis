

from netCDF4 import Dataset
from mpl_toolkits.axes_grid1 import ImageGrid
import matplotlib.pyplot as plt
import numpy as np

class create(object):
	def __init__(self):
		self.domain=None
		self.dates=None
		self.directory=None
		self.array=[]
		self.level=[]
		self.axes=[]
		self.prefix=[]
		self.sufix=[]

	def config(self,**kwargs):
		
		self.domain = kwargs['domain']
		self.dates = kwargs['dates']
		self.level = kwargs['level']
		self.directory = kwargs['directory']
		self.axes = self.initialize_plot()
		self.prefix='/pgbhnl.gdas.'
		self.sufix='.nc'

	def initialize_plot(self):
		fig = plt.figure()

		plot_grids=ImageGrid( fig,111,
								nrows_ncols = (3,2),
								axes_pad = 0.0,
								add_all = True,
								share_all=False,
								label_mode = "L",
								cbar_location = "top",
								cbar_mode="single")		
		return plot_grids


	def isotac(self):
		u_arrays=read_files(self,'u')
		v_arrays=read_files(self,'v')
		
		for ax in self.axes:
			ax.imshow(v_arrays)

		plt.show()


#------------------------------------------
# LOCAL FUNCTIONS
#------------------------------------------
def read_files(self,var):

	if var == 'u':
		ncvar='UGRD_P0_L100_GLL0'
	elif var == 'v':
		ncvar='VGRD_P0_L100_GLL0'
	elif var == 'temp':
		ncvar='TMP_P0_L100_GLL0'
	elif var == 'rh':
		ncvar='RH_P0_L100_GLL0'
	elif var == 'geop'
		ncvar='HGT_P0_L100_GLL0'
	elif var == 'absvort':
		ncvar='ABSV_P0_L100_GLL0'


	gindx=get_geo_indices(self)
	vindx=get_vertical_index(self)

	for d in self.dates:
		cfsr_file = self.directory+self.prefix+d.strftime('%Y%m%d%H')+self.sufix
		data=Dataset(cfsr_file,'r')
		array = data.variables[ncvar][vindx, gindx[0]:gindx[1], gindx[2]:gindx[3]]

	data.close()
	return array
	

def get_geo_indices(self):
	d=self.dates[0]
	cfsr_file = self.directory+self.prefix+d.strftime('%Y%m%d%H')+self.sufix
	data=Dataset(cfsr_file,'r')
	nclons=data.variables['lon_0'][:]
	nclons = nclons-180
	nclats=data.variables['lat_0'][:]
	data.close()

	# longitude lower and upper index
	lonleft = np.argmin( np.abs( nclons - self.domain[0] ) )
	lonright = np.argmin( np.abs( nclons - self.domain[1] ) )  

	# latitude lower and upper index
	lattop = np.argmin( np.abs( nclats - self.domain[2] ) )
	latbot = np.argmin( np.abs( nclats - self.domain[3] ) ) 

	return [lonleft,lonright,lattop,latbot]

def get_vertical_index(self):
	d=self.dates[0]
	cfsr_file = self.directory+self.prefix+d.strftime('%Y%m%d%H')+self.sufix
	data=Dataset(cfsr_file,'r')
	ncisob=data.variables['lv_ISBL0'][:]
	data.close()
	indx=np.argmin( np.abs( ncisob - self.level ) )

	return indx
