#!/bin/bash

cd YouTubeSpider
grep -hr "http://productforums.google.com/forum/#!category-topic/youtube/*" | tr "/" "\n" | grep -oe "[-a-zA-Z0-9]\{11\}" | sort | uniq > scraped_hashes_new
cp scraped_hashes_new ../scraped_hashes/
cd ../scraped_hashes
cat scraped_hashes scraped_hashes_new > scraped_h
mv scraped_h scraped_hashes
cat scraped_hashes orig_uniq_hashes | sort | uniq -u > hashes_left
cat hashes_left | sed -e "s/.*/'http:\/\/productforums.google.com\/forum\/#!category-topic\/youtube\/&',/" > urls.py
echo ']' >> urls.py
echo "urls = [" | cat - urls.py > /tmp/out && mv /tmp/out urls.py
