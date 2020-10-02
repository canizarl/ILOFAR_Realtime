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
"


while true
do
	source activate monitor_env

	today=$(date +'%Y.%m.%d')

	mkdir -p  ~/Monitor/data_buff/$today

	# # # # # # # # # #
	# Directories     #
	# # # # # # # # # #
	og_data_source="lcu:/data/home/user1/data/kbt/rcu357_1beam/${today}/*00?.dat"
	realta_data_source="lcu:/data/home/user1/data/kbt/rcu357_1beam_datastream/${today}/*00?.dat"
	monitor_temp_data=~/"Monitor/data_buff/${today}"
	python_dir=~/"Scripts/Python/MonitorRealtime/"
	YYYY=$(date +'%Y')
	MM=$(date +'%m')
	DD=$(date +'%d')


	echo " "
	echo $(date)



	if rsync -ahP $og_data_source $monitor_temp_data | grep -q '.dat'; then
		echo "Upload succeeded"
        python /home/ilofar/Scripts/Python/MonitorRealtime/lofar_monitor.py ${monitor_temp_data}/*X* /home/ilofar/Data/IE613/monitor/$today
		
		
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
	elif rsync -ahP $realta_data_source $monitor_temp_data/datastream | grep -q '.dat'; then
		echo "Upload succeeded. Realta is working."
        python /home/ilofar/Scripts/Python/MonitorRealtime/lofar_monitor.py ${monitor_temp_data}/datastream/*X* /home/ilofar/Data/IE613/monitor/$today
		
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

		
    	echo "Upload failed. Try in half an hour"
		sleep 1200
	fi







	# send logs
	echo "sending logs to webserver"
	curl -F file=@status_lcu.txt https://lofar.ie/monitor/post_log.php?txt=status_lcu
    curl -F file=@status_lgc.txt https://lofar.ie/monitor/post_log.php?txt=status_lgc
	echo "logs sent correctly"

	echo " sleep 10 mins"
	#wait 10 mins
	sleep 600
done













