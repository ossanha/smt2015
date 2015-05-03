#!/bin/sh

dirs=`ls ~/SMTLIB | tr [A-Z] [a-z]`
out="all_standings.md"
pat="# Final standings"
echo "# All standings" > $out
for d in $dirs; do
    echo "$d"
    echo "# ${d}" >> $out
    ./benchmark.py -ld -pd ${d} | grep -A 7 "${pat}" | sed -e 's/${pat}//g' >> ${out}
done
