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
from matplotlib import colors

import seaborn as sns
sns.set_style("ticks")

class create(object):
	def __init__(self,**kwargs):
		self.domain = kwargs['domain']
		self.dates = kwargs['dates']
		self.directory = kwargs['directory']
		self.level = []
		self.axes = []
		self.prefix = '/pgbhnl.gdas.'
		self.sufix = '.nc'
		self.lats = None
		self.lons = None
		self.l1 = ' '
		self.l2 = ' '
		self.l3 = ' '
		self.horizontal=True
		self.orientation=None
		self.hboundary=None
		self.zboundary=kwargs['zboundary']

	def initialize_plot(self):
		fig = plt.figure(figsize=(8.5,11))

		if self.orientation:
			rowscols=(6,1)
			axpad=0.1
		else:
			rowscols=(3,2)
			axpad=0
		grid = ImageGrid( fig,111,
								nrows_ncols = rowscols,
								axes_pad = axpad,
								add_all = True,
								share_all=False,
								label_mode = "L",
								cbar_location = "top",
								cbar_mode="single",
								cbar_size='5%',
								aspect=True)		
		# grid = plt.subplots(3,2,sharex=True,sharey=True)
		# fig.tight_layout()
		self.l3=''
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
		self.l1='CFSR Isotacs [$ms^{-1}$]'
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
		self.l1='CFSR Temperature [$^\circ$C]'
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
			self.axes[i].cax.colorbar(cf,ticks=clevels[::4])
			set_limits(self,i)
		self.l1='CFSR Potential Temperature [K]'
		self.l2='\nLevel: '+ str(self.level/100) + 'hPa'

	def thetaeq(self,**kwargs):
		self.initialize_plot()
		self.level = kwargs['level']*100
		cmap = kwargs['cmap']
		clevels = kwargs['clevels']
		t_arrays=read_files(self,'temperature') # [C]
		q_arrays=read_files(self,'sphum') # [kg/kg]
		rh_arrays=read_files(self,'relhumid')
		press = np.zeros(rh_arrays[0].shape)+kwargs['level'] #[hPa]
		X,Y = np.meshgrid(self.lons,self.lats)
		for i in range(6):
			mixr = thermo.mixing_ratio(specific_humidity= q_arrays[i])
			theta = thermo.theta_equiv2(C=t_arrays[i],hPa=press,
										mixing_ratio=mixr,relh=rh_arrays[i])
			cf = self.axes[i].contourf(X,Y,theta, clevels, cmap=cmap)
			self.axes[i].cax.colorbar(cf,ticks=clevels[::4])
			set_limits(self,i)
			self.add_date(i)
		self.l1='CFSR Equivalent Potential Temperature [K]'
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
		self.l1='CFSR Relative Humidity [%]'
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
		self.l1='CFSR Absolute Vorticity [$s^{-1}$]'
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
		self.l1='CFSR ' + str(kwargs['top']) + ' - '+ str(kwargs['bottom']) + ' hPa' +' Geopotential Thickness [m]'
		# self.l2='\nbetween '+ str(kwargs['top']) + ' and '+ str(kwargs['bottom']) + ' hPa'

	def windvector(self,**kwargs):
		if 'level' in kwargs:
			self.level=kwargs['level']*100 #[Pa]
			self.l2='\nWind vectors: '+str(kwargs['level'])+' hPa'
		u_arrays=read_files(self,'u')
		v_arrays=read_files(self,'v')
		X,Y = np.meshgrid(self.lons,self.lats)
		jump = kwargs['jump']
		width = kwargs['width']
		key = kwargs['key']
		colorkey = kwargs['colorkey']
		scale = kwargs['scale']
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
									scale=scale,
									width=width,
									zorder=9)
			keylab=str(key)+' m/s'
			self.axes[i].quiverkey(Q, 0.9, 0.05, key, keylab,
							labelpos='N',
							coordinates='axes',
							fontproperties={'weight': 'bold','size':12},
							color=colorkey,
							labelcolor=colorkey)

	def geopotential(self,**kwargs):
		if 'level' in kwargs:
			self.level=kwargs['level']*100 #[Pa]
			self.l3='\nGeopotential hgt: '+str(kwargs['level'])+' hPa\n'
		geop_arrays=read_files(self,'geop')
		X,Y = np.meshgrid(self.lons,self.lats)
		for i in range(6):
			hgt=geop_arrays[i]/10 #[dm]
			cs = self.axes[i].contour(X,Y,hgt,colors='k',linewidths=0.5)			
			self.axes[i].clabel(cs, 
								fontsize=12,
								fmt='%1.0f',)

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
		plt.suptitle(	self.l1 + self.l2 + self.l3 )

	def add_date(self,i):
		# for i in range(6):
			date=self.dates[i]
			date=date.strftime('%Y%m%d %H')+' UTC'
			self.axes[i].text(0.1, 0.05, date,
					horizontalalignment='left',
					verticalalignment='bottom',
					transform = self.axes[i].transAxes,
					bbox=dict(facecolor='white'),
					zorder=10)

	def add_location(self,locname):

		if locname == 'bby':
			label='BBY'

		for i in range(6):
			if i == 0:
				self.axes[i].plot(-123.09,38.30,'o',markersize=4,color='b')
				self.axes[i].annotate(label,xy=(-123.09,38.30),
											xycoords='data',
											xytext=(-121.0,41.),
											textcoords='data',
											size=15,
											color='b',
											arrowprops=dict(arrowstyle="-",
																fc='b',
																ec='b',
																lw=2))
			else:
				self.axes[i].plot(-123.09,38.30,'o',markersize=4,color='b')


	def cross_section(self,**kwargs):
		

		field=kwargs['field']
		clevels=kwargs['clevels']
		cmap=kwargs['cmap']
		self.orientation=kwargs['orientation']
		
		self.initialize_plot()
		self.horizontal = False		
		t_arrays=read_files(self,'temperature') # [C]
		q_arrays=read_files(self,'sphum') # [kg/kg]
		rh_arrays=read_files(self,'relhumid')
		
		isob = get_vertical_array(self)/100. # to [hPa]
		z,n=t_arrays[0].shape
		press=np.tile(np.array([isob]).transpose(),(1,n))

		X,Y=np.meshgrid(range(len(self.lons)),range(len(isob)))


		if len(clevels) == 2:
			foo=clevels[0]
			boundsc=clevels[1]
			clevels=foo

		''' make a color map of fixed colors '''
		vmin=min(clevels)
		vmax=max(clevels)
		bounds=clevels
		snsmap=sns.color_palette(cmap, n_colors=len(bounds))
		cmap = colors.ListedColormap(snsmap)		
		norm = colors.BoundaryNorm(bounds, cmap.N)

		plot_field=[]
		if field == 'thetaeq':
			for i in range(6):
				mixr = thermo.mixing_ratio(specific_humidity= q_arrays[i])
				theta = thermo.theta_equiv2(C=t_arrays[i],hPa=press,
											mixing_ratio=mixr,relh=rh_arrays[i])
				theta[theta>320]=np.nan
				plot_field.append(theta)
			plot_fieldc = plot_field
			cboundaries=bounds
			cticks=bounds
			boundsc=bounds
			ti = ' - Equivalent potential temperature [K]'
		elif field == 'q':
			for i in range(6):
				q = q_arrays[i]
				plot_field.append(q*1000.) #[g kg-1]
			plot_fieldc = plot_field
			cboundaries=bounds
			cticks=bounds
			boundsc=bounds
			ti = ' - Specific humidity [g kg-1]'
		elif field == 'U':
			plot_field=read_files(self,'u')
			plot_fieldc = plot_field
			cboundaries=bounds
			cticks=bounds	
			boundsc=bounds
			ti = ' - Wind speed zonal component [m s-1]'
		elif field == 'V':
			plot_field=read_files(self,'v')
			plot_fieldc = plot_field
			cboundaries=bounds
			cticks=bounds	
			boundsc=bounds		
			ti = ' - Wind speed meridional component [m s-1]'
		elif field == 'thetaeq+U':
			for i in range(6):
				mixr = thermo.mixing_ratio(specific_humidity= q_arrays[i])
				theta = thermo.theta_equiv2(C=t_arrays[i],hPa=press,
											mixing_ratio=mixr,relh=rh_arrays[i])
				theta[theta>320]=np.nan
				plot_field.append(theta)			
			plot_fieldc=read_files(self,'u')
			cboundaries=bounds
			cticks=bounds			
			t0 = '\nEquivalent potential temperature [K] (color coded)'
			t1 = '\nWind speed zonal component [m s-1] (contour lines)'
			ti=t0+t1
		elif field == 'thetaeq+V':
			for i in range(6):
				mixr = thermo.mixing_ratio(specific_humidity= q_arrays[i])
				theta = thermo.theta_equiv2(C=t_arrays[i],hPa=press,
											mixing_ratio=mixr,relh=rh_arrays[i])
				theta[theta>320]=np.nan
				plot_field.append(theta)			
			plot_fieldc=read_files(self,'v')
			cboundaries=bounds
			cticks=bounds			
			t0 = '\nEquivalent potential temperature [K] (color coded)'
			t1 = '\nWind speed meridional component [m s-1] (contour lines)'
			ti=t0+t1


		for i in range(6):
			im=self.axes[i].imshow(plot_field[i],
									interpolation='none',
									vmin=vmin,
									vmax=vmax,
									cmap=cmap,
									norm=norm)
			self.axes[i].cax.colorbar(im,cmap=cmap, norm=norm,
										boundaries=cboundaries, ticks=cticks[::4])
			xticks=self.lons[::10]
			xticklabs=[str(x) for x in xticks]
			xticklabs.reverse()
			xticklabs.append(' ')
			xticklabs.reverse()
			self.axes[i].set_xticklabels(xticklabs)
			yidx = np.where(isob == self.zboundary)[0]
			self.axes[i].set_ylim([36,yidx])
			yticks = self.axes[i].get_yticks()
			isob_yticks = [isob[y] for y in yticks]
			if i == 0:
				yticklabs=[str(x) for x in isob_yticks]		
			else:
				yticklabs=[' ' for x in isob_yticks]		
			self.axes[i].set_yticklabels(yticklabs)

			''' add contour lines '''			
			cs=self.axes[i].contour(X,Y,plot_fieldc[i],
										origin='lower',levels=boundsc,colors='k',linewidths=0.5)
			if field in ['thetaeq+U', 'thetaeq+V']:
				self.axes[i].clabel(cs, boundsc,
							fmt='%1.0f',
							fontsize=10)			
			self.axes[i].set_ylim([36,yidx])

			''' add vertical line '''
			xidx = np.where(self.lons == -123.0)
			self.axes[i].axvline(xidx,color='k',linestyle=':')

			''' add date to subplot '''
			self.add_date(i)

			''' add axis label '''
			self.axes[i].set_xlabel('Longitude [deg]')
			if i == 0: self.axes[i].set_ylabel('Pressure level [hPa]')

		t1='Climate Forecast System Reanalysis'+ti
		if self.orientation[0] == 'zonal':
			t2='\nLatitude: ' + str(self.orientation[1])
		elif self.orientation[0] == 'meridional':
			t2='\nLongitude: ' + str(self.orientation[1])
		plt.suptitle(t1+t2)

	def show(self):
		# plt.show(block=False)
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
	array=[]
	for d in self.dates:
		if self.horizontal:
			vindx=get_vertical_index(self) # vertical index
			data=get_horizontal_field(self,d,ncvar,vindx)
			data=data[gindx[2]:gindx[3],gindx[0]:gindx[1]]
		else:
			data=get_vertical_field(self,d,ncvar,gindx)

		if var=='temperature':
			data[:,:] = [x - 273.15 for x in data]
		elif var =='absvort':
			data[:,:] = [x * 10**4 for x in data]			

		array.append(data)
	return array
	

