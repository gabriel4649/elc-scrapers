# Overclocked
egrep -oh "http://ocremix.org/forums/showthread\.php\?[tp]=[0-9]*" * | sort | uniq | sed -e 's/.*/\"&\",/' > results; echo "]" >> results; sed -i '1iurls= [' results

# Fanart
egrep -oh "http://forums.fanart-central.net/viewtopic\.php\?[pt]=[0-9]*" * | sort | uniq | sed -e 's/.*/\"&\",/' > results; echo "]" >> results; sed -i '1iurls= [' results

# Deviantart
egrep -oh "http://forum.deviantart.com/[A-Za-z]*/[A-Za-z]*/[0-9]*" * | sort | uniq | sed -e 's/.*/\"&\",/' > results; echo "]" >> results; sed -i '1iurls= [' results
