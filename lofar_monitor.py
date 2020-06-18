import matplotlib.pyplot as plt
from lofar_bst import Lofar_BST_357
import astropy.units as u
from astropy.units import Quantity
from sunpy.time import TimeRange
import datetime


t_start =datetime.datetime.now()

file_357 = '20200602_071428_bst_00X.dat'

debugg = 1




if debugg == 1:        
    year = 2020
    month = 6
    day = 2
    hour = 7
    minutes = 27
else:        
    year = t_start.year
    month = t_start.month
    day = t_start.day
    hour = 7
    minutes = 27






dt = datetime.timedelta(minutes = 10)
t1 = datetime.datetime(year,month,day,hour,minutes)
t0 = t1 - dt


time_range = TimeRange(f'{t0.year}/{t0.month:02}/{t0.day:02} {t0.hour}:{t0.minute}',
    f'{t1.year}/{t1.month:02}/{t1.day:02} {t1.hour}:{t1.minute}')




bst_357 = Lofar_BST_357(file_357,trange=time_range)

clip_int = Quantity([1,99]*u.percent)

bst_357.plot(clip_interval=clip_int, bg_subtract=True)
fig = plt.gcf()
fig.set_size_inches(11,8)


plt.savefig(f'{file_357[:-4]}_{t0.hour:02}{t0.minute:02}_{t1.hour:02}{t1.minute:02}.png',dpi=300)
plt.show()


t_end = datetime.datetime.now()


print(f"lofar monitor: ")
print(f"Start:  {t_start}")
print(f"End:    {t_end}")
print(f'Time elapsed:  {t_end-t_start}')