def get_horizontal_field(self,date,ncvar,vindx):

	cfsr_file = self.directory+self.prefix+date.strftime('%Y%m%d%H')+self.sufix
	data=Dataset(cfsr_file,'r')
	# array_out = data.variables[ncvar][vindx,:,:]
	array_out = data.variables[ncvar][:,:,:]
	array_out=shiftgrid(array_out)
	array_out=array_out[vindx,:,:]

	data.close()
	# array_out=shiftgrid(array_out)
	return array_out


def get_vertical_field(self,date,ncvar,gindx):

	cfsr_file = self.directory+self.prefix+date.strftime('%Y%m%d%H')+self.sufix
	data=Dataset(cfsr_file,'r')
	if self.orientation[0] == 'zonal':
		array_out = data.variables[ncvar][:,:, :]
		array_out = shiftgrid(array_out)
		array_out = array_out[:, gindx[2], gindx[0]:gindx[1]]
		
	
	elif self.orientation[0] == 'meridional':
		array_out = data.variables[ncvar][:, gindx[0]:gindx[1], gindx[2]]
		print gindx[2]
		fig,ax=plt.subplots()
		ax.imshow(array_out)
		plt.draw()		

		array_out = data.variables[ncvar][:,:,gindx[2]]
		fig,ax=plt.subplots()
		ax.imshow(array_out)
		plt.draw()		

		print self.lats
		plt.show()

		exit()

	data.close()
		
	return array_out



