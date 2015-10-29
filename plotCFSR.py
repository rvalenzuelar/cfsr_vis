#
# Visualization of CFSR data
#
# Raul Valenzuela
# August, 2015
#


from datetime import datetime,timedelta

import CFSR

def main():

	lonleft=-150
	lonright=-116
	lattop=55
	latbot=20	

	domain=[lonleft,lonright,lattop,latbot]

	local_directory='/home/rvalenzuela/'
	# directory='/Users/raulv/Desktop/'

	case = raw_input('\nIndicate case (e.g. 1): ')
	base_directory=local_directory +'CFSR/case'+case.zfill(2)
	print base_directory

	
	if case=='3':
		start=datetime(2001,1,23,0)
		end=datetime(2001,1,24,6)
	elif case=='7':
		start=datetime(2001,2,17,6)
		end=datetime(2001,2,18,6)

	delta=timedelta(hours=6)
	dates=get_dates(start,end,delta)

	cfsr = CFSR.create(domain=domain, dates=dates, directory=base_directory,
							zboundary=600)

	cfsr.isotac(level=300, clevels=range(40,75,5),cmap='jet')
	cfsr.windvector(jump=5, width=1.0, scale=2.0, key=40,colorkey='r')
	cfsr.geopotential(level=300, clevels=range(830,970,10))
	cfsr.surfpressure(clevels=range(980,1034,4))
	cfsr.add_coast(res='c')
	cfsr.add_title()
	cfsr.add_location('bby')

	# cfsr.absvort(level=500, clevels=range(1,6,1),cmap='YlOrBr')
	# cfsr.windvector(level=500, jump=5, width=1.0, scale=2.0, key=40,colorkey='r')
	# cfsr.geopotential(level=500, clevels=range(520,600,10))
	# cfsr.surfpressure(clevels=range(980,1034,4))
	# cfsr.add_coast(res='c')
	# cfsr.add_title()
	# cfsr.add_location('bby')

	# cfsr.relhumid(level=700, clevels=range(90,102,2),cmap='YlGn')
	# cfsr.windvector(jump=5, width=1.5, scale=1.0, key=20,colorkey='r')
	# cfsr.geopotential()
	# cfsr.add_coast(res='c')
	# cfsr.add_title()
	# cfsr.add_location('bby')

	# cfsr.temperature(level=1000, vmin=0,vmax=20,cmap='jet')
	# cfsr.windvector(jump=5, width=1.5, scale=1.0, key=20,colorkey='white')
	# cfsr.geopotential()
	# cfsr.add_coast(res='c')
	# cfsr.add_title()
	# cfsr.add_location('bby')

	# cfsr.geothickness(top=800, bottom=1000, clevels=range(1720,1900,10),cmap='RdBu_r')
	# cfsr.windvector(level=900, jump=5, width=1.5, scale=1.0, key=30,colorkey='white')
	# cfsr.geopotential(level=500)
	# cfsr.add_coast(res='c')
	# cfsr.add_title()
	# cfsr.add_location('bby')

	cfsr.thetaeq(level=800, clevels=range(276,328,2),cmap='RdBu_r')
	cfsr.windvector(level=1000, jump=5, width=1.0, scale=1.0, key=20,colorkey='b')
	cfsr.surfpressure(clevels=range(980,1034,4))
	cfsr.add_coast(res='c')
	cfsr.add_title()
	cfsr.add_location('bby')

	# cfsr.cross_section(field='thetaeq', orientation=['zonal',38.30], 
	# 					clevels=range(276,318,2),cmap='RdBu_r')

	# cfsr.cross_section(field='q', orientation=['zonal',38.30], 
	# 					clevels=range(0,11,1),cmap='RdBu_r')
	
	# cfsr.cross_section(field='U', orientation=['zonal',38.30], 
	# 					clevels=range(-16,18,2),cmap='RdBu_r')

	# cfsr.cross_section(field='V', orientation=['zonal',38.30], 
	# 					clevels=range(-16,18,2),cmap='RdBu_r')

	# cfsr.cross_section(field='thetaeq+V', orientation=['zonal',40.], 
	# 					clevels=[range(276,328,2), range(-15,20,5)],
	# 					cmap='RdBu_r')

	# cfsr.cross_section(field='thetaeq+U', orientation=['zonal',38.30], 
	# 					clevels=[range(276,328,2), range(-15,20,5)],
	# 					cmap='RdBu_r')

	# cfsr.cross_section(field='thetaeq+V', orientation=['zonal',38.30], 
	# 					clevels=[range(276,328,2), range(-15,20,5)],
	# 					cmap='RdBu_r')

	# cfsr.cross_section(field='thetaeq+V', orientation=['zonal',35.], 
	# 				clevels=[range(276,328,2), range(-15,20,5)],
	# 				cmap='RdBu_r')

	cfsr.show('ipython')


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



