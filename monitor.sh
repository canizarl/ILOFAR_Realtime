#!/bin/bash

"
 ILOFAR MONITOR

  SUPPORTS
  357 Solar Observations
  357 w/ REALTA Solar Observations

  Uses a data buffer folder to get the data from the LCU. Every 10 mins it syncs using rsync.
  If it cant sync means observation isnt on or station is in international mode and will wait 30 mins.

  USES lofar_monitor.py to generate Dynamic spectra which is then sent to a webserver(done inside python)
  Generates logs from CPU status and station status and sends them  to webserver.

  RUN this using tmux.
  to run tmux:

  # NEW Tmux session
    tmux new -s monitor
  # in tmux ... run script
    ./monitor.sh
  # use ctrl+b d  to dettach
  # to reattach to the session
    tmux attach -t monitor


  NEEDS:
  lofar_monitor.py
  lofar_bst.py
  authors: Alberto Canizares  - canizares (at) cp.dias.ie
           Jeremy Rigney - jeremy.rigney (at) dias.ie

  changes:
  2020-12-14 :  Jeremy: added line to run update_antenna_status.py.   
  2020-12-14 :  Alberto: 30 mins delay when international mode removed. Now it always updates every 10 mins.  
  2020-12-15 :  Alberto: Clear data_buffer at night.  
  2020-12-15 :  Jeremy: Send HBA+LBA status log files to webserver
  2022-03-09 :  DMcK: Disable venv after LGC upgrade, patch daynow=$(date +%d) -> daynow=$(date +%e | sed 's/ //g')
"
day="0"

while true
do
	#source activate monitor_env

	daynow=$(date +%e | sed 's/ //g')
	if (($day != $daynow))
	then
		echo "new day"

		# clear all figures
		for i in {1..10}
		do
			curl -F file=@/home/ilofar/Monitor/NoData/LC_NO_DATA.png https://lofar.ie/operations-monitor/post_image.php?img=lc${i}X.png
			curl -F file=@/home/ilofar/Monitor/NoData/LC_NO_DATA.png https://lofar.ie/operations-monitor/post_image.php?img=lc${i}Y.png

			curl -F file=@/home/ilofar/Monitor/NoData/SPEC_NO_DATA.png https://lofar.ie/operations-monitor/post_image.php?img=spectro${i}X.png
			curl -F file=@/home/ilofar/Monitor/NoData/SPEC_NO_DATA.png https://lofar.ie/operations-monitor/post_image.php?img=spectro${i}Y.png
			rm -rf ~/Monitor/data_buff/
		done
	fi

	today=$(date +'%Y.%m.%d')
	day=$(date +%d)
	
	mkdir -p  ~/Monitor/data_buff/$today

	# # # # # # # # # #
	# Directories     #
	# # # # # # # # # #
	og_data_source="lcu:/data/home/user1/data/kbt/rcu357_1beam/${today}/*00?.dat"
	realta_data_source="lcu:/data/home/user1/data/kbt/rcu357_1beam_datastream*/${today}/*00?.dat"
	monitor_temp_data=~/"Monitor/data_buff/${today}"
	python_dir=~/"Scripts/Python/MonitorRealtime/"
	YYYY=$(date +'%Y')
	MM=$(date +'%m')
	DD=$(date +'%d')


	echo " "
	echo $(date)

	# populates folders in Data folder with javascript files for the calendar to know the names of the figures that will be used. 	
	python3 addtoscript.py
	curl -F file=@/home/ilofar/Data/IE613/monitor/dates_calendar.js https://lofar.ie/operations-monitor/post_log.php?js=dates_calendar

        python3 update_antenna_status.py #/home/ilofar/Monitor/
        curl -F file=@HBA_numbers.txt https://lofar.ie/operations-monitor/post_log.php?txt=HBA_numbers
        curl -F file=@LBA_numbers.txt https://lofar.ie/operations-monitor/post_log.php?txt=LBA_numbers	
        
        if rsync -ahP $og_data_source $monitor_temp_data | grep -q '.dat'; then
		echo "Upload succeeded"
      		newestfile=$(ls -Art ${monitor_temp_data}/ | tail -n 1)
		python3 /home/ilofar/Scripts/Python/MonitorRealtime/lofar_monitor.py ${monitor_temp_data}/${newestfile} /home/ilofar/Data/IE613/monitor/$today
		
		
		# # # # # # # # # #
		# STATUS REPORT   #
		# # # # # # # # # #		   
		# LGC   
		echo 'LGC STATUS' > status_lgc.txt
		date >> status_lgc.txt
		sensors >> status_lgc.txt
		#LCU
		echo 'LCU STATUS' > status_lcu.txt
		date >> status_lcu.txt
		ssh lcu 'rspctl --status' >> status_lcu.txt
	
        echo "lofar monitor generated a preview."
        echo ""
		./sendtomonitor.sh

	elif rsync -ahP $realta_data_source $monitor_temp_data/datastream | grep -q '.dat'; then
		echo "Upload succeeded. Realta is working."
		newestfile=$(ls -Art ${monitor_temp_data}/datastream/ | tail -n 1)
       		python3 /home/ilofar/Scripts/Python/MonitorRealtime/lofar_monitor.py ${monitor_temp_data}/datastream/${newestfile} /home/ilofar/Data/IE613/monitor/$today
		
		# # # # # # # # # #
		# STATUS REPORT   #
		# # # # # # # # # #		   
		# LGC   
		echo 'LGC STATUS' > status_lgc.txt
		date >> status_lgc.txt
		sensors >> status_lgc.txt
		#LCU
		echo 'LCU STATUS' > status_lcu.txt
		date >> status_lcu.txt
		ssh lcu 'rspctl --status' >> status_lcu.txt

		echo "lofar monitor generated a preview."
		./sendtomonitor.sh
        echo ""
	else
		# # # # # # # # # #
		# STATUS REPORT   #
		# # # # # # # # # #		   
		# LGC   
		echo 'LGC STATUS' > status_lgc.txt
		date >> status_lgc.txt
		sensors >> status_lgc.txt
		#LCU
		echo 'LCU STATUS' > status_lcu.txt
		date >> status_lcu.txt
		echo "LCU IN INTERNATIONAL MODE" >> status_lcu.txt

    		#echo "Upload failed. Try in half an hour"
		#sleep 1200
	fi


	# send logs
	echo "sending logs to webserver"
	curl -F file=@status_lcu.txt https://lofar.ie/operations-monitor/post_log.php?txt=status_lcu
	curl -F file=@status_lgc.txt https://lofar.ie/operations-monitor/post_log.php?txt=status_lgc
	echo "logs sent correctly"
        
        echo " sleep 10 mins"
	#wait 10 mins
	sleep 600
	
done











