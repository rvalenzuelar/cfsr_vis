#
# Visualization of CFSR data
#
# Raul Valenzuela
# August, 2015
#


from datetime import datetime,timedelta

import plotCFSR

def main():

	lonleft=-150
	lonright=-116
	lattop=55
	latbot=20	

	domain=[lonleft,lonright,lattop,latbot]

	start=datetime(2001,1,23,12)
	end=datetime(2001,1,24,18)
	delta=timedelta(hours=6)
	dates=get_dates(start,end,delta)

	directory='/home/rvalenzuela/CFSR/case03'
	# directory='/Users/raulv/Desktop/CFSR'

	cfsr=plotCFSR.create()
	cfsr.config(domain=domain, dates=dates, directory=directory)

	cfsr.isotac(level=300, clevels=range(40,75,5))
	cfsr.windvector(jump=5, width=1.5, key=40,color='k')
	cfsr.geopotential()
	cfsr.add_coast(res='c')
	cfsr.add_date()
	cfsr.add_title()

	cfsr.absvort(level=500, clevels=range(1,6,1),cmap='YlOrBr')
	cfsr.windvector(jump=5, width=1.5, key=40,color='k')
	cfsr.geopotential()
	cfsr.add_coast(res='c')
	cfsr.add_date()
	cfsr.add_title()

	cfsr.relhumid(level=700, clevels=range(90,102,2),cmap='YlGn')
	cfsr.windvector(jump=5, width=1.5, key=20,color='k')
	cfsr.geopotential()
	cfsr.add_coast(res='c')
	cfsr.add_date()
	cfsr.add_title()

	cfsr.temperature(level=1000, vmin=0,vmax=20,cmap='jet')
	cfsr.windvector(jump=5, width=1.5, key=20,color='k')
	cfsr.geopotential()
	cfsr.add_coast(res='c')
	cfsr.add_date()
	cfsr.add_title()

	cfsr.geothickness(top=800, bottom=1000, clevels=range(1720,1900,10),cmap='RdBu_r')
	cfsr.windvector(level=900, jump=5, width=1.5, key=30,color='k')
	cfsr.geopotential(level=500)
	cfsr.add_coast(res='c')
	cfsr.add_date()
	cfsr.add_title()

	cfsr.theta(level=975, clevels=range(268,298,2),cmap='coolwarm')
	cfsr.windvector(jump=5, width=1.5, key=30,color='white')
	cfsr.geopotential()
	cfsr.add_coast(res='c')
	cfsr.add_date()
	cfsr.add_title()

	# cfsr.thetaeq(level=975, clevels=range(270,355,5))
	# cfsr.windvector(jump=5, width=1.5, key=40)
	# # cfsr.geopotential()
	# cfsr.add_coast(res='c')
	# cfsr.add_title()


	cfsr.show()


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



