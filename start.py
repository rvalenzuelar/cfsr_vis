#
# Visualization of CFSR data
#
# Raul Valenzuela
# August, 2015
#


from datetime import datetime,timedelta

import plotCFSR
import addCFSR

def main():

	lonleft=-150
	lonright=-116
	lattop=55
	latbot=20	

	domain=[lonleft,lonright,lattop,latbot]

	start=datetime(2001,1,22,18)
	end=datetime(2001,1,24,0)
	delta=timedelta(hours=6)
	dates=get_dates(start,end,delta)

	# directory='/home/rvalenzuela/CFSR/case03'
	directory='/Users/raulv/Desktop/CFSR'

	cfsr=plotCFSR.create()
	cfsr.config(domain=domain, dates=dates, directory=directory)

	cfsr.initialize_plot(level=300)
	cfsr.isotac(cmap=range(40,70,5))
	cfsr.windvector()
	cfsr.geopotential()
	# cfsr.add_coast()

	cfsr.initialize_plot(level=500)
	cfsr.absvort(cmap=range(1,6,1))
	cfsr.windvector()
	cfsr.geopotential()

	cfsr.initialize_plot(level=700)
	cfsr.relhumid(cmap=range(50,110,10))
	cfsr.windvector()
	cfsr.geopotential()

	cfsr.initialize_plot(level=1000)
	cfsr.temperature(vmin=0,vmax=20)
	cfsr.windvector()
	cfsr.geopotential()


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



