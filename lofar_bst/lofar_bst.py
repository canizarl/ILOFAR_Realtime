#!/usr/bin/env python

# Developers:
# Pearse Murphy : pearse.murphy@dias.ie
# Alberto Canizares: canizares@cp.dias.ie



# MODIFICATIONS
# 2020-07-08  Alberto  _get_data(self): ----> added while loop to make sure data can be reshaped to 488
# 2020-08-06  Alberto : plot 		date_format = dates.DateFormatter("%H:%M") Seconds removed from x axis to avoid overlapping.

"""
Modified to be used in ilofar monitor.

"""


import copy

import astropy.units as u
import matplotlib.pyplot as plt
import numpy as np

from astropy.time import Time, TimeDelta
from astropy.visualization import AsymmetricPercentileInterval
from matplotlib import dates
from sunpy.time import TimeRange

def sb_to_freq(sb, obs_mode):
	"""
	Converts LOFAR single station subbands to frequency
	Returns frequency as astropy.units.Quantity (MHz)
	Inputs: subband number, observation mode (3, 5 or 7)
	"""
	nyq_zone_dict = {3:1, 5:2, 7:3}
	nyq_zone = nyq_zone_dict[obs_mode]
	clock_dict = {3:200, 4:160, 5:200, 6:160, 7:200} #MHz
	clock = clock_dict[obs_mode]
	freq = (nyq_zone-1+sb/512)*(clock/2)
	return freq*u.MHz #MHz

class Lofar_BST:
	"""
	Class to read and plot I-LOFAR beamformed statistics (BST) data
	Required arguments: bst_file = File name,
						sbs = subbands observed,
						obs_mode = observation mode
	Optional arguments: trange = time range (sunpy.time.TimeRange), 
						frange = frequency range (2 element list/array with start and end frequency as astropy.units.Quantity),
						bit_mode = bit mode (usually 4, 8 or 16),
						integration = integration time (seconds)
	"""
	def __init__(self,bst_file, sbs, obs_mode, trange=None, frange=None, bit_mode=8, integration=1):
		self.bst_file = bst_file
		self.sbs = sbs
		self.obs_mode = obs_mode
		self.trange = trange
		self.frange = frange
		self.bit_mode = bit_mode
		obs_start = bst_file.split("_bst")[0][-15:]
		self.obs_start = Time.strptime(obs_start, "%Y%m%d_%H%M%S")
		self.integration = TimeDelta(integration, format="sec")
		self._get_data()
		self.data = self.data.T

	def __repr__(self):
		return "I-LOFAR mode {} observation".format(self.obs_mode) \
				+ "\n Time range:" + str(self.times[0]) + " to " + str(self.times[-1]) \
				+ "\n Frequency range:" + str(self.freqs[0]) + " to " + str(self.freqs[-1])

	def _get_data(self):
		"""
		Read in data from BST file and calculate time and frequency
		"""
		data = np.fromfile(self.bst_file)
		t_len = data.shape[0]/len(self.sbs)

		# Make sure that data can be reshaped to 488
		while len(data)%488!=0:
			data = data[:-1]
			



		self.data = data.reshape(-1, len(self.sbs))
		tarr = np.arange(t_len) * self.integration
		self.times = self.obs_start + tarr
		if self.trange is not None:
			t_start_end = []

			for time in (self.trange.start, self.trange.end):
				diff_arr = np.abs(time-self.times)
				min_val = np.min(diff_arr)
				t_start_end.append(np.where(diff_arr == min_val.value)[0][0])
			t_start, t_end = t_start_end
		else:
			t_start = 0
			t_end = None
		self.times = self.times[t_start:t_end]
		self.freqs = sb_to_freq(self.sbs, self.obs_mode)
		if self.frange is not None:
			f_start_end = []
			for freq in self.frange:
				diff_arr = np.abs(freq.to(u.MHz)-self.freqs)
				min_val = np.min(diff_arr)
				f_start_end.append(np.where(diff_arr == min_val)[0][0])
			f_start, f_end = f_start_end
		else:
			f_start = 0
			f_end = None
		self.freqs = self.freqs[f_start:f_end]
		self.data = self.data[t_start:t_end, f_start:f_end]
	def plot(self, ax=None, title=None, bg_subtract=False, scale="linear", clip_interval: u.percent=None, pol=''):
		"""
		Plot dynamic spectrum for whole data
		Assume first 10 seconds are pure background for background subtraction
		TODO: 
		Tweak background subtraction
		"""
		if not ax:
			fig, ax = plt.subplots()
		data = copy.deepcopy(self.data)
		if bg_subtract:
			data = (data.T/np.mean(data[:,:10],axis=1)).T
		imshow_args = {}
		date_format = dates.DateFormatter("%H:%M")
		if scale == "log":
			data = np.log10(data)
		if clip_interval is not None:
			if len(clip_interval) == 2:
				clip_percentages = clip_interval.to('%').value
				vmin, vmax = AsymmetricPercentileInterval(*clip_percentages).get_limits(data)
			else:
				raise ValueError("Clip percentile interval must be specified as two numbers.")
			imshow_args["vmin"] = vmin
			imshow_args["vmax"] = vmax

		ret = ax.imshow(data, aspect="auto", 
						extent=[self.times.plot_date[0], self.times.plot_date[-1], self.freqs.value[-1], self.freqs.value[0]],
						**imshow_args)
		ax.xaxis_date()
		ax.xaxis.set_major_formatter(date_format)
		if title:
			ax.set_title(title)
		else:
			ax.set_title("I-LOFAR Mode {} Solar Observation / {} polarization".format(self.obs_mode, self.pol))
		ax.set_xlabel("Start Time " + self.obs_start.iso[:-4] + "UTC")
		ax.set_ylabel("Frequency (MHz)")
		return ret

