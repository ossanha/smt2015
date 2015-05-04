#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import csv
import sys

filename = sys.argv[1]
plt.style.use('ggplot')

def pp_uu(alldata):
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
    axes = [ax1, ax2, ax3, ax4]
    legends = alldata[0][1:]
    data = sorted( [(x, int(y), int(z)) for x,y,z in alldata[1:]], key=lambda d: d[1])
    for i in range(4):
        ax = axes[i]
        if i != 3:
            ldata = data[7*i:7*(i + 1)]
        else:
            ldata = data[7*i:]
        cat_names = [ x[0] for x in ldata ]
        npb = [ x[1] for x in ldata ]
        unused = [ x[2] for x in ldata ]
        N = len(ldata)
        ind = np.arange(N)                # the x locations for the groups
        width = 0.4                      # the width of the bars
        b_npb = ax.barh(ind+width, npb, width, color='0.6')

        b_unused = ax.barh(ind, unused, width, color='0')

        # axes and labels
        ax.set_ylim(-width,len(ind)+width)
        ax.set_xlim(0,1.15 * max(npb))
        ax.set_title(', '.join(cat_names), fontsize=10)
        ax.set_yticks(ind+width)
        xtickNames = ax.set_yticklabels(cat_names, fontsize=10)
        plt.setp(xtickNames)

        ## add a legend
        ax.legend( (b_npb[0], b_unused[0]), legends, loc=4 )
        def autolabel(rects):
            # attach some text labels
            for rect in rects:
                w = rect.get_width()
                ax.text(1.05 * w, rect.get_y(), '%d'%int(w), fontsize=12)

        autolabel(b_npb)
        autolabel(b_unused)
    #fig.tight_layout()
    #fig.savefig('uu.png', bbox_inches='tight', dpi=fig.dpi)
    plt.subplots_adjust(left=0.05, right=0.98, top=0.96, bottom=0.06)
    plt.show()


with open(filename) as csvfile:
    reader = csv.reader(csvfile)
    alldata = [ row for row in reader ]
    pp_uu(alldata)
