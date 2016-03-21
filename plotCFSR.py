#
# Visualization of CFSR data
#
# Raul Valenzuela
# August, 2015
#


# from datetime import datetime, timedelta
from glob import glob
import os
import CFSR


def plot(case=None, field=None, dates=None, ax=None):

    lonleft = -150
    lonright = -116
    lattop = 55
    latbot = 20
    domain = [lonleft, lonright, lattop, latbot]

    if case is None and dates is not None:
        basedir = '/home/rvalenzuela/CFSR'
        elem = os.listdir(basedir)
        dirs = [e for e in elem if 'case' in e]
        result = [glob(basedir+'/'+d+'/*nc') for d in dirs]
        flat = [val for sublist in result for val in sublist]
        datestr = [d.strftime('%Y%m%d%H') for d in dates]
        file = []
        for d in datestr:
            file.append([s for s in flat if d in s])
        files = [val for sublist in file for val in sublist]
        files.sort()
        dates.sort()

        cfsr = CFSR.create(domain=domain, dates=dates,
                           files=files, ax=ax, zboundary=600)

    else:
        str_case = str(case)
        homedir = os.path.expanduser('~')
        base_directory = homedir + '/CFSR/case'+str_case.zfill(2)
        print base_directory

        if dates is None:
            dates = get_dates(str_case)

        cfsr = CFSR.create(domain=domain, dates=dates,
                           directory=base_directory, ax=ax,
                           zboundary=600)

    if field == 'isotac':
        cfsr.isotac(level=300, clevels=range(40, 75, 5), cmap='jet')
        cfsr.windvector(level=300, jump=5, width=1.0,
                        scale=2.0, key=40, colorkey='r')
        cfsr.geopotential(level=300, clevels=range(830, 970, 10))
        cfsr.add_coast(res='c')
        cfsr.add_title()
        cfsr.add_location('bby')

    if field == 'absvort':
        cfsr.absvort(level=500, clevels=range(1, 6, 1), cmap='YlOrBr')
        cfsr.windvector(level=500, jump=5, width=1.0,
                        scale=2.0, key=40, colorkey='r')
        cfsr.geopotential(level=500, clevels=range(520, 600, 10))
        cfsr.add_coast(res='c')
        cfsr.add_title()
        cfsr.add_location('bby')

    if field == 'relhumid':
        cfsr.relhumid(level=700, clevels=range(90, 102, 2), cmap='YlGn')
        cfsr.windvector(level=700, jump=5, width=1.5,
                        scale=1.0, key=20, colorkey='r')
        cfsr.geopotential(level=700, clevels=range(280, 325, 5))
        cfsr.add_coast(res='c')
        cfsr.add_title()
        cfsr.add_location('bby')

    if field == 'temperature':
        cfsr.temperature(level=1000, vmin=0, vmax=20, cmap='jet')
        cfsr.windvector(jump=5, width=1.5,
                        scale=1.0, key=20, colorkey='white')
        cfsr.geopotential()
        cfsr.add_coast(res='c')
        cfsr.add_title()
        cfsr.add_location('bby')

    if field == 'geothick':
        cfsr.geothickness(top=500, bottom=1000,
                          clevels=range(5100, 5730, 30), cmap='RdBu_r')
        cfsr.windvector(level=1000, jump=4, width=0.5,
                        scale=1.5, key=20, colorkey='white')
        cfsr.surfpressure(clevels=range(980, 1034, 4))
        cfsr.add_coast(res='c')
        cfsr.add_title()
        cfsr.add_location('bby')

    if field == 'theta':
        cfsr.theta(level=1000, clevels=range(270, 298, 2), cmap='RdBu_r')
        cfsr.windvector(level=1000, jump=2, width=0.5,
                        scale=1.5, key=20, colorkey='b')
        cfsr.surfpressure(clevels=range(980, 1034, 4))
        cfsr.add_coast(res='c')
        cfsr.add_title()
        cfsr.add_location('bby')

    if field == 'thetaeq':
        cfsr.thetaeq(level=1000, clevels=range(260, 350, 5), cmap='RdBu_r')
        cfsr.windvector(level=1000, jump=3, width=0.7,
                        scale=1.5, key=20, colorkey='b')
        cfsr.surfpressure(clevels=range(980, 1034, 4))
        cfsr.add_coast(res='c')
        cfsr.add_title()
        cfsr.add_location('bby')

    if field == 'iwv_flux':
        cfsr.iwv_flux(clevels=range(300, 1700, 200), cmap='YlGn',
                      jump=8, width=1.1, scale=50, key=800, colorkey='k')
        cfsr.surfpressure(clevels=range(980, 1034, 4))
        cfsr.add_coast(res='c')
        cfsr.add_title()
        cfsr.add_location('bby')

    cfsr.show('ipython')


def get_dates(case):
    import pandas as pd

    cfsr_time = {
        '1': pd.date_range('1998-01-18 00:00', periods=6, freq='6H'),
        '2': pd.date_range('1998-01-26 00:00', periods=6, freq='6H'),
        '3': pd.date_range('2001-01-23 00:00', periods=6, freq='6H'),
        '7': pd.date_range('2001-02-17 06:00', periods=6, freq='6H'),
        '8': pd.date_range('2003-01-12 00:00', periods=6, freq='6H'),
        '9': pd.date_range('2003-01-21 00:00', periods=6, freq='6H'),
        '10': pd.date_range('2003-02-15 00:00', periods=6, freq='6H'),
        '11': pd.date_range('2004-01-09 00:00', periods=4, freq='6H'),
        '12': pd.date_range('2004-02-02 00:00', periods=4, freq='6H'),
        '13': pd.date_range('2004-02-16 00:00', periods=6, freq='6H'),
        '14': pd.date_range('2004-02-25 00:00', periods=4, freq='6H')
    }

    return cfsr_time[case]


# def plot_cross_sections():

#     cfsr.cross_section(field='thetaeq', orientation=['zonal', 38.30],
#                        clevels=range(276, 318, 2), cmap='RdBu_r')

#     cfsr.cross_section(field='q', orientation=['zonal', 38.30],
#                        clevels=range(0, 11, 1), cmap='RdBu_r')

#     cfsr.cross_section(field='U', orientation=['zonal', 38.30],
#                        clevels=range(-16, 18, 2), cmap='RdBu_r')

#     cfsr.cross_section(field='V', orientation=['zonal', 38.30],
#                        clevels=range(-16, 18, 2), cmap='RdBu_r')

#     cfsr.cross_section(field='thetaeq+V', orientation=['zonal', 40.],
#                        clevels=[range(276, 328, 2), range(-15, 20, 5)],
#                        cmap='RdBu_r')

#     cfsr.cross_section(field='thetaeq+U', orientation=['zonal', 38.30],
#                        clevels=[range(276, 328, 2), range(-15, 20, 5)],
#                        cmap='RdBu_r')

#     cfsr.cross_section(field='thetaeq+V', orientation=['zonal', 38.30],
#                        clevels=[range(276, 328, 2), range(-15, 20, 5)],
#                        cmap='RdBu_r')

#     cfsr.cross_section(field='thetaeq+V', orientation=['zonal', 35.],
#                        clevels=[range(276, 328, 2), range(-15, 20, 5)],
#                        cmap='RdBu_r')
