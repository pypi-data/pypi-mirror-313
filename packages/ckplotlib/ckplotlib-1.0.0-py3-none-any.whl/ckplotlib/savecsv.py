"""
* Written by CK
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

from .config import ckFigureConfig


class _CkLineProps():

    def __init__( self, *args ):
        if len( args ) == 1:
            self.name_y = args[0]
        elif len( args ) == 2:
            self.name_x = args[0]
            self.name_y = args[1]
        else:
            print( '[error] ckplotlib.savecsv._CkLineProps.__init__' )
            print( 'The number of arguments must be one or two.' )
            sys.exit(1)


def _get_line(
    line: plt.Line2D | None,
    ax:   plt.Axes   | None
) -> plt.Line2D:
    if line is None:
        if ax is None:
            ax = plt.gca()
        lines = ax.get_lines()

        if len( lines ) == 0:
            print( '[error] line does not exist.' )
            sys.exit(1)

        line = lines[-1]

    return line


def addlinename(
    *args: str,
    line: plt.Line2D | None = None,
    ax:   plt.Axes   | None = None
) -> None:
    """
    - args:
        - if the number of args is
        - one: name_y
        - two: name_x, name_y
        - otherwise: error
    - line:
        line object is automatically determined to be ax.get_lines()[-1]
        if not specified
    - ax:
        [used when line is not specified]
        - line is searched from ax.
        - ax object is automatically determined to be plt.gca()
        if not specified
    """
    line = _get_line(
        line = line,
        ax   = ax
    )

    line.ckLineProps = _CkLineProps( *args )



#==============================================================#
# supporting function
#==============================================================#
def _get_ax_data(
    ax:    plt.Axes         | None = None,
    lines: list[plt.Line2D] | None = None,
    common_x:   bool = False,
    col_prefix: str  = '',
    col_suffix: str  = '',
    show_msg:   bool = True
) -> list[ pd.DataFrame ]:

    if ax is None: ax = plt.gca()

    # "lines" has priority over "ax.get_lines()"
    lines = ax.get_lines() if lines is None else lines
    len_lines = len( lines )

    ### check
    if len_lines == 0:
        print( '[error] plot data does not exist.' )
        sys.exit(1)

    line0 = lines[0]
    common_x_col = 'x'
    ckLineProps  = getattr( line0, 'ckLineProps', False )
    if ckLineProps:
        common_x_col = getattr( ckLineProps, 'name_x', common_x_col )


    # common_x check
    if common_x:
        x0, _ = line0.get_data()

        common = True
        for line in lines:
            _x, _ = line.get_data()
            if np.size( x0 ) == np.size( _x ):
                if not np.allclose( x0, _x ):
                    common = False
            else:
                common = False

        if not common:
            if show_msg:
                print( '   * ckplotlib.savecsv' )
                print( '       * x data arrays are not common.' )
                print( '       * common_x is changed to False.' )
                show_msg = False
            common_x = False


    dfs = []
    xcols = []
    ycols = []
    for i, line in enumerate( lines ):
        x, y = line.get_data()
        ckLineProps = getattr( line, 'ckLineProps', False )

        xcol = common_x_col if common_x or len_lines==1 else f'x{i+1}'
        ycol = f'y'         if len_lines==1             else f'y{i+1}'

        xcol = f'{col_prefix}{xcol}{col_suffix}'
        ycol = f'{col_prefix}{ycol}{col_suffix}'

        if ckLineProps:
            if not common_x:
                xcol = getattr( ckLineProps, 'name_x', xcol )
            ycol = getattr( ckLineProps, 'name_y', ycol )

        xcols.append( xcol )
        ycols.append( ycol )

        df = pd.DataFrame(
            np.array([ x, y ]).T,
            columns = [ xcol, ycol ]
        )
        dfs.append( df )


    # duplicates check
    if len_lines > 1:
        if ycols[0] in ycols[1:]:
            print( '[error] ckplotlib.savecsv._get_ax_data' )
            print( 'y column names are duplicates.' )
            print( f'names = {ycols}' )
            sys.exit(1)

        if not common_x:
            if xcols[0] in xcols[1:]:
                print( '[error] ckplotlib.savecsv._get_ax_data' )
                print( 'When common_x option is False, x columns names must not be duplicates.' )
                print( f'names = {xcols}' )
                sys.exit(1)


    if common_x:
        new_dfs = dfs[0]
        for df in dfs[1:]:
            new_dfs = pd.concat(
                [ new_dfs, df.iloc[:,1] ],
                axis = 1,
                join = 'inner'
            )
            # new_dfs = pd.merge(
            #     new_dfs,
            #     df,
            #     how = 'inner',
            #     on  = xcol
            # )
    else:
        new_dfs = pd.concat(
            dfs,
            axis = 1,
            join = 'outer'
        )

    return new_dfs, show_msg


def _get_fig_data(
    fig: plt.Figure | None = None,
    common_x:         bool = False,
    subplot_common_x: bool = False
) -> list[ pd.DataFrame ]:

    if fig is None: fig = plt.gcf()

    dfs = []
    axes = fig.get_axes()
    axes_len = len( axes )
    col_prefix = ''
    col_suffix = ''
    show_msg = True
    for i, ax in enumerate( axes ):
        if axes_len > 1:
            col_prefix = f'f{i+1}['
            col_suffix = ']'
        df, show_msg = _get_ax_data(
            ax         = ax,
            common_x   = common_x,
            col_prefix = col_prefix,
            col_suffix = col_suffix,
            show_msg   = show_msg
        )
        dfs.append( df )


    if common_x and subplot_common_x:
        new_dfs = dfs[0]
        # xcol    = dfs[0].columns[0]
        xcol_left = dfs[0].columns[0]
        for df in dfs[1:]:
            # print(df)
            xcol_right = df.columns[0]
            new_dfs = pd.merge(
                new_dfs,
                df,
                how      = 'outer',
                left_on  = xcol_left,
                right_on = xcol_right
            )
            new_dfs = new_dfs.drop(
                columns = xcol_right
            )
        new_dfs = new_dfs.rename(
            columns = { xcol_left: 'x'}
        )

    else:
        new_dfs = pd.concat(
            dfs,
            axis = 1,
            join = 'outer'
        )

    return new_dfs



def _write_header(
    path:   str,
    header: str
) -> None:

    with open( path, mode='w' ) as f:
        f.write( header + '\n' )


#==============================================================#
# main
#==============================================================#
def savecsv(
    fname,
    fig: plt.Figure | None = None,
    dirname:    str | None = None,
    header:     str | None = None,
    common_x:         bool = False,
    subplot_common_x: bool = False
) -> None:


    dfs = _get_fig_data(
        fig              = fig,
        common_x         = common_x,
        subplot_common_x = subplot_common_x
    )

    save_path = f'{fname}.csv'
    if dirname is not None:
        os.makedirs( dirname, exist_ok=True )
        save_path = os.path.join( dirname, save_path )

    if header is None:
        mode = 'w'
    else:
        mode = 'a'
        _write_header(
            path   = save_path,
            header = header
        )

    if ckFigureConfig.show_savefname:
        print( f' > {save_path}' )

    dfs.to_csv(
        save_path,
        index = False,
        mode  = mode
    )
