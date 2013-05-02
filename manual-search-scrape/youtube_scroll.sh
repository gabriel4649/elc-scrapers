#!/bin/bash


WID=`xdotool search "Mozilla Firefox" | head -1`

for (( i=1; i<=100; i++ ))
do
    xdotool key  --clearmodifiers "ctrl+b"
    NUMBER=$[ ( $RANDOM % 10 )  + 5 ]
    sleep $NUMBER; xdotool key space $WID
    echo "Scrolling"
done
