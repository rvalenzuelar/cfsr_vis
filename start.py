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
	# lonleft=-180
	# lonright=0
	# lattop=90
	# latbot=0
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
	cfsr.isotac()
	cfsr.windvector()
	cfsr.geopotential()
	# addCFSR.ancillary()

	# cfsr.initialize_plot(level=500)
	# cfsr.absvort()
	# cfsr.windvector()
	# cfsr.geopotential()

	# cfsr.initialize_plot(level=700)
	# cfsr.relhumid()
	# cfsr.windvector()
	# cfsr.geopotential()

	# cfsr.initialize_plot(level=1000)
	# cfsr.temperature()
	# cfsr.windvector()
	# cfsr.geopotential()
	# addCFSR.ancillary()

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