def get_geo_index(self):
	
	d=self.dates[0]
	cfsr_file = self.directory+self.prefix+d.strftime('%Y%m%d%H')+self.sufix
	data=Dataset(cfsr_file,'r')
	nclons=data.variables['lon_0'][:] # len = 720
	nclons=nclons-180 # [0 ...60 ...-180 ...-60 ...0] to [-180 ... -60 ... 0  ... 60 ... 180]
	nclats=data.variables['lat_0'][:] # len = 361
	data.close()

	''' longitude lower and upper index '''
	lonleft = np.argmin( np.abs( nclons - self.domain[0] ) ) 
	lonright = np.argmin( np.abs( nclons - self.domain[1] ) ) + 1

	''' latitude lower and upper index '''
	lattop = np.argmin( np.abs( nclats - self.domain[2] ) ) - 1
	latbot = np.argmin( np.abs( nclats - self.domain[3] ) ) + 1

	# if len(self.lons) == 0:
	# 	self.lons=nclons[lonleft:lonright]
	# 	# self.lons=nclons

	# if len(self.lats) == 0:
	# 	self.lats=nclats[lattop:latbot]
	# 	# self.lats=nclats

	if self.horizontal:
		self.lons=nclons[lonleft:lonright]
		self.lats=nclats[lattop:latbot]
		return [lonleft,lonright,lattop,latbot]
	else:
		if self.orientation[0] == 'zonal':
			lat_section = np.argmin( np.abs( nclats - self.orientation[1] ) )		
			self.lons=nclons[lonleft:lonright]			
			return [lonleft,lonright,lat_section]
		elif self.orientation[0] == 'meridional':
			lon_section = np.argmin( np.abs( nclons - self.orientation[1] ) )
			self.lats=nclats[lattop:latbot]
			return [lattop,latbot,lon_section]
		


