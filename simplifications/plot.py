#!/usr/bin/env python3
import argparse
import numpy as np
import matplotlib.pyplot as plt
import csv
import sys
import logging
import operator

parser = argparse.ArgumentParser("Plot graphs for simplications")
parser.add_argument("-d", "--debug", dest = "debug",
                        action = "store_true",
                        help = 'activate debugging messages')
parser.add_argument("-type", "--type", dest = "type",
                    default="avg",
                    help = " generate plot according to type (avg, perpb)")
parser.add_argument("-view", "--view", dest = "view",
                    default=None,
                    help = " generate plot according to type (scatter)")
parser.add_argument("-default", "--default", dest = "default",
                    default=90,
                    type=float,
                    help = " default value for missing data points")
# 90 is the max time allowed for these benchmarks

args = parser.parse_args()

if args.debug:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

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

        inter_c1 = dict()
        inter_c2 = dict()
        for k, v in c1.items():
            inter_c1[k] = v
            if not k in c2:
                inter_c2[k] = args.default
        for k, v in c2.items():
            inter_c2[k] = v
            if not k in c1:
                inter_c1[k] = args.default
        print(len(inter_c1.items()), len(inter_c2.items()))

        def get_val(key):
            try:
                return c2[key]
            except KeyError:
                return 0.0
        c1_sorted = sorted(inter_c1.items(), key=operator.itemgetter(1))
        if args.type == "perpb":
            c2_sorted = [ (x[0], get_val(x[0])) for x in c1_sorted ]
        else:
            c2_sorted = sorted(inter_c2.items(), key=operator.itemgetter(1))
        times1 = [ x[1] for x in c1_sorted ]
        times2 = [ x[1] for x in c2_sorted ]
        if args.view  == "scatter":
            print(len(times1), len(times2))
            ax.scatter(times1, times2, c=colors[1])
            ax.plot(times1, times1, color=colors[0])
            ax.set_xlabel(legends[0] + "(s)")
            ax.set_ylabel(legends[1] + "(s)")
            #ax.legend(legends, loc=2)
        else:
            ax.plot(times1, color=colors[0],linewidth=lw)
            ax.plot(times2, color=colors[1],linewidth=lw)
            ax.set_xlabel("Solved instances")
            ax.set_ylabel("Time")
            ax.legend(legends, loc=0)

plt.tight_layout()
plt.subplots_adjust(left=0.04, right=0.98, top=0.96, bottom=0.06)
save=sv + ".pdf"
#print("Saving as " + save)

#plt.savefig(save, dpi=50)
plt.show()
