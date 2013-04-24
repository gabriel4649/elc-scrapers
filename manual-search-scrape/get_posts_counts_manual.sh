#!/bin/bash
touch counts
dir="$1"
for f in $dir*_raw
do
    grep -h "thread" $f | grep "page" -v | sort | uniq | wc -l > temp
    echo "$f" | cat - temp >> counts
    rm temp
done
