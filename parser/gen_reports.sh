#!/bin/sh

DIRS="alia" 
# auflia auflira aufnira bv lia lra nia nra qf_abv qf_alia qf_aufbv qf_auflia qf_ax qf_idl qf_lra qf_nia qf_nra qf_rdl qf_uf qf_ufbv qf_ufidl qf_uflia qf_uflra qf_ufnra uf ufbv uflia"

if test $# -ge 1; then
    REPORT_DIR=$1
else
    REPORT_DIR=reports
fi

if [ ! -e $REPORT_DIR ]; then
    echo -n "Creating directory $REPORT_DIR ..."
    mkdir -p $REPORT_DIR
    echo "done"
fi

for d in $DIRS; do
    echo -n "Generating report for $d ..."
    ./benchmark.py -ld -pd $d > $REPORT_DIR/$d.md
    echo "done"
done
