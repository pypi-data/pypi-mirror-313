"""
* Written by CK
"""
import matplotlib as mpl
import matplotlib.pyplot as plt
import os
from copy import copy
from glob import glob
from .. import get_configdir
from ..config import ckFigureConfig

CURRENT_DIR      = '.'
CPL_MPLSTYLE_DIR = os.path.dirname( __file__ )
CPL_CONFIG_DIR   = get_configdir()
MPL_CONFIG_DIR   = mpl.get_configdir()

SEARCH_DIRS = [
    CURRENT_DIR,
    CPL_CONFIG_DIR,
    MPL_CONFIG_DIR,
    CPL_MPLSTYLE_DIR
]


################################################################
# FontConstants
################################################################
#==============================================================#
# Arial for sans
#==============================================================#
try:
    from matplotlib._mathtext import _font_constant_mapping as mapping
    from matplotlib._mathtext import FontConstantsBase

    class ArialFontConstants( FontConstantsBase ):
        script_space   = 0.075
        subdrop        = 0.2
        sup1           = 0.4
        sub1           = 0.2
        sub2           = 0.3
        delta          = 0.075
        delta_slanted  = 0.3
        delta_integral = 0

    def _append_arial_font_constants():
        mapping.update( Arial = ArialFontConstants )

except:
    def _append_arial_font_constants():
        print( '[error] ckplotlib.mplstyle' )
        print( 'failed to set ArialFontConstants' )


#==============================================================#
# Times New Roman for serif
#==============================================================#
try:
    from matplotlib._mathtext import _font_constant_mapping as mapping
    from matplotlib._mathtext import ComputerModernFontConstants
    # from matplotlib._mathtext import STIXFontConstants
    class TimesNewRomanFontConstants( ComputerModernFontConstants ):
        pass

    # class TimesNewRomanFontConstants( STIXFontConstants ):
    #     pass

    def _append_times_font_constants():
        mapping.update( **{'Times New Roman': TimesNewRomanFontConstants} )

except:
    def _append_times_font_constants():
        print( '[error] ckplotlib.mplstyle' )
        print( 'failed to set TimesNewRomanFontConstants' )




################################################################
# use_mplstyle
################################################################
#==============================================================#
# use_mplstyle
#==============================================================#
def _get_mplstyle_path(
    mplstyle: str,
    dirs: list = []
) -> str | None:
    """
    search mplstyle file
    1. mplstyle (if "mplstyle" is path)
    2. search from directories sepecified as list of dirs
        - dirs[0]
        - dirs[1]
    """

    # mplstyle is written as path
    exists = os.path.isfile( mplstyle )
    if exists:
        return mplstyle


    fname = mplstyle
    FMT_LEN = 9
    FMT = '.mplstyle'

    if len( fname ) > FMT_LEN:
        wo_fmt = not fname[-FMT_LEN:] == FMT
    else:
        wo_fmt = True

    if wo_fmt:
        fname = f'{mplstyle}.mplstyle'

    for mplstyle_dir in dirs:
        if mplstyle_dir == CURRENT_DIR:
            # recursive option is not used to avoid searching a lot of files
            mplstyle_path_list = glob( f'{mplstyle_dir}/{fname}' )
        else:
            mplstyle_path_list = glob( f'{mplstyle_dir}/**/{fname}', recursive = True )

        if len( mplstyle_path_list ) > 0:
            return mplstyle_path_list[0]

        # path = os.path.join(
        #     mplstyle_dir,
        #     fname
        # )
        # exists = os.path.isfile( path )
        # if exists:
        #     return path


    # error
    print( '[error] ckplotlib.mplstyle._get_mplstyle_path' )
    print( f'invalid mplstyle name "{mplstyle}".' )
    return None


def get_mplstyle_path(
    mplstyle: str,
    dirname: str|None = None
) -> str | None:
    """
    search & return mplstyle file
    if "mplstyle" is path:
        return "mplstyle"
    else:
        search from directories
        1. dirname [if is not None]
        2. current directory
        3. CPL_MPLSTYLE_DIR
        4. MPL_CONFIG_DIR
    """

    search_dirs = SEARCH_DIRS.copy()
    if dirname is not None:
        search_dirs.insert( 0, dirname )

    mplstyle = _get_mplstyle_path(
        mplstyle = mplstyle,
        dirs     = search_dirs
    )

    if ckFigureConfig.show_mplstyle_src:
        print( f' > mplstyle: "{mplstyle}"' )
    return mplstyle


def use_mplstyle(
    mplstyle: str,
    dirname: str|None = None,
    use: bool = False
) -> dict:
    """
    search mplstyle file
    if "mplstyle" is path:
        use "mplstyle"
    else:
        search from directories
        1. dirname [if is not None]
        2. current directory
        3. CPL_MPLSTYLE_DIR
        4. MPL_CONFIG_DIR
    """
    mplstyle = get_mplstyle_path(
        mplstyle = mplstyle,
        dirname  = dirname
    )

    props = {}
    if mplstyle is not None:
        if use:
            plt.style.use( mplstyle )
        props.update( **_mplstyle2dict( mplstyle ) )

    return props


