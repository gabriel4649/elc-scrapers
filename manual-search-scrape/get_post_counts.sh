#!/bin/bash
terms=( "copyright" "legal" "illegal" "permission" "trademark" "stealing" \
"steal" "stole" "license" "rights" "attorney" "infringement" "copy" "copying" \
"plagiarism" );

dir="$1"
dest="$2"

if [ -f "$dest/counts.txt" ];
then
    rm "$dest/counts.txt"
fi

touch "$dest/counts.txt"
for i in "${terms[@]}"
do
    grep -rl "$i" "$dir" | wc -l > temp
    echo "$i" | cat - temp >> "$dest/counts.txt"
    rm temp
done

ls "$dir" | wc -l > temp
echo "total" | cat - temp >> "$dest/counts.txt"
rm temp
