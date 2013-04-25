#!/bin/bash

terms=( "copyright" "legal" "illegal" "permission" "trademark" "stealing" \
"steal" "stole" "license" "rights" "attorney" "infringement" "copy" "copying" \
"plagiarism" );

dir="$1"
dest="$2"

for i in "${terms[@]}"
do
    if [ ! -d "$dest$i" ]; then
        mkdir "$dest$i"
    fi

    grep -url $i $dir | sort | uniq | xargs -d '\n' cp -t "$dest$i"
done

if [ ! -d "$dest/all" ]; then
    mkdir "$dest/all"
fi

cp -r $dir "$dest/all"
