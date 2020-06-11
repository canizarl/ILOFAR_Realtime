""" 

    bst_dynamic_spectra.py
    Displays dynamic spectra from ILOFAR bst data

    Supported instruments:
        LOFAR        -- bst .dat file




    Some notes on how I code.
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!   Denotes to be changed
   -----------------------------------------   Denotes module heading to be turned into function
   iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii   Denotes information
   aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa   ADD code. Plans for supporting function


"""


import numpy as np
import matplotlib.pyplot as plt
from matplotlib import dates
from datetime import datetime, timedelta
import os


def sb_to_freq(sb, mode):
    """
        simple function to convert ilofar subbands into frequencies
        input:
            sb: int subbands (488 for mode 357)
            mode: int mode 3 , 5 or 7.... typically. supports 4 and 6 too. 
        output:
            freqs: 1d vector with frequencies for y axis

    """
    if mode == 3:
        nyq_zone = 1
        clock = 200 #MHz
    elif mode == 4:
        nyq_zone = 1
        clock = 200 #MHz
    elif mode == 5:
        nyq_zone = 2
        clock = 200 #MHz
    elif mode == 6:
        nyq_zone = 3
        clock = 160 #MHz
    elif mode == 7:
        nyq_zone = 3
        clock = 200 #MHz
    else:
        print("ERROR mode not supported")
        return 0

    
    freq = (nyq_zone-1+sb/512)*(clock/2)
    return freq #MHz

def backsub(data, percentile=1.0):
    # written by Eoin Carley
    # Get time slices with standard devs in the bottom nth percentile.
    # Get average spectra from these time slices.
    # Devide through by this average spec.
    # Expects (row, column)

    print('Performing background subtraction.')
    data = np.log10(data)
    data[np.where(np.isinf(data)==True)] = 1.0
    data[np.where(np.isnan(data)==True)] = 1.0
    
    data_std = np.std(data, axis=0)
    data_std = data_std[np.nonzero(data_std)]
    min_std_indices = np.where( data_std < np.percentile(data_std, percentile) )[0]
    min_std_spec = data[:, min_std_indices]
    min_std_spec = np.mean(min_std_spec, axis=1)
    data = np.transpose(np.divide( np.transpose(data), min_std_spec))
    print('Background subtraction finished.')

    #Alternative: Normalizing frequency channel responses using median of values.
        #for sb in np.arange(data.shape[0]):
        #       data[sb, :] = data[sb, :]/np.mean(data[sb, :])

    return data




def make_spectro(bstfile):
    """
        Takes a .dat file from lofar bst data and 
        outputs dynamic spectra information

        input:
            bstfile: str PATH to the file

        output:
            data: 2d matrix of dynamic spectra 
            freqs: 1d vector with frequencies for y axis
            t_arr: 1d vector with times for x axis

    """

    rawdata=np.fromfile(bstfile)
    file_size=os.path.getsize(bstfile)
    lendata=len(rawdata)
    ndatapoints=file_size/len(rawdata)

    print(f"lendata = {lendata}")
    print(f"file_size = {file_size}")
    bitmode=file_size/lendata
    print(f"file_size = {bitmode}")


    #Reshape data
    subbands = 488
    beamlets = subbands#rawdata.shape[1]
    data = rawdata.reshape(-1,beamlets)
    print(f"data shape: {data.shape}")


    if int(bitmode) == 8:
        #bitmode is 8 therefore 488 subbands (not always though)
        t_len = data.shape[0]/subbands
        print("Time samples:",t_len )
    else:
        print(f'ERROR: bitmode is not 8, different bitmodes are not supported yet')



    #  iiiiiiiiiiiiiiiiiiiiii    #
    "  FREQUENCY VECTOR          "
    #  iiiiiiiiiiiiiiiiiiiiii    #
    freqs = []
    sbs = np.arange(54,452+2,2)
    freqs = sb_to_freq(sbs,mode = 3)

    sbs = np.arange(54,452+2,2)
    freqs = np.concatenate([freqs,sb_to_freq(sbs,mode = 5)])
    sbs = np.arange(54,228+2,2)
    freqs = np.concatenate([freqs,sb_to_freq(sbs,mode = 7)])



    #  iiiiiiiiiiiiiiiiiiiiii    #
    "  TIME VECTOR               "
    #  iiiiiiiiiiiiiiiiiiiiii    #
    obs_start = bstfile[len(bstfile)-27:len(bstfile)-12]
    obs_start = datetime.strptime(obs_start, "%Y%m%d_%H%M%S")
    obs_len  = timedelta(seconds = data.shape[0])

    obs_end = obs_start + obs_len
    t_lims = [obs_start, obs_end]
    t_lims = dates.date2num(t_lims)
    print(t_lims)

    #you only really need start and end time for imshow but we'll do a full array anyway
    t_arr = np.arange(0,data.shape[0])
    t_arr = t_arr*timedelta(seconds=1)
    t_arr = obs_start+t_arr
    t_arr = dates.date2num(t_arr)

    print(obs_start)
    return data.T,freqs, t_arr


def plt_dynSpec(data,freqs,epoch,pol,savefile='no'):
    '''
    Plots dynamic spectra.
    Expects:
        data: 2d matrix of dynamic spectra 
        freqs: 1d vector with frequencies for y axis
        epoch: 1d vector with times for x axis
        pol: char X or Y to display which polarisation is it
        savefile: str 'yes' or 'no' to savefile or not 

    '''



    #  iiiiiiiiiiiiiiiiiiiiii    #
    "  Settings                  "
    #  iiiiiiiiiiiiiiiiiiiiii    #
    datamin = np.percentile(data,1)
    datamax = np.percentile(data, 99)
    colormap = 'plasma'
    date_obs = dates.num2date(epoch[0]) 
    


    #  iiiiiiiiiiiiiiiiiiiiii    #
    "  Plot                  "
    #  iiiiiiiiiiiiiiiiiiiiii    #
    plt.figure()
    plt.pcolormesh(epoch, freqs, data,
                    vmin=datamin, vmax=datamax,
                    cmap = colormap)
    plt.title(f'LOFAR MODE 357 - {pol} - IE613 (Birr) - {date_obs.year} - {date_obs.month:02} - {date_obs.day:02}')
    plt.xlabel('Time (UT)')
    plt.ylabel('Frequency MHz')
    plt.gca().invert_yaxis()
    # aaaaaaaa #
    " change x labels format to time format "
    # aaaaaaaa #


    plt.show()




    #  aaaaaaaaaaaaaaaaaaaaaa    #
    "  Savefile                  "
    #  aaaaaaaaaaaaaaaaaaaaaa    #
    if savefile=='yes':
        print('SAVEFILE NOT  SUPPORTED YET')







if __name__ == "__main__":
 
    "  aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa   "
    #       ADD command line arguments             #
    "  aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa  "
    # filename
    # usage
    # verbose probably just for debbugging mode





    "  iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii    "
    #             Read in data                      #
    "  iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii    "
    bstfile = "20200602_071428_bst_00X.dat"

    pol = bstfile[-5]    # polarisation  X or Y. knows from file name . 






    "  iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii    "
    #             Extract data                      #
    "  iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii    "
    data,freqs,epoch = make_spectro(bstfile)

 
 
    "  iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii    "
    #        Bacground subtract data                #
    "  iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii    "
    spectro = backsub(data,percentile=1)



    "  iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii    "
    #        Plot dynamic spectra                   #
    "  iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii    "
    plt_dynSpec(spectro,freqs, epoch, pol)


