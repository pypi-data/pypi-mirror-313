"""
* Written by CK
"""
import sys
import matplotlib.pyplot as plt
from cycler import cycler, Cycler
from .color import ckcolor, matplotlib_colors

def make_cycle( **kwargs ) -> Cycler:
    return (
        cycler(**kwargs)
    )


#==============================================================#
# cycle
#==============================================================#
ck_cycle = cycler( color = [
    'k',
    ckcolor['red'       ],
    ckcolor['blue'      ],
    ckcolor['lightblue' ],
    ckcolor['green'     ],
    ckcolor['orange'    ],
    ckcolor['magenta'   ]
])
mpl_cycle = cycler( color = matplotlib_colors )


cycle_8colors = make_cycle(
    color = [
        'k',
        ckcolor['red'       ],
        ckcolor['magenta'   ],
        ckcolor['orange'    ],
        '#9ccc6c',
        ckcolor['green'     ],
        ckcolor['lightblue' ],
        ckcolor['blue'      ]
    ]
)
cycle_7colors = make_cycle(
    color = [
        'k',
        ckcolor['red'       ],
        ckcolor['magenta'   ],
        ckcolor['orange'    ],
        ckcolor['green'     ],
        ckcolor['lightblue' ],
        ckcolor['blue'      ]
    ]
)
cycle_6colors = make_cycle(
    color = [
        'k',
        ckcolor['red'       ],
        ckcolor['orange'    ],
        ckcolor['green'     ],
        ckcolor['lightblue' ],
        ckcolor['blue'      ]
    ]
)
cycle_5colors = make_cycle(
    color = [
        'k',
        ckcolor['red'       ],
        ckcolor['green'     ],
        ckcolor['lightblue' ],
        ckcolor['blue'      ]
    ]
)
cycle_4colors = make_cycle(
    color = [
        'k',
        ckcolor['red'       ],
        ckcolor['green'     ],
        ckcolor['blue'      ]
    ]
)



cycle_br = make_cycle(
    color = [
        ckcolor['blue'],
        ckcolor['red']
    ]
)

cycle_rb = make_cycle(
    color = [
        ckcolor['red'],
        ckcolor['blue']
    ]
)

cycle_krb = make_cycle(
    color = [
        'k',
        ckcolor['red'],
        ckcolor['blue']
    ]
)

cycle_kbr = make_cycle(
    color = [
        'k',
        ckcolor['blue'],
        ckcolor['red']
    ]
)


cycles = dict(
    colors8 = cycle_8colors,
    colors7 = cycle_7colors,
    colors6 = cycle_6colors,
    colors5 = cycle_5colors,
    colors4 = cycle_4colors,
    br  = cycle_br,
    rb  = cycle_rb,
    kbr = cycle_kbr,
    krb = cycle_krb
)


#==============================================================#
# skip cycle
#==============================================================#
def skip_cycle(
    ax: plt.Axes | None = None
) -> None:
    """
    advance cycler
    """

    if ax is None:
        ax = plt.gca()

    try:
        """
        ####################################
        # matplotlib ver. >= 3.8           #
        ####################################
        >>> pprint( vars( ax._get_lines ) )
        {
            '_cycler_items': [
                {'color': 'k', 'marker': 's', 'markersize': 6}},
                {'color': '#b5443c', 'marker': 'o', 'markersize': 6},
                {'color': '#6b8d4d', 'marker': 'D', 'markersize': 5},
                ...
                {'color': '#1894b1', 'marker': '>', 'markersize': 5}
            ],
            '_idx': 0,
            '_prop_keys': {
                'marker', 'markersize', 'color'
            },
            'command': 'plot'
        }
        """
        ax._get_lines._idx = (ax._get_lines._idx + 1) % len(ax._get_lines._cycler_items)

    except:
        try:
            """
            ####################################
            # matplotlib ver. < 3.8            #
            ####################################
            >>> pprint( vars( ax._get_lines ) )
            {
                '_prop_keys': {'color'},
                'axes': <Axes: >,
                'command': 'plot',
                'prop_cycler': <itertools.cycle object>
            }
            """
            # matplotlib ver. < 3.8
            next(ax._get_lines.prop_cycler)

        except:
            print( '[error] ckplotlib.mplprops.skip_cycle' )
            print( 'failed to skip prop_cycler.' )


#==============================================================#
# restart cycle
#==============================================================#
def restart_cycle(
    i:         int,
    cycle_len: int,
    ax:        plt.Axes | None = None
) -> None:
    if ax is None:
        ax = plt.gca()

    for _ in range( i, cycle_len ):
        skip_cycle( ax = ax )
