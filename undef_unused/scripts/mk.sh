#!/bin/sh

out="data.csv"

echo "category,#scripts,#unused" > $out
for dir in `find -type d `; do
    if test "$dir" != "."; then
        echo "Getting data for $dir"
        files=`grep Alerts ${dir}/prelude.md | cut -d ':' -f 2 | cut -d '/' -f 2 | awk '{s+=$1} END {print s}'`
        unused=`grep unused ${dir}/prelude.md | cut -d ':' -f 2 | awk '{s+=$1} END {print s}'`
        d=`echo ${dir} | sed -e 's@\./@@g'`
        echo "$d,$files,$unused" >> $out
    fi
done
