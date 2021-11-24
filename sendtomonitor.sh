#!/bin/bash
today=$(date +'%Y.%m.%d')
pathtodata="/home/ilofar/Data/IE613/monitor/${today}"


# First count how many files there are
n=$(ls $pathtodata/*X*| wc -l)

# limited to 10 pairs per polarization
if (($n > 10));
then
    n=10
fi;

# Dynamic spectra.... X and Y
echo "Sending Dynamic Spectra X polarization"
i=1
for f in $(ls -r $pathtodata/*X* | grep -v "lightcurve" | head -$n); do
    echo "File $i-> $f"
    curl -F file=@$f https://lofar.ie/operations-monitor/post_image.php?img=spectro${i}X.png
    i=$((i+1))
done

echo "Sending Dynamic Spectra Y polarization"
i=1
for f in $(ls -r $pathtodata/*Y* | grep -v "lightcurve" | head -$n); do
    echo "File $i-> $f"
    curl -F file=@$f https://lofar.ie/operations-monitor/post_image.php?img=spectro${i}Y.png
    i=$((i+1))
done


# Lightcurves ........X and Y
echo "Sending Lightcurves X polarization"
i=1
for f in $(ls -r $pathtodata/*X*lightcurve* | head -$n); do
    echo "File $i-> $f"
    curl -F file=@$f https://lofar.ie/operations-monitor/post_image.php?img=lc${i}X.png
    i=$((i+1))
done

echo "Sending Lightcurves Y polarization"
i=1
for f in $(ls -r $pathtodata/*Y*lightcurve* | head -$n); do
    echo "File $i-> $f"
    curl -F file=@$f https://lofar.ie/operations-monitor/post_image.php?img=lc${i}Y.png
    i=$((i+1))
done

