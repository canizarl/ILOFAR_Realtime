#!/bin/bash


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



        echo " "
        echo $(date)



        if rsync -ahP $og_data_source $monitor_temp_data | grep -q '.dat'; then
                echo "Upload succeeded" 
                python /home/ilofar/Scripts/Python/MonitorRealtime/lofar_monitor.py ${monitor_temp_data}/*X*
                sensors > status_lgc.txt
                ssh lcu 'rspctl --status' > status_lcu.txt
                echo "lofar monitor generated a preview."
                echo ""
        elif rsync -ahP $realta_data_source $monitor_temp_data/datastream | grep -q '.dat'; then
                echo "Upload succeeded. Realta is working." 
                python /home/ilofar/Scripts/Python/MonitorRealtime/lofar_monitor.py ${monitor_temp_data}/datastream/*X*
                sensors > status_lgc.txt
                ssh lcu 'rspctl --status' > status_lcu.txt
                echo "lofar monitor generated a preview."
                echo ""
        else
                sensors > status_lgc.txt
                echo "LCU IN INTERNATIONAL MODE" > status_lcu.txt
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
