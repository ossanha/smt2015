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

files = [ ("CVC4 (QF_LRA)", "smtpp_prepro_time_CVC4_QF_LRA.txt"),
          ("CVC4 (LassoRanker)", "smtpp_prepro_time_CVC4_QF_LRA_lassoranker.txt"),
          ("Z3 (QF_LRA)", "smtpp_prepro_time_Z3_QF_LRA.txt"),
          ("Z3 (LassoRanker)", "smtpp_prepro_time_Z3_QF_LRA_lassoranker.txt"),
]
plt.style.use('ggplot')
fig, axes = plt.subplots(2, 2)

def to_float(str):
    s = str.lstrip().rstrip()
    if s == '' or s == 'CPU':
        return args.default
    elif s == "Excluded":
        return 0
    else:
        return float(str)

def extract_data(fname):
    with open(fname) as csvfile:
        reader = csv.reader(csvfile)
        data = [ r for r in reader ]
        summary = dict()
        timeout = 0
        for i, row in enumerate(data[1:]):
            logging.debug("Line {} : {} ".format(i, row))
            no_simp = to_float(row[2])
            if no_simp == args.default:
                timeout += 1
            # Row 1 is pp time, 2 is prover no simp time, 3 prover with simp time
            summary[row[0]] = to_float(row[2]), to_float(row[3]), to_float(row[1])
        return timeout, summary

colors=['0.4', '0']
lw=2
for (i, (title, fname)) in enumerate(files):
    print("Computing for {}".format(fname))
    ax = axes[i / 2][i % 2]
    ax.set_title(title)
    tout, data = extract_data(fname)
    data_sorted = sorted(data.items(), key=operator.itemgetter(1))
    #print(data_sorted[:20])
    prover_no_simp = [ d[0] for (_, d) in data_sorted ]
    prover_simp = [ d[1] for (_, d) in data_sorted ]
    cumulated = [ d[1] + d[2] for (_, d) in data_sorted ]
    resolved_no_simp = 0
    resolved_cumulated = 0
    resolved_simp = 0
    for (_, d) in data_sorted:
        if d[0] < args.default: resolved_no_simp += 1
        if d[1] < args.default: resolved_simp += 1
        if d[1] + d[2] < args.default: resolved_cumulated += 1
    print(resolved_no_simp, resolved_simp, resolved_cumulated)
    # pure proof times
    ax.plot(prover_no_simp, prover_no_simp)
    ax.scatter(prover_no_simp, prover_simp, c='blue')
    #ax.scatter(prover_no_simp, cumulated, c='green')
    # cumulated

    
    
plt.tight_layout()
plt.subplots_adjust(left=0.04, right=0.98, top=0.96, bottom=0.06)

#plt.savefig(save, dpi=50)
plt.show()
