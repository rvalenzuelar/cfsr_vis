#
# Visualization of CFSR data
#
# Raul Valenzuela
# August, 2015
#


from datetime import datetime,timedelta
import matplotlib.pyplot as plt
import numpy as np

import CFSR

def main():

	lonleft=-150
	lonright=-116
	lattop=55
	latbot=20	

	domain=[lonleft,lonright,lattop,latbot]

	local_directory='/home/rvalenzuela/'
	# directory='/Users/raulv/Desktop/'
	# local_directory='/home/raul/'

	case = raw_input('\nIndicate case (e.g. 1): ')
	base_directory=local_directory +'CFSR/case'+case.zfill(2)
	print base_directory

	start, end = get_times(case)
	
	delta=timedelta(hours=6)
	dates=get_dates(start,end,delta)
	
	cfsr = CFSR.create(domain=domain, dates=dates[:-1], directory=base_directory,
							zboundary=600)

	# cfsr.isotac(level=300, clevels=range(40,75,5),cmap='jet')
	# cfsr.windvector(level=300, jump=5, width=1.0, scale=2.0, key=40,colorkey='r')
	# cfsr.geopotential(level=300, clevels=range(830,970,10))
	# cfsr.add_coast(res='c')
	# cfsr.add_title()
	# cfsr.add_location('bby')

	# cfsr.absvort(level=500, clevels=range(1,6,1),cmap='YlOrBr')
	# cfsr.windvector(level=500, jump=5, width=1.0, scale=2.0, key=40,colorkey='r')
	# cfsr.geopotential(level=500, clevels=range(520,600,10))
	# cfsr.add_coast(res='c')
	# cfsr.add_title()
	# cfsr.add_location('bby')

	# cfsr.relhumid(level=700, clevels=range(90,102,2),cmap='YlGn')
	# cfsr.windvector(level=700, jump=5, width=1.5, scale=1.0, key=20,colorkey='r')
	# cfsr.geopotential(level=700, clevels=range(280,325,5))
	# cfsr.add_coast(res='c')
	# cfsr.add_title()
	# cfsr.add_location('bby')

	# cfsr.temperature(level=1000, vmin=0,vmax=20,cmap='jet')
	# cfsr.windvector(jump=5, width=1.5, scale=1.0, key=20,colorkey='white')
	# cfsr.geopotential()
	# cfsr.add_coast(res='c')
	# cfsr.add_title()
	# cfsr.add_location('bby')

	cfsr.geothickness(top=500, bottom=1000, clevels=range(5100,5730,30),cmap='RdBu_r')
	# cfsr.geothickness(top=800, bottom=1000, clevels=range(1750,1880,10),cmap='RdBu_r')
	# cfsr.geothickness(top=700, bottom=1000, clevels=range(2720,3040,20),cmap='RdBu_r')
	cfsr.windvector(level=1000, jump=4, width=0.5, scale=1.5, key=20,colorkey='white')
	# cfsr.geopotential(level=900)
	cfsr.surfpressure(clevels=range(980,1034,4))
	cfsr.add_coast(res='c')
	cfsr.add_title()
	cfsr.add_location('bby')

	# cfsr.theta(level=1000, clevels=range(270,298,2),cmap='RdBu_r')
	# cfsr.windvector(level=1000, jump=2, width=0.5, scale=1.5, key=20,colorkey='b')
	# # cfsr.geopotential(level=800,clevels=range(2000,3010,10))
	# # cfsr.geopotential(level=900)
	# cfsr.surfpressure(clevels=range(980,1034,4))
	# cfsr.add_coast(res='c')
	# cfsr.add_title()
	# cfsr.add_location('bby')

	# cfsr.thetaeq(level=1000, clevels=range(262,328,4),cmap='RdBu_r')
	# cfsr.windvector(level=1000, jump=2, width=0.5, scale=1.5, key=20,colorkey='b')
	# # cfsr.geopotential(level=800,clevels=range(2000,3010,10))
	# # cfsr.geopotential(level=900)
	# cfsr.surfpressure(clevels=range(980,1034,4))
	# cfsr.add_coast(res='c')
	# cfsr.add_title()
	# cfsr.add_location('bby')

	# ts_theta = cfsr.series['theta']
	ts_mslp = cfsr.series['surfpressure']
	ts_u = np.asarray(cfsr.series['u'])
	ts_v = np.asarray(cfsr.series['v'])
	ts_wspd = np.sqrt(ts_u**2+ts_v**2)
	R2D = 180./np.pi
	atan = np.arctan2(ts_v, ts_u)
	ts_wdir = (270-atan*R2D)%360

	fig,ax=plt.subplots(4,1,sharex=True)
	# ax[0].plot(ts_theta,'o-')
	ax[1].plot(ts_mslp,'o-')
	ax[2].plot(ts_wspd,'o-')
	ax[3].plot(ts_wdir,'o-')
	ax[0].invert_xaxis()
	plt.draw()





	cfsr.show('ipython')

def get_times(case):


	cfsr_time = {
				'1': [datetime(1998,1,18,0), datetime(1998,1,19,6)],
				'2': [datetime(1998,1,26,0), datetime(1998,1,27,6)],
				'3': [datetime(2001,1,23,0), datetime(2001,1,24,0)],
				'7':[datetime(2001,2,17,6), datetime(2001,2,18,0)]
				}


	return cfsr_time[case]


def plot_cross_sections():

	cfsr.cross_section(field='thetaeq', orientation=['zonal',38.30], 
						clevels=range(276,318,2),cmap='RdBu_r')

	cfsr.cross_section(field='q', orientation=['zonal',38.30], 
						clevels=range(0,11,1),cmap='RdBu_r')
	
	cfsr.cross_section(field='U', orientation=['zonal',38.30], 
						clevels=range(-16,18,2),cmap='RdBu_r')

	cfsr.cross_section(field='V', orientation=['zonal',38.30], 
						clevels=range(-16,18,2),cmap='RdBu_r')

	cfsr.cross_section(field='thetaeq+V', orientation=['zonal',40.], 
						clevels=[range(276,328,2), range(-15,20,5)],
						cmap='RdBu_r')

	cfsr.cross_section(field='thetaeq+U', orientation=['zonal',38.30], 
						clevels=[range(276,328,2), range(-15,20,5)],
						cmap='RdBu_r')

	cfsr.cross_section(field='thetaeq+V', orientation=['zonal',38.30], 
						clevels=[range(276,328,2), range(-15,20,5)],
						cmap='RdBu_r')

	cfsr.cross_section(field='thetaeq+V', orientation=['zonal',35.], 
					clevels=[range(276,328,2), range(-15,20,5)],
					cmap='RdBu_r')

def get_dates(start,end,delta):

	dates=[]
	if delta == timedelta(hours=0):
		dates.append(start)
		return dates
	else:
		foo=start
		dates.append(start)
		while foo<=end:
			foo += delta
			dates.append(foo)
		return dates

if __name__ == "__main__":
	main()



