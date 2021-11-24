"""
Uses lofar_bst.py (version modified by Alberto Canizares
https://github.com/canizarl/ILOFAR_Realtime

Used in ILOFAR station.
Collects data from lgc to display near real time dynamic spectra of the current observations.
Supports:
357 solar bst observations.

Changes:
    01/12/2020 : Alberto : no longer sends pngs from this script. Sending from bash.


"""

import matplotlib as mpl

mpl.use('Agg')  # Comment this out if you want to display anything
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

plt.rcParams.update({'font.size': 16})
import sys
import os
import math

lgc = 1

if lgc == 0:
    # PATH to bst file location
    pathtothisfile = '/Users/albertocanizares/OneDrive/Work/0_PhD/Projects/ILOFAR_REALTIME/Scripts/lofar_bst'
    sys.path.append(pathtothisfile)
    print(pathtothisfile)

if lgc == 1:
    # PATH to bst file location
    pathtothisfile = '/home/ilofar/Scripts/Python/MonitorRealtime'
    sys.path.append(pathtothisfile)
    print(pathtothisfile)

from lofar_bst import Lofar_BST_357
import astropy.units as u
from astropy.units import Quantity
from sunpy.time import TimeRange
import datetime
import numpy as np
from astropy.time import Time, TimeDelta


def savespectro(file_357, t0, t1, save_dir, pol, savefigure=1):
    """
    Sacvespectro:
        file_357 - str: name of file
        t0 - datetime : Start time
        t1 - datetime : end time
        save_dir - str: path to directory to save figures
        savefigure - int : leave as 1 to save figures

        This function uses LOFAR_BST_357 to extract data from a file, and time range. Gnerates dynamic spectra and saves
        it into a directory.

    """

    # Generates the time range for LOFAR_BST_357
    time_range = TimeRange(t0, t1)

    # LOAD DATA using Lofar_BST_357
    bst_357 = Lofar_BST_357(file_357, trange=time_range, pol=pol)

    # Adjust the levels for the plots
    clip_int = Quantity([50, 98] * u.percent)

    # Start timer to keep track of computational expense
    t0_plotting_spectro = datetime.datetime.now()

    # Generates the dynamic spectra
    bst_357.plot(clip_interval=clip_int, bg_subtract=True)

    # Generates a figure of the dynamic spectra
    fig = plt.gcf()
    fig.set_size_inches(11, 8)

    # End timer to keep track of computational expense
    t1_plotting_spectro = datetime.datetime.now()

    # Start timer to keep track of computational expense
    t0_saving_spectro = datetime.datetime.now()

    # Saving the plot
    if savefigure == 1:
        file_357 = file_357[-27:]
        png_dir = save_dir

        spectro_name = file_357[:-4] + '_' + str(t0.datetime.hour).zfill(2) + str(t0.datetime.minute).zfill(
            2) + '_' + str(t1.datetime.hour).zfill(2) + str(t1.datetime.minute).zfill(2) + '.png'
        plt.savefig(png_dir + '/' + spectro_name, dpi=300)
        pathtospectro = png_dir + '/' + spectro_name
        pngname = spectro_name[:-4]

        # No longer sending from here.
    # if lgc == 1:
    #    print("Sending "+ pngname + " to monitor webserver")
    #    #os.system("curl -F file=@"+pathtospectro+" https://lofar.ie/operations-monitor/post_image.php?img="+pngname)
    #    os.system("curl -F file=@"+pathtospectro+" https://lofar.ie/operations-monitor/post_image.php?img=spectro1"+pol+".png")
    #    print(pathtospectro)

    plt.close()
    t1_saving_spectro = datetime.datetime.now()

    print("plotting_spectro:   " + str(t1_plotting_spectro - t0_plotting_spectro))
    print("saving_spectro:   " + str(t1_saving_spectro - t0_saving_spectro))
    return 0


