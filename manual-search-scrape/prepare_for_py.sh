grep -h "thread" * | grep "page" -v | sort | uniq | sed -e 's/.*/\"&\",/' > results; echo "]" >> results; sed -i '1iurls= [' results
