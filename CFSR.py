#
# CFSR class
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
import Thermodyn as thermo


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
		self.l1=''
		self.l2=''
		self.l3=''
		self.l4=''

	def config(self,**kwargs):
		self.domain = kwargs['domain']
		self.dates = kwargs['dates']
		self.directory = kwargs['directory']
		self.prefix='/pgbhnl.gdas.'
		self.sufix='.nc'

	def initialize_plot(self):
		fig = plt.figure(figsize=(8.5,11))
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
		# fig.tight_layout()

		self.axes = grid


	def isotac(self,**kwargs):
		self.initialize_plot()
		self.level = kwargs['level']*100
		u_arrays=read_files(self,'u')
		v_arrays=read_files(self,'v')
		X,Y = np.meshgrid(self.lons,self.lats)
		clevels = kwargs['clevels']
		for i in range(6):
			SPD = np.sqrt(u_arrays[i]**2+v_arrays[i]**2)
			cs = self.axes[i].contourf(X,Y,SPD,clevels)
			set_limits(self,i)
			self.axes[i].set_aspect(1)
			self.axes[i].cax.colorbar(cs,ticks=clevels)
		self.l1='CFSR Reanalysis Isotacs [$ms^{-1}$]'
		self.l2='\nLevel: '+ str(self.level/100) + 'hPa'

	def temperature(self,**kwargs):
		self.initialize_plot()
		self.level = kwargs['level']*100
		t_arrays=read_files(self,'temperature')
		X,Y = np.meshgrid(self.lats,self.lons)
		cmap = kwargs['cmap']
		for i in range(6):
			extent=[min(self.lons),max(self.lons),
					min(self.lats),max(self.lats)]
			im = self.axes[i].imshow(t_arrays[i],
								extent=extent,
								interpolation=None,
								vmin=kwargs['vmin'],
								vmax=kwargs['vmax'],
								cmap=cmap)
			set_limits(self,i)
			self.axes[i].cax.colorbar(im)
		self.l1='CFSR Reanalysis Temperature [$^\circ$C]'
		self.l2='\nLevel: '+ str(self.level/100) + 'hPa'

	def theta(self,**kwargs):
		self.initialize_plot()
		self.level = kwargs['level']*100
		cmap = kwargs['cmap']
		t_arrays=read_files(self,'temperature') # [C]
		q_arrays=read_files(self,'sphum') # [kg/kg]
		X,Y = np.meshgrid(self.lons,self.lats)
		clevels = kwargs['clevels']
		for i in range(6):
			mixr = thermo.mixing_ratio(specific_humidity= q_arrays[i])
			press = np.zeros(mixr.shape)+kwargs['level'] #[hPa]
			theta = thermo.theta2(C=t_arrays[i],hPa=press,mixing_ratio=mixr)
			cf = self.axes[i].contourf(X,Y,theta, clevels, cmap=cmap)
			self.axes[i].cax.colorbar(cf,ticks=clevels)
			set_limits(self,i)
		self.l1='CFSR Reanalysis Potential Temperature [K]'
		self.l2='\nLevel: '+ str(self.level/100) + 'hPa'

	def relhumid(self,**kwargs):
		self.initialize_plot()
		self.level = kwargs['level']*100
		cmap = kwargs['cmap']
		rh_arrays=read_files(self,'relhumid')
		X,Y = np.meshgrid(self.lons,self.lats)
		clevels = kwargs['clevels']
		for i in range(6):
			cf = self.axes[i].contourf(X,Y,rh_arrays[i], clevels, cmap=cmap)
			self.axes[i].cax.colorbar(cf,ticks=clevels)
			set_limits(self,i)
		self.l1='CFSR Reanalysis Relative Humidity [%]'
		self.l2='\nLevel: '+ str(self.level/100) + 'hPa'

	def absvort(self,**kwargs):
		self.initialize_plot()
		self.level = kwargs['level']*100
		cmap = kwargs['cmap']
		vort_arrays=read_files(self,'absvort')
		X,Y = np.meshgrid(self.lons,self.lats)
		clevels = kwargs['clevels']
		for i in range(6):
			cs = self.axes[i].contourf(X,Y,vort_arrays[i],clevels,cmap=cmap)
			self.axes[i].cax.colorbar(cs,ticks=clevels)
			set_limits(self,i)
		self.l1='CFSR Reanalysis Absolute Vorticity [$s^{-1}$]'
		self.l2='\nLevel: '+ str(self.level/100) + 'hPa'

	def geothickness(self,**kwargs):
		self.initialize_plot()
		self.level=kwargs['top']*100 #[Pa]
		lv1_arrays=read_files(self,'geop')
		self.level=kwargs['bottom']*100 #[Pa]
		lv2_arrays=read_files(self,'geop')
		X,Y = np.meshgrid(self.lons,self.lats)
		clevels = kwargs['clevels']
		cmap = kwargs['cmap']		
		for i in range(6):
			thickness=lv1_arrays[i]-lv2_arrays[i]
			cs = self.axes[i].contourf(X,Y,thickness,clevels,cmap=cmap)
			self.axes[i].cax.colorbar(cs,ticks=clevels[::2])
			set_limits(self,i)
		self.l1='CFSR Reanalysis Geopotential Thickness [m]'
		self.l2='\nbetween '+ str(kwargs['top']) + ' and '+ str(kwargs['bottom']) + ' hPa'

	def windvector(self,**kwargs):
		if 'level' in kwargs:
			self.level=kwargs['level']*100 #[Pa]
			self.l3='\nWind vectors: '+str(kwargs['level'])+' hPa'
		u_arrays=read_files(self,'u')
		v_arrays=read_files(self,'v')
		X,Y = np.meshgrid(self.lons,self.lats)
		jump = kwargs['jump']
		width = kwargs['width']
		key = kwargs['key']
		color = kwargs['color']
		for i in range(6):
			u = u_arrays[i]
			v = v_arrays[i]
			u = u[::jump,::jump]
			v = v[::jump,::jump]
			x = X[::jump,::jump]
			y = Y[::jump,::jump]
			Q = self.axes[i].quiver(x, y, u, v, 
									units='dots',
									scale_units='dots',
									scale=2.0,
									width=width)
			keylab=str(key)+' m/s'
			self.axes[i].quiverkey(Q, 0.15, 0.05, key, keylab,
							labelpos='N',
							coordinates='axes',
							fontproperties={'weight': 'bold','size':12},
							color=color,
							labelcolor=color)

	def geopotential(self,**kwargs):
		if 'level' in kwargs:
			self.level=kwargs['level']*100 #[Pa]
			self.l4='\nGeopotential hgt: '+str(kwargs['level'])+' hPa'
		geop_arrays=read_files(self,'geop')
		X,Y = np.meshgrid(self.lons,self.lats)
		for i in range(6):
			hgt=geop_arrays[i]/10 #[dm]
			cs = self.axes[i].contour(X,Y,hgt,colors='k')			
			self.axes[i].clabel(cs, 
								fontsize=12,
								fmt='%1.0f',)
			# add_date(self,i)



	def add_coast(self,**kwargs):
		M = Basemap(projection='cyl', lat_0=35, lon_0=-130,
					resolution = kwargs['res'], area_thresh = 0.1,
					llcrnrlon=self.domain[0], llcrnrlat=self.domain[3]+0.05,
					urcrnrlon=self.domain[1]+0.01, urcrnrlat=self.domain[2])
		coastline = M.coastpolygons
		xline= coastline[0][0]
		yline= coastline[0][1]
		for i in range(6):
			self.axes[i].plot(xline, yline,
								color = (0.5,0.5,0.5),
								linewidth = 2,
								linestyle = '-')
	
	def add_title(self):
		plt.suptitle(	self.l1 + 
						self.l2 + 
						self.l3 + 
						self.l4)

	def add_date(self):
		for i in range(6):
			date=self.dates[i]
			date=date.strftime('%Y%m%d %H')+' UTC'
			self.axes[i].text(0.98, 0.05, date,
					horizontalalignment='right',
					verticalalignment='center',
					transform = self.axes[i].transAxes,
					bbox=dict(facecolor='white'),
					zorder=10)

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
	elif var == 'sphum':
		ncvar='SPFH_P0_L100_GLL0'# [kg kg-1]


	gindx=get_geo_index(self) # horizontal index
	vindx=get_vertical_index(self) # vertical index

	array=[]
	for d in self.dates:
		cfsr_file = self.directory+self.prefix+d.strftime('%Y%m%d%H')+self.sufix
		data=Dataset(cfsr_file,'r')
		sub=shiftgrid(data.variables[ncvar][vindx,:,:])
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
	lonleft = np.argmin( np.abs( nclons - self.domain[0] ) ) - 1
	lonright = np.argmin( np.abs( nclons - self.domain[1] ) ) + 1

	# latitude lower and upper index
	lattop = np.argmin( np.abs( nclats - self.domain[2] ) ) - 1
	latbot = np.argmin( np.abs( nclats - self.domain[3] ) ) + 1

	if len(self.lons) == 0:
		self.lons=nclons[lonleft:lonright]
		# self.lons=nclons

	if len(self.lats) == 0:
		self.lats=nclats[lattop:latbot]
		# self.lats=nclats

	return [lonleft,lonright,lattop,latbot]


def get_vertical_index(self):
	d=self.dates[0]
	cfsr_file = self.directory+self.prefix+d.strftime('%Y%m%d%H')+self.sufix
	data=Dataset(cfsr_file,'r')
	ncisob=data.variables['lv_ISBL0'][:]
	data.close()
	indx=np.argmin( np.abs( ncisob - self.level ) )

	return indx


def shiftgrid(array):
	"""
	shift grid so it goes from -180 to 180 (instead of 0 to 360
	in longitude)
	"""
	part = np.hsplit(array,2)
	array_arranged=np.concatenate((part[1],part[0]),axis=1)

	return array_arranged

def set_limits(self,i):
	xlim=[self.domain[0],self.domain[1]]
	ylim=[self.domain[3],self.domain[2]]
	self.axes[i].set_xlim(xlim)
	self.axes[i].set_ylim(ylim)


	
