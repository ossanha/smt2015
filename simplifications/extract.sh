#!/bin/sh

name="foo"
extract_name () {
    echo "Extract $1"
    name=`echo $1 | sed -e 's/perf_//g' | sed -e 's/_g/ g/g' | cut -d ' ' -f 1`
}

for f in $@; do
    extract_name $f
    fname="${name}.csv"
    echo "Writing ${fname}"
    echo ${name} > ${fname}
    grep "smt2" $f | grep -v interrupted | grep -v exceeded | awk  '{print $1,",", $2}' >> ${fname}
    fname="${name}_lassoranker.csv"
    echo "Writing  ${fname}"
    echo ${name} > ${fname}
    grep "smt2" $f | grep LassoRanker | grep -v interrupted | grep -v exceeded | awk  '{print $1,",", $2}' >> ${fname}
done
