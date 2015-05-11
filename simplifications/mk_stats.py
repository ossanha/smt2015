#!/usr/bin/env python

import re
import os
import logging
import argparse
import csv
import numpy as np
import matplotlib.pyplot as plt
import operator

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

def filter_keys(predicate, htbl):
    """
    Returns a dictionary containing only the keys of htbl for which
    the predicate is true.
    """
    d = dict()
    n = 0
    for k in htbl.keys():
        if predicate(k):
            d[k] = htbl[k]
            n += 1
    return n, d

def filter_items(predicate, htbl):
    """
    Returns a dictionary containing only the items of htbl for which
    the predicate is true.
    """
    d = dict()
    n = 0
    for k, v in htbl.items():
        if predicate(v):
            d[k] = v
            n += 1
    return n, d

def subset_to_lasso(d):
    _, d = filter_keys(lambda x: re.match(lassoranker_pat, x), d)
    return d

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

# Will containt the results for each file
results = dict()
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

    elements = t.split()
    prover = elements[0]
    ptype = elements[1]
    other = elements[2] if len(elements) > 2 else ""

    if not prover in results:
        results[prover] = dict()
    results[prover]["{}{}".format(ptype, other)] = data

    if type == "simp":
        not_pp, count, almost = count_pp_under_time_cut(data, args.time_cut)
        print("Solved (QF_LRA + PP) < {}: {} ({}/{})".format(args.time_cut,
                                                     count, not_pp, almost))
        not_pp, count, almost = count_pp_under_time_cut(lassoranker,
                                                        args.time_cut)
        print("Solved (LR + PP) < {}: {} ({}/{})".format(args.time_cut,
                                                     count, not_pp, almost))

## Treat the results
logging.debug("Provers: {}".format(len(results)))

def display(results, title):

  for prover, prover_results in results.items():
      print("\n\n# Summary for {}\n".format(prover))
      for k in results[prover].keys():
          logging.debug("{}:{}@".format(k,len(results[prover][k])))
      _, initial_proven_simp = filter_items(lambda x: x is not None, prover_results["simp_500s"])
      _, initial_proven_default = filter_items(lambda x: x is not None, prover_results["default"])
      _, initial_proven_default_500 = filter_items(lambda x: x is not None, prover_results["default_500s"])

      proven_simp = initial_proven_simp
      proven_default = initial_proven_default
      proven_default_500 = initial_proven_default
      def combat(title, d1, d1title, d2, d2title):
          l1 = len(d1)
          l2 = len(d2)
          m1, proven1 = filter_keys(lambda x: not x in d2, d1)
          print("{} {} {}/{} : {} ({}/{})".format(prover,
                                                  title,
                                                  d1title,
                                                  d2title, m1, l1, l2 ))
          m2, proven2 = filter_keys(lambda x: not x in d1, d2)
          print("{} {} {}/{}: {} ({}/{})".format(prover, title,
                                                 d2title, d1title, m2, l2, l1))
          return m1, m2
      combat("", proven_simp, "Simp", proven_default, "Default")
      combat("", proven_simp, "Simp", proven_default_500, "Default500")

      # With smtpp
      print("{} files have been preprocessed: now restricting analysis to them".format(len(smtpp_times)))
      f = (lambda x: x in smtpp_times and smtpp_times[x] is not None)
      _, proven_simp = filter_keys(f, proven_simp)
      _, proven_default = filter_keys(f, proven_default)
      _, proven_default_500 = filter_keys(f, proven_default_500)
      combat("SMTpp", proven_simp, "Simp", proven_default, "Default")
      combat("SMTpp", proven_simp, "Simp", proven_default_500, "Default500")

      ordered_proven_simp = sorted([ (k, v) for k, v in proven_simp.items()],
                                   key = operator.itemgetter(1))
      opsimp_values = [ v for _, v in ordered_proven_simp ]
      smtpp_values = [ smtpp_times[k] for k, _ in ordered_proven_simp ]
      smtpp_pct_values = [ 0 if x == 0 and y == 0 else 100 * y / (x + y)
                           for (x, y) in zip(opsimp_values, smtpp_values) ]


      # Under time limit
      cumulated = dict()
      for k, t in proven_simp.items():
          cumulated[k] = t + smtpp_times[k]
      max_cum = max([v for _, v in cumulated.items()])
      g = lambda x: x < args.time_cut
      default_500 = proven_default_500
      _, proven_cumulated = filter_items(g, cumulated)
      _, proven_default = filter_items(g, proven_default)
      _, proven_default_500 = filter_items(g, proven_default_500)
      print("Elements found under {}s".format(args.time_cut))
      combat("SMTpp", proven_cumulated, "Simp + smtpp", proven_default, "Default")
      combat("SMTpp", proven_cumulated, "Simp + smtpp", proven_default_500, "Default500")

      # lines for elements proven by both
      _, both_cumulated = filter_keys(lambda k: k in initial_proven_default_500, cumulated)
      _, both_default = filter_keys(lambda k: k in both_cumulated, initial_proven_default_500)
      l = [ (k, v) for k, v in both_default.items() ]
      default_ord = sorted(l, key=operator.itemgetter(1))
      both_cumulated_ord = [ both_cumulated[k] for k, _ in l ]
      both_default_ord = [ v for _, v in l]


      cum = []
      deflt = []
      diff_cum = []
      diff_deflt = []
      xaxis = range (20, 400, 20)
      for tcut in xaxis:
          print(tcut)
          filter = lambda x: x < tcut
          _, proven_cumulated = filter_items(filter, cumulated)
          _, proven_default_500 = filter_items(filter, default_500)
          p1, p2 = combat("SMTpp", proven_cumulated, "Simp + smtpp",
                          proven_default_500, "Default500")
          cum.append(len(proven_cumulated))
          deflt.append(len(proven_default_500))
          diff_cum.append(p1)
          diff_deflt.append(p2)

      plt.style.use('ggplot')
      fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
      ax1.plot(xaxis, cum, label="{} + {}".format(prover, "SMTpp"))
      ax1.plot(xaxis, deflt, lw = 2, c='green', label=prover)
      ax1.legend(loc=2)
      ax1.set_xlabel("Time limit (s)")
      ax1.set_ylabel("# scripts solved")
      ax1.set_title("Instances proven")
      ax1.axvline(max_cum)
      ax2.plot(xaxis, diff_cum, label = "{} + SMTpp".format(prover))
      ax2.plot(xaxis, diff_deflt, label = "{}".format(prover))
      ax2.set_xticks(range(len(cum)), xaxis)
      ax2.legend(loc=2)
      ax2.set_xlabel("Time limit (s)")
      ax2.set_ylabel("# scripts solved")
      ax2.set_title("Instances proven only by one combination")
      ax2.set_ylabel("Time (s)")

      ax3.plot(smtpp_pct_values, marker='o', linestyle='')
      ax3.set_title("Time % of SMTpp in solved instances")
      ax3.margins(0.01)

      ax4.plot(both_default_ord, both_default_ord)
      ax4.scatter(both_default_ord, both_cumulated_ord)
      ax4.set_title("No simp vs simp on common solved instances")

      plt.tight_layout()
      plt.show()

display(results, "QF_LRA")

lassoranker_results = dict()
for p, cat in results.items():
    lassoranker_results[p] = dict()
    for k, v in cat.items():
        lassoranker_results[p][k] = subset_to_lasso(v)

display(lassoranker_results, "LassoRanker")
