#!/usr/bin/env python3

base = "_z3"
inibase = "./.benchmark_z3.ini"


with open('./benches.conf', 'r') as f:
    for line in f.readlines():
        bname = line.split('=')[0].rstrip().lower()
        fname = ".smtbench{}_{}.ini".format(base,bname)
        with open(fname, 'w') as bfile:
            with open(inibase, 'r') as bmark_common:
                for bline in bmark_common.readlines():
                    bfile.write(bline)
                bfile.write(line)
