#!/bin/sh

SMTLIB="/home/richard/SMTLIB"
report="../report.md"
out="data.csv"

echo "category,#scripts,#over,#under" > $out
for dir in `ls ${SMTLIB}`; do
    if test "$dir" != "."; then
        echo "Getting data for $dir"
        files=`grep -A 6 "### ${dir} : summary" ${report} | grep Alerts | cut -d '/' -f 2 | awk '{s+=$1} END {print s}'`
        under=`grep -A 6 "### ${dir} : summary" ${report} | grep "* Under :" | cut -d ':' -f 2`
        over=`grep -A 6 "### ${dir} : summary" ${report} | grep "* Over :" | cut -d ':' -f 2`
        echo "$dir,$files,$over,$under" >> $out
    fi
done
