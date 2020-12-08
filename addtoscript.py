# -*- coding: utf-8 -*-
import glob
import os
og_dir = os.getcwd()
# Directories in LGC to be checked:
directory_to_check = "/home/ilofar/Data/IE613/monitor"
#directory_to_check = "/Users/albertocanizares/OneDrive/Work/0_PhD/Projects/ILOFAR_REALTIME/test/monitor/"
# Which directory do you want the single output dates javascript to be saved in?
directory_save_dates = "/home/ilofar/Data/IE613/monitor"
#directory_save_dates = "/Users/albertocanizares/OneDrive/Work/0_PhD/Projects/ILOFAR_REALTIME/test/monitor/"
directories = [os.path.abspath(x[0]) for x in os.walk(directory_to_check)]

for each in directories:
    print(each)



substring = "monitor/2"  #this is used to make function create_list only run in subfolders with the required png
substring2 = "00X"
substring3 =  "00Y"
substring4 = "lightcurve"

def cut(str):
  if len(str) < 2:
    return ''
  return str[23:]

def cut_year2(str):
  return str[-10:-6]
    
def cut_month2(str):
    month = int(str[-5:-3])
    month2 = month - 1            # in javascript january is 0.
    return month2

def cut_day2(str):
  return int(str[-2:])


# #below function creates a list of dates to be blacklisted from the calendar in the website ------------------
# def Create_date_list():
#     for x in range(2017, 2030):
#         for y in range(1,13):
#             for z in range(1,32):
#                 nam = "new Date("  + str(x) + "," + str(y) + "," + str(z)  + ")"
#                 dates.append(nam)
#     s = 0
#     for i in directories: 
#         if directories[s].find(substring) != -1:  
#             os.chdir(i)         # Change working Directory
#             part = "new Date("  + cut_year2(directories[s]) + "," + str(cut_month2(directories[s])) + "," + str(cut_day2(directories[s]))  + ")"
#             print(part)
#             dates.remove(part)
#         s += 1
#     os.chdir(directory_save_dates)         # Change working Directory back to beginning directory to save file with all the dates
#     with open('dates_calendar.js', 'w') as f:  #writing a javascript file that makes a list of all dates with data for calendar function
#         print('var date_list = ' + str(dates).replace("'", "") , file = f)



#below function creates a list of pngs in each subfolder by date of creation, in a javascript file that can be fetched by website to display all pngs ------------------
def Create_list():
    s = 0
    for i in directories:
        if directories[s].find(substring) != -1:  
            os.chdir(i)         # Change working Directory
            files = glob.glob("*.png")  #finding all files in subdirectory with .png filenames
            files.sort(key=os.path.getmtime, reverse = True)  #sorting png list by modified date
            x_axis = 1
            x_light = 1
            y_axis = 1
            y_light = 1
            with open('figures.js', 'w') as f:  #writing a javascript file for website to show plots
                for t in range(len(files)):
                    if files[t].find(substring2) != -1: #if png is X axis it will show in row above Y axis
                        if files[t].find(substring4) != -1: #if lightcurve put on right of screen
                            print('document.getElementById("spectra_right_X' + str(x_light) + '").innerHTML += "<img src=\\"' + 'https://data.lofar.ie' + cut(directories[s].replace('\\', '/')) + '/' + files[t].replace('\\', '/')  + '\\" style = \\"width:100%\\">" ', file = f)
                            print('', file = f) 
                            x_light += 1 
                        else: 
                            print('document.getElementById("spectra_left_X' + str(x_axis) + '").innerHTML += "<img src=\\"' + 'https://data.lofar.ie' + cut(directories[s].replace('\\', '/')) + '/' + files[t].replace('\\', '/')  + '\\" style = \\"width:100%\\">" ', file = f)
                            print('', file = f)   
                            x_axis += 1
                            
                    if files[t].find(substring3) != -1: #if png is Y axis it will below X-Axis
                        if files[t].find(substring4) != -1: #if lightcurve put on right of screen
                            print('document.getElementById("spectra_right_Y' + str(y_light) + '").innerHTML += "<img src=\\"' + 'https://data.lofar.ie' + cut(directories[s].replace('\\', '/')) + '/' + files[t].replace('\\', '/')  + '\\" style = \\"width:100%\\">" ', file = f)
                            print('', file = f)     
                            y_light += 1
                        else: 
                            print('document.getElementById("spectra_left_Y' + str(y_axis) + '").innerHTML += "<img src=\\"' + 'https://data.lofar.ie' + cut(directories[s].replace('\\', '/')) + '/' + files[t].replace('\\', '/')  + '\\" style = \\"width:100%\\">" ', file = f)
                            print('', file = f)
                            y_axis += 1
        s += 1





#Create_date_list()



# This is a list of days that have to be blocked in the calendar
# because there was no observation. 
# So first generate a list of all the dates between 2017 and 2100
# then find out what days had observations and remove these dates 
# from the list. 
# The resulting is a blacklist containing dates with no observations.

dates = []         # initialise the dates list 



""" 
    yyyy is year
    mm is month 
    dd is day

"""
for yyyy in range(2017, 2100):
    for mm in range(1,13):
        if (mm == 4)|(mm==6)|(mm==9)|(mm==11):  # april, june, sept, nov 30 days
            for dd in range(1,31):
                new_date = "new Date("  + str(yyyy) + "," + str(mm-1) + "," + str(dd)  + ")"
                dates.append(new_date)     
        elif(mm==2):
            if (yyyy%4==0):
                if (yyyy%100 !=0 ):
                    for dd in range(1,30):
                        new_date = "new Date("  + str(yyyy) + "," + str(mm-1) + "," + str(dd)  + ")"
                        dates.append(new_date)    
                elif (yyyy%100==0) & (yyyy%400==0):
                    for dd in range(1,30):
                        new_date = "new Date("  + str(yyyy) + "," + str(mm-1) + "," + str(dd)  + ")"
                        dates.append(new_date)   
                else:
                    for dd in range(1,29):
                        new_date = "new Date("  + str(yyyy) + "," + str(mm-1) + "," + str(dd)  + ")"
                        dates.append(new_date)     
            else:
                for dd in range(1,29):
                    new_date = "new Date("  + str(yyyy) + "," + str(mm-1) + "," + str(dd)  + ")"
                    dates.append(new_date)     
        else:
            for dd in range(1,32):
                new_date = "new Date("  + str(yyyy) + "," + str(mm-1) + "," + str(dd)  + ")"
                dates.append(new_date)
s = 0



"""
    Now remove the observation dates from the dates list
    Go through each directory. 
    Directories have the dates in their address so go into 
    each directory and grab the year, month or day accordingly
    bare in mind that directories are in a full path and need to 
    be cut to the part of the string that refers to year month or day

"""
for i in directories: 
    if directories[s].find(substring) != -1:  
        os.chdir(i)         # Change working Directory
        
        #  local_date refers to the dates that the observation took place in local mode.
        local_date = "new Date("  + cut_year2(directories[s]) + "," + str(cut_month2(directories[s])) + "," + str(cut_day2(directories[s]))  + ")"
        #print(local_date)
        dates.remove(local_date)
    s += 1
os.chdir(directory_save_dates)         # Change working Directory back to beginning directory to save file with all the dates

with open('dates_calendar.js', 'w') as f:  #writing a javascript file that makes a list of all dates with data for calendar function
    print('var date_list = ' + str(dates).replace("'", "") , file = f)

print("dates_calendar.js updated! ")




Create_list()



os.chdir(og_dir)