def get_vertical_index(self):

	ncisob = get_vertical_array(self)
	indx=np.argmin( np.abs( ncisob - self.level ) )

	return indx

def get_vertical_array(self):

	d=self.dates[0]
	cfsr_file = self.directory+self.prefix+d.strftime('%Y%m%d%H')+self.sufix
	data=Dataset(cfsr_file,'r')
	ncisob=data.variables['lv_ISBL0'][:]
	data.close()

	return ncisob


def shiftgrid(array):
	"""
	shift grid so it goes from -180 to 180 (instead of 0 to 360
	in longitude)
	"""
	# part = np.hsplit(array,2)
	# array_arranged=np.concatenate((part[1],part[0]),axis=1)

	parts = np.split(array,2,axis=2) # 3D meridional incision
	array_arranged=np.concatenate((parts[1],parts[0]),axis=2)

	return array_arranged

def set_limits(self,i):
	if self.horizontal:
		xlim=[self.domain[0],self.domain[1]]
		ylim=[self.domain[3],self.domain[2]]
		self.axes[i].set_xlim(xlim)
		self.axes[i].set_ylim(ylim)
	else:
		if self.orientation[0] == 'zonal':
			xlim=[self.domain[0],self.domain[1]]
			# ylim=[1000.,100.]
			self.axes[i].set_xlim(xlim)
			# self.axes[i].set_ylim(ylim)
		elif self.orientation[0] == 'meridional':
			xlim=[self.domain[3],self.domain[2]]
			ylim=[1000.,100.]
			self.axes[i].set_xlim(xlim)
			self.axes[i].set_ylim(ylim)

	
