#!/usr/bin/env python3
import argparse
import numpy as np
import matplotlib.pyplot as plt
import csv
import sys
import logging
import operator
import re

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
parser.add_argument("-default", "--default", dest = "default_time",
                    default=90,
                    type=float,
                    help = " default value for missing data points")

parser.add_argument("-tl", "--time-limit", dest = "time_limit",
                    default=1000,
                    type=float,
                    help = " default value for missing data points")

parser.add_argument("-cu", "--cumulative-time", dest = "cu_time",
                    action = "store_true",
                    help = " ")

# 90 is the max time allowed for these benchmarks

args = parser.parse_args()

if args.debug:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)


def get_smtpp_timings(fname):
    excl_pat = re.compile("Excluded.*")
    cpu_pat = re.compile("CPU.*")
    with open(fname, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter = '\t')
        data = dict()
        for r in reader:
            fname = r[0]
            result = r[1].rstrip().lstrip()
            if re.match(cpu_pat, result):
                data[fname] = None
            elif not re.match(excl_pat, result):
                data[fname] = float(result)
        return data

lassoranker_pat = re.compile(".*LassoRanker.*")
smtpp_times = get_smtpp_timings("smtpp_prepro_time.txt")

smtpp_times_lr = dict()
for k, v in smtpp_times.items():
    if re.match(lassoranker_pat, k):
        smtpp_times_lr[k] = v

print("SMTPP", len(smtpp_times), len(smtpp_times_lr))
provers = ["Z3", "CVC4"]
cases = ["default", "simp"]
benches = ['QF_LRA', 'LassoRanker']

def read_data(fname):
    smt2file = re.compile("\S+.smt2")
    data = dict()
    def extract_time(v, res):
        if res != '1' and res != '0':
            return args.default_time
        else:
            return float(v)

    def only_fields(l):
        return [ s for s in l if s != '' ]

    with open(fname, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter = ' ')
        for r in reader:
            if re.match(smt2file, r[0]):
                fields = only_fields(r)
                data[fields[0]] = extract_time(fields[1], fields[2])
        data_lassoranker = dict()
        for k, v in data.items():
            if re.match(lassoranker_pat, k):
                data_lassoranker[k] = v
        return data, data_lassoranker

def filename(prover, case):
    s = "perf_{}_QF_LRA_{}_graphene".format(prover, case)
    print(s)
    if case == "default":
        s += "_500s"
    return s + ".txt"

plt.style.use('ggplot')
fig, axes = plt.subplots(2, 2)
colors=['0.4', '0']
lw=2


p = provers[1]
default, default_lr = read_data(filename(p, cases[0]))
simp, simp_lr = read_data(filename(p, cases[1]))

sorteddef = sorted(default_lr.items(), key=operator.itemgetter(1))
sortedsimp = sorted(simp_lr.items(), key=operator.itemgetter(1))
def_sorted = [ v for k, v in sorteddef if v < args.time_limit ]
simp_sorted = [ v for k, v in sortedsimp if v < args.time_limit]
#def2_sorted = [ v for _, v in def_sorted ]

ax = axes[0][0]
ax.plot(def_sorted)
ax.plot(simp_sorted, color = 'g')
#ax.scatter(def2_sorted, simp_sorted)
               
# for i, p in enumerate(provers):

#     print ("Lasso ranker sizes ", len(default), len(simp),
#            len(default_lassoranker), len(simp_lassoranker))
#     def refill(d1, d2, d3):
#         smt2files = dict()
#         def process(d):
#             for k in d.keys():
#                 if args.cu_time:
#                     if k in d3 and d3[k] is not None:
#                         logging.debug(k + " is in")
#                         smt2files[k] = True
#                     else:
#                         logging.debug(k + " is NOT in")
#                 else:
#                     logging.debug(k + " is in TOO")
#                     smt2files[k] = True
#         process(d1)
#         process(d2)
#         for fname in smt2files.keys():
#             if not fname in d1:
#                 d1[fname] = args.default_time
#             if not fname in d2:
#                 d2[fname] = args.default_time
#         return smt2files

#     def mk_points(files, d1, d2, d3):
#         d1_sorted = sorted(d1.items(), key=operator.itemgetter(1))
#         d1_limited = [ (k , v) for k, v in d1_sorted if k in files ]
#         d2_done = [ d2[k] for k, _ in d1_limited ]
# #        print([ k for k in d3.keys() ])
#         if args.cu_time:
#             d3_done = [ d2[k] + d3[k] \
#                         if d2[k] != args.default_time and d3[k] is not None \
#                         else args.default_time for k, _ in d1_limited  ]
#         else:
#             d3_done = []
#         d1_done = [ v for _, v in d1_limited ]
#         return d1_done, d2_done, d3_done

#     g = [(default, simp, smtpp_times),
#          (default_lassoranker, simp_lassoranker, smtpp_times_lr)]
#     for j, (d1, d2, d3) in enumerate(g):
#         print(i, j)
#         print(len(d1), len(d2), len(d3))
#         files = refill(d1, d2, d3)
#         l1, l2, l3 = mk_points(files, d1, d2, d3)
#         #print(l1, l2, l3)
#         print("Lines", len(l1), len(l2), len(l3))
#         ax = axes[i][j]
#         ax.plot(l1, l1, color=colors[0])
#         ax.set_xlabel('{} (s)'.format(p))
#         ax.set_title(benches[j])
#         if args.cu_time:
#             l = l3
#             ylabel = 'SMTpp + {} simp (s)'.format(p)
#         else:
#             l = l2
#             ylabel = '{} simp (s)'.format(p)
#         ax.scatter(l1, l3, c='g')

plt.tight_layout()
#plt.subplots_adjust(left=0.04, right=0.98, top=0.96, bottom=0.06)
plt.show()
