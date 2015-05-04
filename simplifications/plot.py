#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import csv
import sys
import logging
import operator

sv = "foo"
provers=["Z3", "CVC4"]
cases=[("", "QF_LRA_default"), ("_lassoranker", "LassoRanker")]
plt.style.use('ggplot')
fig, axes = plt.subplots(2, 2)

def extract_data(fname):
    with open(fname) as csvfile:
        reader = csv.reader(csvfile)
        data = [ r for r in reader ]
        summary = dict()
        for row in data[1:]:
            summary[row[0]] = float(row[1])
        return summary

colors=['0.4', '0']
lw=2
for i, p in enumerate(provers):
    for j, c in enumerate(cases):
        print(p, c)
        ax = axes[i][j]
        legends = [p, p + " simp"]
        fname1 = "{}_QF_LRA_default{}.csv".format(p, c[0])
        fname2 = "{}_QF_LRA_simp{}.csv".format(p, c[0])
        ax.set_title("{} ({})".format(p, c[1]))
        c1 = extract_data(fname1)
        c2 = extract_data(fname2)
        #print(c1)
        #print(c2)
        c1_sorted = sorted(c1.items(), key=operator.itemgetter(1))
        #print(c1_sorted)
        def get_val(key):
            try:
                return c2[key]
            except KeyError:
                return 0.0
        c2_sorted = [ (x[0], get_val(x[0])) for x in c1_sorted ]
        both = zip(c1_sorted, c2_sorted)
        for b in both:
            print(b[0])
            print(b[1])
        
        times1 = [ x[1] for x in c1_sorted ]
        times2 = [ get_val(x[0]) for x in c1_sorted ]
        ax.set_xlabel("Solved instances")
        ax.set_ylabel("Time")
        ax.plot(times1, color=colors[0],linewidth=lw)
        ax.plot(times2, color=colors[1],linewidth=lw)
        ax.legend(legends, loc=0)

plt.tight_layout()
plt.subplots_adjust(left=0.04, right=0.98, top=0.96, bottom=0.06)
save=sv + ".pdf"
#print("Saving as " + save)

#plt.savefig(save, dpi=50)
#plt.show()
