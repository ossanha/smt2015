#!/bin/sh

dirs=`ls ~/SMTLIB | tr [A-Z] [a-z]`
tools=`cat alia/extract.md | grep : | cut -d ':' -f 1`
res="res.csv"

echo -n "Tool" > $res
for d in $dirs
do
    echo -n ",$d" >> $res
done
echo "" >> $res

for t in $tools
do
    echo "Handling $t"
    echo -n "$t" >> $res
    for d in $dirs
    do
        echo "$d"
        extract="${d}/extract.md"
        pos=`grep "${t}" "${extract}" | cut -d ':' -f 2`
        if [ "$pos" != "" ]; then
            echo -n ",${pos}" >> $res
        else
            echo -n ",0" >> $res
        fi
    done
    echo "" >> $res
done
