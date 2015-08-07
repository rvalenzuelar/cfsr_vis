
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
	delta=timedelta(hours=0)
	dates=get_dates(start,end,delta)

	directory='/home/rvalenzuela/CFSR/case03'

	cfsr=plotCFSR.create()
	cfsr.config(domain=domain, dates=dates,level=300,directory=directory)

	cfsr.isotac()

	

	# addCFSR.ancillary()

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



