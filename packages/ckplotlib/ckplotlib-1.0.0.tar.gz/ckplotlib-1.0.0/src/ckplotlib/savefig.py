"""
* Written by CK
"""
import matplotlib.pyplot as plt
import os
import pickle
from .config import ckFigureConfig

SAVE_PARAMS = dict(
    bbox_inches = 'tight',
    pad_inches  = 0.2
)

def _print_savepath( path: str ) -> None:
    if ckFigureConfig.show_savefname:
        print( f' > {path}' )


def savefig(
    fname: str,
    dirname:    str | None = None,
    fig: plt.Figure | None = None,
    png:         bool = ckFigureConfig.png,
    svg:         bool = ckFigureConfig.svg,
    pkl:         bool = False,
    pgf:         bool = False,
    png_dpi:     int  = ckFigureConfig.png_dpi,
    svg_dpi:     int  = ckFigureConfig.svg_dpi,
    replace:     bool = True,
    save_params: dict = SAVE_PARAMS,
    **kwargs
) -> None:

    if fig is None: fig = plt.gcf()

    save_fname = fname
    if dirname is not None:
        os.makedirs( dirname, exist_ok=True )
        save_fname = os.path.join( dirname, fname )

    if png:
        save_fpath = f'{save_fname}.png'
        if replace or not os.path.isfile( save_fpath ):
            _print_savepath( save_fpath )
            fig.savefig(
                save_fpath,
                format = 'png',
                dpi    = png_dpi,
                **save_params,
                **kwargs
            )

    if svg:
        save_fpath = f'{save_fname}.svg'
        if replace or not os.path.isfile( save_fpath ):
            _print_savepath( save_fpath )
            fig.savefig(
                save_fpath,
                format = 'svg',
                dpi    =  svg_dpi,
                **save_params,
                **kwargs
            )

    if pgf:
        save_fpath = f'{save_fname}.pgf'
        if replace or not os.path.isfile( save_fpath ):
            _print_savepath( save_fpath )
            fig.savefig(
                save_fpath,
                format = 'pgf',
                **save_params,
                **kwargs
            )

    if pkl:
        save_fpath = f'{save_fname}.pkl'
        if replace or not os.path.isfile( save_fpath ):
            _print_savepath( save_fpath )
            with open( save_fpath, 'wb' ) as f:
                pickle.dump(fig, f)

