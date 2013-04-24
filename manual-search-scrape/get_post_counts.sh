#!/bin/bash
terms=( "copyright" "legal" "illegal" "permission" "trademark" "stealing" \
"steal" "stole" "license" "rights" "attorney" "infringement" "copy" "copying" \
"plagiarism" );

dir="$1"

if [ -f "$dir/counts" ];
then
    rm "$dir/counts"
fi

touch "$dir/counts"
for i in "${terms[@]}"
do
    grep -rl "$i" $dir | wc -l > temp
    echo "$i" | cat - temp >> "$dir/counts"
    rm temp
done

ls "$dir" | wc -l > temp
echo "total" | cat - temp >> "$dir/counts"
rm temp
