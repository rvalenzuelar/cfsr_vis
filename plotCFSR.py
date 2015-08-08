#
# Visualization of CFSR data
#
# Raul Valenzuela
# August, 2015
#


from netCDF4 import Dataset
from mpl_toolkits.axes_grid1 import ImageGrid
from pylab import quiver,quiverkey
from mpl_toolkits.basemap import Basemap

import matplotlib.pyplot as plt
import numpy as np

class create(object):
	def __init__(self):
		self.domain=None
		self.dates=None
		self.directory=None
		self.level=[]
		self.axes=[]
		self.prefix=[]
		self.sufix=[]
		self.lats=[]
		self.lons=[]

	def config(self,**kwargs):
		
		self.domain = kwargs['domain']
		self.dates = kwargs['dates']
		self.directory = kwargs['directory']
		self.prefix='/pgbhnl.gdas.'
		self.sufix='.nc'

	def initialize_plot(self,**kwargs):
		fig = plt.figure()

		grid = ImageGrid( fig,111,
								nrows_ncols = (3,2),
								axes_pad = 0.0,
								add_all = True,
								share_all=False,
								label_mode = "L",
								cbar_location = "top",
								cbar_mode="single",
								cbar_size='1%',
								aspect=True)		

		# grid = plt.subplots(3,2,sharex=True,sharey=True)

		self.axes = grid

		level = kwargs['level']
		self.level = level*100 # [Pa]

	def isotac(self,**kwargs):

		u_arrays=read_files(self,'u')
		v_arrays=read_files(self,'v')
		X,Y = np.meshgrid(self.lons,self.lats)

		for i in range(6):

			SPD = np.sqrt(u_arrays[i]**2+v_arrays[i]**2)

			cs = self.axes[i].contourf(X,Y,SPD,kwargs['cmap'])
			self.axes[i].set_aspect(1)
			self.axes[i].cax.colorbar(cs)
	
	def temperature(self,**kwargs):

		t_arrays=read_files(self,'temperature')
		X,Y = np.meshgrid(self.lats,self.lons)

		for i in range(6):
			
			extent=[min(self.lons),max(self.lons),
					min(self.lats),max(self.lats)]
			im = self.axes[i].imshow(t_arrays[i],
								extent=extent,
								interpolation=None,
								vmin=kwargs['vmin'],
								vmax=kwargs['vmax'])
			self.axes[i].cax.colorbar(im)

	def relhumid(self,**kwargs):

		rh_arrays=read_files(self,'relhumid')
		X,Y = np.meshgrid(self.lons,self.lats)

		for i in range(6):
			
			cs = self.axes[i].contourf(X,Y,rh_arrays[i],
										kwargs['cmap'],
										cmap='YlGn')
			self.axes[i].cax.colorbar(cs)

	def absvort(self,**kwargs):

		vort_arrays=read_files(self,'absvort')

		X,Y = np.meshgrid(self.lons,self.lats)

		for i in range(6):
			
			cs = self.axes[i].contourf(X,Y,vort_arrays[i],
										kwargs['cmap'],
										cmap='YlOrBr')
			self.axes[i].cax.colorbar(cs)



	def windvector(self):

		u_arrays=read_files(self,'u')
		v_arrays=read_files(self,'v')
		X,Y = np.meshgrid(self.lons,self.lats)
		jump = 3
		for i in range(6):

			u = u_arrays[i]
			v = v_arrays[i]
			u = u[::jump,::jump]
			v = v[::jump,::jump]
			x = X[::jump,::jump]
			y = Y[::jump,::jump]

			Q = self.axes[i].quiver(x, y, u, v, units='width')
			qk = quiverkey(Q, 0.9, 0.95, 10, r'$10 \frac{m}{s}$',
							labelpos='E',
							coordinates='figure',
							fontproperties={'weight': 'bold'})

	def geopotential(self):

		geop_arrays=read_files(self,'geop')
		X,Y = np.meshgrid(self.lons,self.lats)

		for i in range(6):
			cs = self.axes[i].contour(X,Y,geop_arrays[i],colors='k')			
			self.axes[i].clabel(cs, 
								fontsize=12,
								fmt='%1.0f',)

	def add_coast(self):

		M = Basemap(projection='cyl', lat_0=35, lon_0=-130,
					resolution = 'i', area_thresh = 0.1,
					llcrnrlon=self.domain[0], llcrnrlat=self.domain[3],
					urcrnrlon=self.domain[1], urcrnrlat=self.domain[2])

		coastline = M.coastpolygons

		xline= coastline[0][0]
		yline= coastline[0][1]

		for i in range(6):
			self.axes[i].plot(xline, yline,
								color = (0.5,0.5,0.5),
								linewidth = 2,
								linestyle = '-')
	def show(self):
		plt.show()


'''			LOCAL FUNCTIONS
*********************************************
'''

def read_files(self,var):

	''' Retrieve arrays per dates '''

	if var == 'u':
		ncvar='UGRD_P0_L100_GLL0'
	elif var == 'v':
		ncvar='VGRD_P0_L100_GLL0'
	elif var == 'temperature':
		ncvar='TMP_P0_L100_GLL0'
	elif var == 'relhumid':
		ncvar='RH_P0_L100_GLL0'
	elif var == 'geop':
		ncvar='HGT_P0_L100_GLL0'
	elif var == 'absvort':
		ncvar='ABSV_P0_L100_GLL0'


	gindx=get_geo_index(self)
	vindx=get_vertical_index(self)

	array=[]
	for d in self.dates:
		cfsr_file = self.directory+self.prefix+d.strftime('%Y%m%d%H')+self.sufix
		data=Dataset(cfsr_file,'r')
		sub=rearrange(data.variables[ncvar][vindx,:,:])
		sub=sub[gindx[2]:gindx[3],gindx[0]:gindx[1]]

		if var=='temperature':
			sub[:,:] = [x - 273.15 for x in sub]
		elif var =='absvort':
			sub[:,:] = [x * 10**4 for x in sub]

		array.append(sub)

	data.close()
	return array
	

def get_geo_index(self):
	
	d=self.dates[0]
	cfsr_file = self.directory+self.prefix+d.strftime('%Y%m%d%H')+self.sufix
	data=Dataset(cfsr_file,'r')
	nclons=data.variables['lon_0'][:]
	nclons=nclons-180
	nclats=data.variables['lat_0'][:]
	data.close()

	# longitude lower and upper index
	lonleft = np.argmin( np.abs( nclons - self.domain[0] ) )
	lonright = np.argmin( np.abs( nclons - self.domain[1] ) )  

	# latitude lower and upper index
	lattop = np.argmin( np.abs( nclats - self.domain[2] ) )
	latbot = np.argmin( np.abs( nclats - self.domain[3] ) ) 

	if len(self.lons) == 0:
		self.lons=nclons[lonleft:lonright]

	if len(self.lats) == 0:
		self.lats=nclats[lattop:latbot]

	return [lonleft,lonright,lattop,latbot]


def get_vertical_index(self):
	
	d=self.dates[0]
	cfsr_file = self.directory+self.prefix+d.strftime('%Y%m%d%H')+self.sufix
	data=Dataset(cfsr_file,'r')
	ncisob=data.variables['lv_ISBL0'][:]
	data.close()
	indx=np.argmin( np.abs( ncisob - self.level ) )

	return indx


def rearrange(array):

	part = np.hsplit(array,2)
	array_arranged=np.concatenate((part[1],part[0]),axis=1)

	return array_arranged

