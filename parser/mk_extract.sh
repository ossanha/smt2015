#!/bin/sh

dirs=`ls ~/SMTLIB | tr [A-Z] [a-z]`
pat="#EXTRACT"
for d in $dirs; do
    echo "$d"
    out="${d}/${d}.md"
    extract="${d}/extract.md"
    ./benchmark.py -ld -pd ${d} > ${out}
    cat ${out} | grep -A 7 "#EXTRACT" > ${extract}
    n=`wc -l ${extract} | cut -d ' ' -f 1`
    if [ $n -ne 8 ]
    then
        echo "${d} has only ${n} tests"
    fi
done
