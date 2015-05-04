#!/usr/bin/env python3

import csv
filename="res.csv"
out = "parser_table.tex"

with open(filename) as csvfile:
    reader = csv.reader(csvfile)
    data = [ r for r in reader ]
    headers = data[0]
    tools = [ "{\\sf " + d[0].replace('_', ' ') + "}" for d in data[1:]]
    places = [ d[1:] for d in data[1:]]
    categories = [ "{\\sf " + s.upper().replace('_', '\\_') + "}" for s in headers[1:] ]
    l = len(categories)
    fout = open(out, 'w')
    def pp_helper(cat, data):
        fout.write("\\resizebox{\\textwidth}{!}{\n")
        #fout.write("\\begin{center}\n")
        fout.write("\\begin{tabular}{|l|" + '|'.join(['c' for _ in range( len(cat))]) + '|}\n')
        fout.write("\\hline\n")
        fout.write("Tools &")
        fout.write(' & '.join(cat) + "\\\\\n\\hline\n")
        for i, d in enumerate(data):
            fout.write(tools[i] + " & ")
            fout.write(' &'.join([ n.replace('_', ' ') for n in d]) + "\\\\\n\\hline\n")
        fout.write("\\end{tabular}")
        #fout.write("\\end{center}\n\n")
        fout.write("}\n")

    lim = 16
    pp_helper(categories[: lim], [ d[: lim] for d in places])
    fout.write("\n \\vspace*{.3cm} \n")
    pp_helper(categories[lim :], [ d[lim :] for d in places])


    fout.close()
