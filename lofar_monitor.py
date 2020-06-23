import matplotlib.pyplot as plt
from lofar_bst import Lofar_BST_357
import astropy.units as u
from astropy.units import Quantity
from sunpy.time import TimeRange
import datetime
import numpy as np
from astropy.time import Time, TimeDelta
import sys
import os




def savespectro(file_357,t0,t1, savefigure=1):
    time_range = TimeRange(t0,t1)

    bst_357 = Lofar_BST_357(file_357,trange=time_range)

    clip_int = Quantity([1,99]*u.percent)


    t0_plotting_spectro = datetime.datetime.now()
    bst_357.plot(clip_interval=clip_int, bg_subtract=True)
    fig = plt.gcf()
    fig.set_size_inches(11,8)
    t1_plotting_spectro = datetime.datetime.now()


    t0_saving_spectro = datetime.datetime.now()
    
    if savefigure == 1:
        file_357 = file_357[-27:]
        png_dir = os.getcwd() + '/monitor'
        plt.savefig(f'{png_dir}/{file_357[:-4]}_{t0.datetime.hour:02}{t0.datetime.minute:02}_{t1.datetime.hour:02}{t1.datetime.minute:02}.png',dpi=300)
    plt.close()
    t1_saving_spectro = datetime.datetime.now()

    print(f'plotting_spectro:   {t1_plotting_spectro-t0_plotting_spectro}')
    print(f'saving_spectro:   {t1_saving_spectro-t0_saving_spectro}')
    return 0


def savelightcurve(light,times,fname, savefigure=1):
    light = np.array(np.sum(light, axis=0))
    times = times.datetime
    t0 = times[0]
    t1 = times[-1]


    obs_start = fname.split("_bst")[0][-15:]
    obs_start = Time.strptime(obs_start, "%Y%m%d_%H%M%S")
    date = obs_start.datetime



    plt.figure()
    plt.plot(times, light)
    plt.title(f'Lightcurve I-LOFAR MODE 357 Solar Observation')
    plt.xlabel(f'Observation Start Time {date.year} - {date.month} - {date.day}  {date.hour}:{date.minute}:{date.second}  UTC')
    plt.ylabel(f'Sum of all antenna correlations ')
    if savefigure == 1:
        fname = fname[-27:]
        png_dir = os.getcwd() + '/monitor'
        plt.savefig(f'{png_dir}/{fname[:-4]}_{t0.hour:02}{t0.minute:02}_{t1.hour:02}{t1.minute:02}_lightcurve.png',dpi=300 )
    plt.close()
    return 0





if __name__ == "__main__":
    filename = sys.argv[1]

    debugg = 1
    t_start =datetime.datetime.now()

    file_357 = filename[:-5]

    bst_357_X = Lofar_BST_357(file_357+'X.dat')
    times_X = bst_357_X.times
    t0 = times_X[-10*60]
    t1 = times_X[-1]

    png_dir = os.getcwd()+'/monitor'


    if not os.path.exists(png_dir):
        os.makedirs(png_dir)

    light_X = bst_357_X.data
    print(light_X.shape)



    bst_357_Y = Lofar_BST_357(file_357+'Y.dat')
    times_Y = bst_357_Y.times
    light_Y = bst_357_Y.data

    
    
    if len(times_X)> 600:
        savelightcurve(light_X[:,-600:-1],times_X[-600:-1],file_357+'X.dat')
        savelightcurve(light_Y[:,-600:-1],times_Y[-600:-1],file_357+'Y.dat')
        
        savespectro(file_357+'X.dat',t0,t1)
        savespectro(file_357+'Y.dat',t0,t1)



    t_end = datetime.datetime.now()

    if debugg == 1:
        print(f"lofar monitor: ")
        print(f"Start:  {t_start}")
        print(f"End:    {t_end}")
        print(f'Time elapsed:  {t_end-t_start}')


