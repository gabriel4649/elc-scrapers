#!/bin/bash

wid="$1"

for (( i=1; i<=100; i++ ))
do
    NUMBER=$[ ( $RANDOM % 10 )  + 5 ]
    sleep $NUMBER; xdotool key space $wid
done
