
from mpl_toolkits.basemap import Basemap


def ancillary():
	return True

def coast():
	M = Basemap(projection='cyl',
				llcrnrlat=self.extent['by'],
				urcrnrlat=self.extent['ty'],
				llcrnrlon=self.extent['lx'],
				urcrnrlon=self.extent['rx'],
				resolution='i')

	coastline = M.coastpolygons

	xline= coastline[1][0][:]
	yline= coastline[1][1][:]

	axis.plot(x, y,
		color=self.coastColor,
		linewidth=self.coastWidth,
		linestyle=self.coastStyle)