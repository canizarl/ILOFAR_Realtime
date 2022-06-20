#!/bin/bash
source activate monitor_env


#
#year="2019"
#month="01"
#day="22"
#data_source="/home/ilofar/Data/IE613/2019"
#png_dir="/home/ilofar/Data/IE613/monitor"
#mkdir ${png_dir}/${year}.${month}.${day}
#
#echo ${png_dir}/${year}.${month}.${day}
#python old_data.py ${data_source}/${month}/${day}/bst/kbt/rcu357_1beam/*X.dat ${png_dir}/${year}.${month}.${day}
#



year="2019"
month="01"
day="22"
data_source="/home/ilofar/Data/IE613/2019"
png_dir="/home/ilofar/Data/IE613/monitor"
mkdir ${png_dir}/${year}.${month}.${day}

echo ${png_dir}/${year}.${month}.${day}
python old_data.py ${data_source}/${month}/${day}/bst/kbt/rcu357_1beam/20190122_102816_bst_00X.dat ${png_dir}/${year}.${month}.${day}
python old_data.py ${data_source}/${month}/${day}/bst/kbt/rcu357_1beam/20190122_103247_bst_00X.dat ${png_dir}/${year}.${month}.${day}
python old_data.py ${data_source}/${month}/${day}/bst/kbt/rcu357_1beam/20190122_105556_bst_00X.dat ${png_dir}/${year}.${month}.${day}

year="2019"
month="01"
day="23"
data_source="/home/ilofar/Data/IE613/2019"
png_dir="/home/ilofar/Data/IE613/monitor"
mkdir ${png_dir}/${year}.${month}.${day}

echo ${png_dir}/${year}.${month}.${day}
python old_data.py ${data_source}/${month}/${day}/bst/kbt/rcu357_1beam/20190123_101517_bst_00X.dat ${png_dir}/${year}.${month}.${day}



year="2019"
month="01"
day="25"
data_source="/home/ilofar/Data/IE613/2019"
png_dir="/home/ilofar/Data/IE613/monitor"
mkdir ${png_dir}/${year}.${month}.${day}

echo ${png_dir}/${year}.${month}.${day}
python old_data.py ${data_source}/${month}/${day}/bst/20190125_112942_bst_00X.dat ${png_dir}/${year}.${month}.${day}
python old_data.py ${data_source}/${month}/${day}/bst/20190125_113920_bst_00X.dat ${png_dir}/${year}.${month}.${day}


year="2019"
month="02"
day="26"
data_source="/home/ilofar/Data/IE613/2019"
png_dir="/home/ilofar/Data/IE613/monitor"
mkdir ${png_dir}/${year}.${month}.${day}

echo ${png_dir}/${year}.${month}.${day}
python old_data.py ${data_source}/${month}/${day}/bst/kbt/rcu357_1beam/20190206_115606_bst_00X.dat ${png_dir}/${year}.${month}.${day}

year="2019"
month="04"
day="24"
data_source="/home/ilofar/Data/IE613/2019"
png_dir="/home/ilofar/Data/IE613/monitor"
mkdir ${png_dir}/${year}.${month}.${day}

echo ${png_dir}/${year}.${month}.${day}
python old_data.py ${data_source}/${month}/${day}/bst/kbt/rcu357_1beam/20190424_063534_bst_00X.dat ${png_dir}/${year}.${month}.${day}


year="2019"
month="05"
day="28"
data_source="/home/ilofar/Data/IE613/2019"
png_dir="/home/ilofar/Data/IE613/monitor"
mkdir ${png_dir}/${year}.${month}.${day}

echo ${png_dir}/${year}.${month}.${day}
python old_data.py ${data_source}/${month}/${day}/bst/kbt/rcu357_1beam/20190508_081554_bst_00X.dat ${png_dir}/${year}.${month}.${day}


year="2019"
month="06"
day="06"
data_source="/home/ilofar/Data/IE613/2019"
png_dir="/home/ilofar/Data/IE613/monitor"
mkdir ${png_dir}/${year}.${month}.${day}

echo ${png_dir}/${year}.${month}.${day}
python old_data.py ${data_source}/${month}/${day}/bst/kbt/rcu357_1beam/20190606_114414_bst_00X.dat ${png_dir}/${year}.${month}.${day}
python old_data.py ${data_source}/${month}/${day}/bst/kbt/rcu357_1beam/20190606_151712_bst_00X.dat ${png_dir}/${year}.${month}.${day}


year="2019"
month="10"
day="23"
data_source="/home/ilofar/Data/IE613/2019"
png_dir="/home/ilofar/Data/IE613/monitor"
mkdir ${png_dir}/${year}.${month}.${day}

echo ${png_dir}/${year}.${month}.${day}
python old_data.py ${data_source}/${month}/${day}/20191023_104307_bst_00X.dat ${png_dir}/${year}.${month}.${day}
python old_data.py ${data_source}/${month}/${day}/20191023_122420_bst_00X.dat ${png_dir}/${year}.${month}.${day}


year="2019"
month="11"
day="07"
data_source="/home/ilofar/Data/IE613/2019"
png_dir="/home/ilofar/Data/IE613/monitor"
mkdir ${png_dir}/${year}.${month}.${day}

echo ${png_dir}/${year}.${month}.${day}
python old_data.py ${data_source}/${month}/${day}/bst/kbt/rcu357_1beam/20191107_094656_bst_00X.dat ${png_dir}/${year}.${month}.${day}






