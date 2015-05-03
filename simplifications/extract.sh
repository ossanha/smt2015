#!/bin/sh

name="foo"
extract_name () {
    echo "Extract $1"
    name=`echo $1 | sed -e 's/perf_//g' | sed -e 's/_g/ g/g' | cut -d ' ' -f 1`
}

cvc4_data="perf_CVC4_QF_LRA_griffon_default.txt"
z3_data="perf_Z3_QF_LRA_griffon_default.txt"
cvc4_pp_data="perf_CVC4_QF_LRA_simp_griffon.txt"
z3_pp_data="perf_Z3_QF_LRA_griffon_default.txt"

for f in `ls *.txt`; do
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
