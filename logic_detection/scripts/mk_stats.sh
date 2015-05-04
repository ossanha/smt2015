#!/bin/sh

SMTLIB="/home/richard/SMTLIB"
report="../report.md"
total=0
under=0
over=0
for dir in `ls ${SMTLIB}`
do
    t=`grep -A 6 "### ${dir} : summary" ${report} | grep Alerts | cut -d '/' -f 2 | awk '{s+=$1} END {print s}'`
    u=`grep -A 6 "### ${dir} : summary" ${report} | grep "* Under :" | cut -d ':' -f 2 | awk '{s+=$1} END {print s}'` 
    o=`grep -A 6 "### ${dir} : summary" ${report} | grep "* Over :" | cut -d ':' -f 2 | awk '{s+=$1} END {print s}'`
    echo "$dir $u $o $t"
    total=`echo "${total}  + ${t}" | bc`
    over=`echo "${over}  + ${o}" | bc`
    under=`echo "${under}  + ${u}" | bc`
done

echo "SMTLIB logic detection stats"
mk_info () {
    echo "$1 $2 $3"
    info="${1} / ${2}"
    echo -n "${3} : ${info}"
    pct=`echo "100.0 * ${info}" | bc -l `
    echo " (${pct} %)"

}

mk_info "${over}" "${total}" "Over"
mk_info ${under} ${total} "Under"
