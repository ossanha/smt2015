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
    data = sorted( [(x, int(y), int(z), int(w)) for x,y,z,w \
                    in alldata[1:]], key=lambda d: d[1])
    for i in range(4):
        ax = axes[i]
        if i != 3:
            ldata = data[7*i:7*(i + 1)]
        else:
            ldata = data[7*i:]
        cat_names = [ x[0] for x in ldata ]
        npb = [ x[1] for x in ldata ]
        over = [ x[2] for x in ldata ]
        under = [ x[3] for x in ldata ]
        N = len(ldata)
        ind = np.arange(N)                # the x locations for the groups
        width = 0.25                      # the width of the bars
        b_npb = ax.barh(ind+2*width, npb, width, color='0.6')

        b_over = ax.barh(ind+width, over, width, color='0.3')
        b_under = ax.barh(ind, under, width, color='0')

        # axes and labels
        ax.set_ylim(-width,len(ind)+width)
        ax.set_xlim(0,1.15 * max(npb))
        ax.set_title(', '.join(cat_names), fontsize=10)
        ax.set_yticks(ind+width)
        xtickNames = ax.set_yticklabels(cat_names, fontsize=10)
        plt.setp(xtickNames)

        ## add a legend
        ax.legend( (b_npb[0], b_over[0], b_under[0]), legends, loc=4 )
        def autolabel(rects):
            # attach some text labels
            for rect in rects:
                w = rect.get_width()
                ax.text(1.05 * w, rect.get_y(), '%d'%int(w), fontsize=10)

        autolabel(b_npb)
        autolabel(b_over)
        autolabel(b_under)
    #fig.tight_layout()
    #fig.savefig('uu.png', bbox_inches='tight', dpi=fig.dpi)
    plt.subplots_adjust(left=0.05, right=0.98, top=0.96, bottom=0.06)
    plt.show()


with open(filename) as csvfile:
    reader = csv.reader(csvfile)
    alldata = [ row for row in reader ]
    pp_uu(alldata)


# y = [[ "AUFLIRA", 20014, 1370, 0, 1370         ],
#      [ "QF_ABV", 15091, 0, 0, 0               ],
#      [ "UFLIA", 12138 , 2282 , 310   , 1972  ],
#      [ "QF_NRA", 11540 , 0    , 0     , 0     ],
#      [ "QF_NIA", 9359 , 0     , 0     , 0     ],
#      [ "QF_UF", 6650 , 0     , 0     , 0     ],
#      [ "QF_LIA", 6141 , 4079  , 3958  , 121   ],
#      [ "UF", 5748 , 32    , 0     , 32    ],
#      [ "NRA", 3813 , 0     , 0     , 0     ],
#      [ "QF_IDL", 2188 , 13    , 13    , 0     ]
# ]

# ## the data
# names = [ l[0] for l in y]
# nproblems = [ l[1] for l in y]
# alarms    = [ l[2] for l in y]
# under     = [ l[4] for l in y]
# over     = [ l[3] for l in y]
# print(nproblems, alarms, under)

# N = len(y)

# ## necessary variables
# ind = np.arange(N)                # the x locations for the groups
# width = 0.15                      # the width of the bars

# ## the bars
# rects1 = ax.bar(ind, nproblems, width,
#                 color='black')

# rects2 = ax.bar(ind+width, alarms, width,
#                     color='green',
#                     )

# rects3 = ax.bar(ind+2*width, under, width,
#                     color='red',
#                     )
# rects4 = ax.bar(ind+3*width, over, width,
#                     color='blue',
#                     )


# # axes and labels
# ax.set_xlim(-width,len(ind)+width)
# ax.set_ylim(0,21000)
# ax.set_ylabel('#')
# ax.set_title('Alarms')
# ax.set_xticks(ind+width)
# xtickNames = ax.set_xticklabels(names)
# plt.setp(xtickNames, rotation=45, fontsize=10)

# ## add a legend
# ax.legend( (rects1[0], rects2[0], rects4[0], rects3[0]), ('#', 'alarms', 'over', 'under') )

# plt.show()
