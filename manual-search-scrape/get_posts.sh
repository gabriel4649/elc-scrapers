#!/bin/bash

# grep -rl "copyright" data/HPFanFicSpider/* | xargs -d '\n' cp -t ~/Desktop/

# Execute getopt
ARGS=`getopt --long -o "s:" "$@"`
# A little magic
eval set -- "$ARGS"

while true ; do
    case "$1" in
        -s )
            scraper=$2
            shift 2
        ;;
        *)
            break
        ;;
    esac 
done;

while read line; do
    scrapy parse --spider=$spider -c parse_thread -d 100 --nolog $line;
done