def _strip_comment( s: str ) -> str:
    """
    cited from matplotlib.cbook
    Strip everything from the first unquoted #.
    """
    pos = 0
    while True:
        quote_pos = s.find('"', pos)
        hash_pos = s.find('#', pos)
        if quote_pos < 0:
            without_comment = s if hash_pos < 0 else s[:hash_pos]
            return without_comment.strip()
        elif 0 <= hash_pos < quote_pos:
            return s[:hash_pos].strip()
        else:
            closing_quote_pos = s.find('"', quote_pos + 1)
            if closing_quote_pos < 0:
                raise ValueError(
                    f"Missing closing quote in: {s!r}. If you need a double-"
                    'quote inside a string, use escaping: e.g. "the \" char"')
            pos = closing_quote_pos + 1  # behind closing quote

def _mplstyle2dict( fname: str ) -> dict:
    rc_temp = {}
    with open( fname ) as fd:
        for line_no, line in enumerate( fd, 1 ):

            strippedline = _strip_comment( line )
            if not strippedline:
                continue
            tup = strippedline.split( ':', 1 )
            if len(tup) != 2:
                print(
                    'Missing colon in file %r, line %d (%r)',
                    fname, line_no, line.rstrip('\n')
                )
                continue
            key, val = tup
            key = key.strip()
            val = val.strip()
            if val.startswith('"') and val.endswith('"'):
                val = val[1:-1]  # strip double quotes
            if key in rc_temp:
                print(
                    'Duplicate key in file %r, line %d (%r)',
                    fname, line_no, line.rstrip('\n')
                )
            # rc_temp[key] = (val, line, line_no)
            rc_temp[key] = val

    return rc_temp


#==============================================================#
# use_mplstyle_base
#==============================================================#
def use_mplstyle_base( use: bool = True ) -> dict:
    """
    - import base.mplstyle
    """
    mplstyle_path = get_mplstyle_path( 'base.mplstyle' )
    if mplstyle_path is not None:
        if use:
            plt.style.use( mplstyle_path )
        return _mplstyle2dict( mplstyle_path )
    else:
        return {}


#==============================================================#
# use_mplstyle_font
#==============================================================#
def use_mplstyle_font(
    mplstyle: str = ckFigureConfig.mplstyle_font,
    adjust_mathtext_space_ratio: float | None = 0.4,
    use: bool = True,
    append_font_constants_func = None
) -> dict:
    """
    ### use_mplstyle
    - import font mplstyle
        - font: 'arial' or 'times' [defalut: 'arial']
        - font mplstyle is searched from
            if mplstyle is path:
                use mplstyle
            else:
                search from directories of
                1. currect directory
                2. f'{CPL_MPLSTYLE_DIR}/font'
                3. MPL_CONFIG_DIR
    - adjust mathtext space [optional]
        - adjust_mathtext_space_ratio: [default: 0.4]
        (no change if the ratio is 1)
    - append_font_constants_func [optional]
        - if you manually make `FontConstants`,
        define callable function to append thy `FontConstants`
        to `matplotlib._mathtext._font_constant_mappingis`
    """
    if mplstyle is None or mplstyle == 'none':
        print( 'no fonts are specified' )
        return {}


    mplstyle_path = get_mplstyle_path( mplstyle )
    if mplstyle_path is not None:
        if use:
            plt.style.use( mplstyle_path )
        props = _mplstyle2dict( mplstyle_path )
    else:
        props = {}


    # append FontConstants to matplotlib._mathtext._font_constant_mapping
    if callable( append_font_constants_func ):
        append_font_constants_func()
    elif mplstyle == 'arial':
        _append_arial_font_constants()
    elif mplstyle == 'times':
        _append_times_font_constants()


    if adjust_mathtext_space_ratio is not None:
        adjust_mathtext_space(
            make_space_ratio = adjust_mathtext_space_ratio
        )

    return props




################################################################
# adjust_mathtext_space
################################################################
try:
    from matplotlib._mathtext import Parser as Parser_
    Parser = copy( Parser_ )
    Parser._make_space_original = copy( Parser._make_space )
    Parser._make_space_ck_ratio = 1

    def _make_space( self, percentage ):
        new_percentage = percentage * self._make_space_ck_ratio
        return self._make_space_original( new_percentage )

    Parser._make_space = _make_space
    Parser_ = Parser

except:
    pass


def adjust_mathtext_space( make_space_ratio: float = 0.4 ):
    """
    if ratio is 1: space does not change
    """
    try:
        from matplotlib._mathtext import Parser
        Parser._make_space_ck_ratio = make_space_ratio
    except:
        pass
