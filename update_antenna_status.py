#!/usr/bin/env python

'''
The following code requests a .JSON file from proxy.lofar.eu containing 
information on any antenna within the I-LOFAR array that return an anomalous 
signal when a station test is run. It has been inserted within the I-LOFAR
station monitor python code on the LGC which is run frequently to give a
close-to-live update on the status of the array.
'''

# -----
# The relevent libraries are imported below.
# The urllib package accesses the .JSON file at proxy.lofar.eu which has information on all I-LOFAR stations.

import numpy as np
import scipy as sp
import json
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import urllib.request

debug = 1

# ----- 
# unest iterates through the dictionary object to find the tiles with errors and returns the error.
def unest(data, key):
    if key in data.keys():
        return data.get(key)
    else:
        for dkey in data.keys():
            if isinstance(data.get(dkey), dict):
                return unest(data.get(dkey), key)
            else:
                continue

# -----
# Write the HBA tiles with errors and their errors to a log file which javascript can then access
def write_to_HBA_log(tile, error):
    with open('HBA_numbers.txt', 'a') as f:
        f.write(tile + '+' + error + ',')

# -----
# Write the LBA tiles with errors and their errors to a log file which javascript can then access
def write_to_LBA_log(antenna, error):
    with open('LBA_numbers.txt', 'a') as f:
        f.write(antenna + '+' + error + ',')

todays_date = (datetime.today()- timedelta(days=0)).strftime('%Y-%m-%d')
n_days_ago =(datetime.today() - timedelta(days=7)).strftime('%Y-%m-%d')

# -----
# The url for access to the most recent json file, takes data from the last 7 days
# If fewer days are specified there is a chance the station has been in local mode,
# the json file may in that case return an error. Code to be written to account for this.
url_scraping = 'https://proxy.lofar.eu/lofmonitor/api/view/ctrl_station_component_errors?format=json&station_name=IE613C&from_date='+n_days_ago+'&to_date='+todays_date+'&error_types='
# -----
# Request .JSON file, download and create dictionary called 'data' with content of .JSON

try:
    with urllib.request.urlopen(url_scraping) as url:
        data = json.loads(url.read().decode())
        
        # -----
        # Save the json file to a txt or csv or something for access later (write code)
       
        # print('JSON data successfully downloaded and parsed as', type(data))

except Exception as e:
    print('Error, unable to request current JSON file, reverting to last available data. Error:', e)
    # -----
    # Access the last saved json file (write code)


# -----
# Define known paths to the error locations for HBA and LBA within the dictionary
HBA_data_json = data['HBA']['errors'][0]
LBA_data_json = data['LBH']['errors'][0]

# -----
# Clear the log files for updating
open('HBA_numbers.txt', 'w').close()
open('LBA_numbers.txt', 'w').close()

# -----
# Below two for loops find the most recent errors for the HBAs from the json dictionary
                                
for tile in HBA_data_json['component_errors']:
    error = unest(HBA_data_json['component_errors'][str(tile)], 'error_type')
    write_to_HBA_log(tile, error)
    if debug==1:
        print('tile hba_data_json works')
    
for tile in HBA_data_json["status"]:
    error = unest(HBA_data_json["status"][str(tile)], 'status')
    write_to_HBA_log(tile, error)

# -----
# The two 'for' loops below iterate through the json dictionary to find the most recent antenna errors. 

for antenna in LBA_data_json['component_errors']:
    error = unest(LBA_data_json['component_errors'][str(antenna)], 'error_type')
    write_to_LBA_log(antenna, error)
    
for antenna in LBA_data_json['status']:
    error = unest(LBA_data_json['status'][str(antenna)], 'status')
    write_to_LBA_log(antenna, error)




