#!/usr/bin/env python

import re
import os
import logging
import argparse
import csv

parser = argparse.ArgumentParser("Data extraction")
parser.add_argument("-d", "--debug", dest = "debug",
                        action = "store_true",
                        help = 'activate debugging messages')

parser.add_argument("-default", "--default", dest = "default_time",
                    default=90,
                    type=float,
                    help = " default value for missing data points")

parser.add_argument("-cut", "--cut-limit", dest = "time_cut",
                    default=500,
                    type=float,
                    help = " remove points over that")
parser.add_argument("-smtppcut", "--smtpp-cut-limit", dest = "smtpp_time_cut",
                    default=500,
                    type=float,
                    help = " remove points over that")

args = parser.parse_args()

if args.debug:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

filepat = re.compile("perf_(.*)_QF_LRA_(.*)_graphene(.*).txt")
lassoranker_pat = re.compile(".*LassoRanker.*")

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

smtpp_times = get_smtpp_timings("smtpp_prepro_time.txt")

def subset_to_lasso(d):
    d1 = dict()
    for k, v in d.items():
        if re.match(lassoranker_pat, k):
            d1[k] = v
    return d1


def get_test_title(filename):
    m = re.match(filepat, filename)
    if m:
        return("{} {} {}".format(m.group(1), m.group(2), m.group(3)))

def read_data(fname):
    logging.debug("Reading {}".format(fname))
    smt2file = re.compile("\S+.smt2")
    data = dict()
    def extract_time(v, res):
        if res != '1' and res != '0':
            return None
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
        return data

files = []
for f in os.listdir('.'):
    if os.path.isfile(f) and re.match(filepat, f):
        logging.debug("Add {}".format(f))
        files.append(f)

files = sorted(files)
print("Files", files)

def count_solved(d):
    n = 0
    for k, v in d.items():
        if v is not None:
            n += 1
    return n

for f in files:
    t = get_test_title(f)
    print(t)
    data = read_data(f)
    lassoranker = subset_to_lasso(data)
    logging.debug("Data: {}, LR: {}".format(len(data), len(lassoranker)))
    solved_qf_lra = count_solved(data)
    solved_lr = count_solved(lassoranker)


    def count_under_time_cut(d, tc):
        n = 0
        for k, v in d.items():
            if v is not None and v < tc:
                n += 1
        return n

    under_tc_qf_lra =  count_under_time_cut(data, args.time_cut)
    under_tc_lr =  count_under_time_cut(lassoranker, args.time_cut)
    print("Solved (QF_LRA): {}".format(solved_qf_lra))
    print("Solved (QF_LRA) < {}: {}".format(args.time_cut, under_tc_qf_lra))
    print("Solved (LR): {}".format(solved_lr))
    print("Solved (LR) < {}: {}".format(args.time_cut, under_tc_lr))

    def count_pp_under_time_cut(d, tc):
        n = 0
        almost = 0
        not_pp = 0
        for k, v in d.items():
            if v is not None and v < tc:
                if not k in smtpp_times or smtpp_times[k] is None:
                    not_pp += 1
                else:
                    vtotal = v + smtpp_times[k]
                    if vtotal < tc:
                        n += 1
                    else: almost += 1
        return not_pp, n, almost

    def is_simp_file(f):
        pat = re.compile("\S+_simp_\S+.txt")
        return re.match(pat, f)

    if is_simp_file(f):
        not_pp, count, almost = count_pp_under_time_cut(data, args.time_cut)
        print("Solved (QF_LRA + PP) < {}: {} ({}/{})".format(args.time_cut,
                                                     count, not_pp, almost))
        not_pp, count, almost = count_pp_under_time_cut(lassoranker, 
                                                        args.time_cut)
        print("Solved (LR + PP) < {}: {} ({}/{})".format(args.time_cut,
                                                     count, not_pp, almost))
