"""
* Written by CK
"""
from matplotlib.colors import LinearSegmentedColormap

#==============================================================#
# colors
#==============================================================#
ckcolor = dict(
    red       = '#b5443c',
    magenta   = '#d85786',
    orange    = '#e7a758',
    green     = '#6b8d4d',
    lightblue = '#1894b1',
    blue      = '#175487',
    grey      = '#515151',
    gray      = '#515151',
    lightgrey = '#848484',
    lightgray = '#848484'
)

ckcolors = [
    ckcolor['red'       ],
    ckcolor['magenta'   ],
    ckcolor['orange'    ],
    ckcolor['green'     ],
    ckcolor['lightblue' ],
    ckcolor['blue'      ]
]

matplotlib_colors = [
    '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
    '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
]


#==============================================================#
# cmap
#==============================================================#
_colors = ['royalblue','white','indianred']
cmap_bwr = LinearSegmentedColormap.from_list('custom', _colors)

_colors = ['mediumturquoise', '#e270ff']
cmap_br = LinearSegmentedColormap.from_list('custom', _colors)

_colors = ['mediumturquoise', 'dimgrey', 'indianred']
cmap = LinearSegmentedColormap.from_list('custom', _colors)

ckcmap = LinearSegmentedColormap.from_list(
    'custom',
    list( reversed( ckcolors ) )
)
# _colors = [
#     '#b43867', # red
#     '#e39761', # orange
#     '#83a14f', # green
#     '#0a82ae', # light blue
#     '#1c3f75' # blue
# ]
# cmap_ck = LinearSegmentedColormap.from_list(
#     'ck', _colors
# )