def savelightcurve(light, times, freqs, fname, save_dir, pol, savefigure=1):
    """
        light :  dynamic spectra
        time  :  epoch
        freqs :  list with 2D items. first is the frequency value, the second one is index, i.e. where to find it in light
        fname : file name
        save_dir: where is it saved
        pol: char:  polarisation X or Y
        savefigure : 1 = yes  0 = no

        This function chooses a set of frequencies in dynamic spectra and plots them as lightcurves.
    """

    # for now use 4 frequencies
    np.shape(light)
    light1 = np.array(light[int(freqs[0, 1]), :])
    light2 = np.array(light[int(freqs[1, 1]), :])
    light3 = np.array(light[int(freqs[2, 1]), :])
    light4 = np.array(light[int(freqs[3, 1]), :])

    # Normalise lightcurves
    light1_ave = np.average(light1)
    light1 = np.divide(light1, light1_ave)

    light2_ave = np.average(light2)
    light2 = np.divide(light2, light2_ave)

    light3_ave = np.average(light3)
    light3 = np.divide(light3, light3_ave)

    light4_ave = np.average(light4)
    light4 = np.divide(light4, light4_ave)

    # light = np.array(np.sum(light, axis=0))
    times = times.datetime
    t0 = times[0]
    t1 = times[-1]

    obs_start = fname.split("_bst")[0][-15:]
    obs_start = Time.strptime(obs_start, "%Y%m%d_%H%M%S")
    date = obs_start.datetime

    fig, ax = plt.subplots()
    fig.set_size_inches(11, 8)
    ax.plot(times, light1, 'r-', label=str(freqs[0, 0]) + "MHz")
    ax.plot(times, light2, 'b-', label=str(freqs[1, 0]) + "MHz")
    ax.plot(times, light3, 'g-', label=str(freqs[2, 0]) + "MHz")
    ax.plot(times, light4, 'k-', label=str(freqs[3, 0]) + "MHz")

    ax.set_title('Lightcurve I-LOFAR MODE 357 Solar Observation ' + pol + ' polarization')
    ax.set_xlabel(
        'Observation Start Time' + str(date.year) + ' - ' + str(date.month) + ' - ' + str(date.day) + '  ' + str(
            date.hour) + ':' + str(date.minute) + ':' + str(date.second) + '  UTC')
    ax.set_ylabel('Arbitrary units')
    ax.legend(loc='upper left')
    ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=2))  # to get a tick every 2 minutes
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))  # optional formatting

    if savefigure == 1:
        fname = fname[-27:]
        png_dir = save_dir
        # plt.savefig(f'{png_dir}/{fname[:-4]}_{t0.hour:02}{t0.minute:02}_{t1.hour:02}{t1.minute:02}_lightcurve.png',dpi=300 )

        lightcurve_name = fname[:-4] + '_' + str(t0.hour).zfill(2) + str(t0.minute).zfill(2) + '_' + str(t1.hour).zfill(
            2) + str(t1.minute).zfill(2) + '_lightcurve.png'

        fig.savefig(png_dir + '/' + lightcurve_name, dpi=300)

        pathtolightcurve = png_dir + '/' + lightcurve_name
        pngname = lightcurve_name[:-4]

        # No longer sending from here.
        # if lgc == 1:
        #    print("Sending "+ pngname + " to monitor webserver")
        #    #os.system("curl -F file=@"+pathtolightcurve+" https://lofar.ie/operations-monitor/post_image.php?img="+pngname)
        #    os.system("curl -F file=@"+pathtolightcurve+" https://lofar.ie/operations-monitor/post_image.php?img=lc1"+pol+".png")

    plt.close()
    return 0


def find_nearest(array, value):
    """
    Finds the nearest value in an array.
    Useful in this context for finding a particular frequency giving it an approximate desired one.
    """
    idx = np.searchsorted(array, value, side="left")
    if idx > 0 and (idx == len(array) or math.fabs(value - array[idx - 1]) < math.fabs(value - array[idx])):
        return array[idx - 1], idx
    else:
        return array[idx], idx


if __name__ == "__main__":
    # input the filename from command line
    if len(sys.argv) >= 2:
        filename = sys.argv[1]  # path to data file
    else:
        filename = "data/20200602_071428_bst_00X.dat"  # this is for testing
    debugg = 1
    t_start = datetime.datetime.now()

    file_357 = filename[:-5]  # this gets rid of 'X.dat' from the file to make sure it works if the Y pol is given

    # lightcurve frequencies
    lcv_freqs = [50, 70, 150, 220]

    # Open the .dat file for the X pol
    bst_357_X = Lofar_BST_357(file_357 + 'X.dat')
    # Get the epoch
    times_X = bst_357_X.times

    # Get the range from last ten mins to now
    # Get the last 10 mins
    t0 = times_X[-10 * 60]
    # the last data point
    t1 = times_X[-1]

    # getting the data for X polarization
    light_X = bst_357_X.data
    # getting the frequencies for X polarization
    freqs_X = np.array(bst_357_X.freqs)

    # find the indices of the corresponding frequencies for extraction from dynamic spectra
    freqs_idx = list()
    for item in lcv_freqs:
        freqs_idx.append(find_nearest(freqs_X, item))

    freqs_idx = np.array(freqs_idx)

    print(light_X.shape)

    # Default output directory is a ./monitor/YYYY.MM.DD
    # otherwise manually add output directory.
    if len(sys.argv) <= 2:
        png_dir = os.getcwd() + '/monitor/' + str(t0.datetime.year) + '.' + str(t0.datetime.month).zfill(2) + '.' + str(
            t0.datetime.day).zfill(2)
    else:
        png_dir = sys.argv[2]

    if not os.path.exists(png_dir):
        os.makedirs(png_dir)

    # Now the y polarization
    bst_357_Y = Lofar_BST_357(file_357 + 'Y.dat')
    times_Y = bst_357_Y.times
    light_Y = bst_357_Y.data

    freqs_Y = np.array(bst_357_Y.freqs)

    freqs_idy = list()
    for item in lcv_freqs:
        freqs_idy.append(find_nearest(freqs_Y, item))

    freqs_idy = np.array(freqs_idy)

    # this is to make sure the file has 10 mins of data
    if len(times_X) > 600:
        savelightcurve(light_X[:, -600:-1], times_X[-600:-1], freqs_idx, file_357 + 'X.dat', png_dir, 'X')
        savelightcurve(light_Y[:, -600:-1], times_Y[-600:-1], freqs_idy, file_357 + 'Y.dat', png_dir, 'Y')

        savespectro(file_357 + 'X.dat', t0, t1, png_dir, 'X')
        savespectro(file_357 + 'Y.dat', t0, t1, png_dir, 'Y')

    t_end = datetime.datetime.now()

    if debugg == 1:
        print("lofar monitor: ")
        print("Start:  " + str(t_start))
        print("End:    " + str(t_end))
        print("Time elapsed:  " + str(t_end - t_start))