class Lofar_BST_357(Lofar_BST):
	"""
	Class for reading and plotting mode 357 observations from I-LOFAR
	This class uses the following assumptions:
	357 mode is always done with 488 subbands
	The subband numbers are defined as
	Mode 3: 54 -> 452 in steps of 2
	Mode 5: 54 -> 452 in steps of 2
	Mode 7: 54 -> 288 in steps of 2
	The integration time is always 1 second
	The target source is always the sun
	inputs: bst_file = filename
			trange = Optional: time range (sunpy.time.TimeRange)
			frange = Optional: frequency range (2 element list/array/tuple astropy.units.Quantity)
	"""
	def __init__(self, bst_file, trange=None, frange=None, pol=''):
		"""
		Initialise super with dummy sbs, obs_mode and frange arguments
		Insert spacing between modes as masked region in data
		"""
		self.bst_file = bst_file
		self.trange = trange
		self.frange = frange
		super().__init__(self.bst_file, sbs=np.arange(488), obs_mode=3, trange=self.trange, frange=None, bit_mode=8, integration=1)
		self.frange = frange
		self.pol = pol
		self._frequency_correction()
	
	def _frequency_correction(self):	
		sbs = np.array((np.arange(54,454,2),np.arange(54,454,2),np.arange(54,230,2)))
		blank_sbs = np.array((np.arange(454,512,2),np.arange(0,54,2),np.arange(454,512,2),np.arange(0,54,2)))
		obs_mode = np.array((3,5,7))
		blank_obs_mode = np.array((3,5,5,7))
		freqs = np.array([sb_to_freq(sb,mode) for sb,mode in zip(sbs, obs_mode)])
		blank_freqs = np.array([sb_to_freq(sb,mode) for sb,mode in zip(blank_sbs, blank_obs_mode)])
		
		self.sbs=np.concatenate((sbs[0], blank_sbs[0], blank_sbs[1], sbs[1],
									blank_sbs[2], blank_sbs[3], sbs[2]))

		self.freqs=np.concatenate((freqs[0], blank_freqs[0], blank_freqs[1], freqs[1],
									blank_freqs[2], blank_freqs[3], freqs[2]))
		
		
		blank_data = np.zeros((self.freqs.shape[0],self.data.shape[1]))
		#1st 200 sbs mode 3, blank, next 200 sbs mode 5, blank, last 88 sbs mode 7  
		blank_data[:200,:] = self.data[:200,:]
		blank_len_0 = len(blank_freqs[0]) + len(blank_freqs[1])
		blank_data[200 + blank_len_0:400 + blank_len_0,:] =self.data[200:400,:]
		blank_len_1 = len(blank_freqs[2]) + len(blank_freqs[3])
		blank_data[400 + blank_len_0 + blank_len_1 :,:] =self.data[400:,:]
		self.data = np.ma.masked_equal(blank_data, 0)
		self.obs_mode = 357

		if self.frange is not None:
			f_start_end = []
			for freq in self.frange:
				diff_arr = np.abs(freq.to(u.MHz)-self.freqs)
				min_val = np.min(diff_arr)
				f_start_end.append(np.where(diff_arr == min_val)[0][0])
			f_start, f_end = f_start_end
		else:
			f_start = 0
			f_end = None
		self.freqs = self.freqs[f_start:f_end]
		self.data = self.data[f_start:f_end,:]		