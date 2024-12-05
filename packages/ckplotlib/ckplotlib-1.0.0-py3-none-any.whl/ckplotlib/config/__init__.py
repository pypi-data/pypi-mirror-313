"""
* Written by CK
"""
import os
import sys
import configparser
from dataclasses import dataclass

from .. import get_configdir
from ..cycle import ck_cycle, mpl_cycle

FNAME = 'config.ini'

CONFIG_FILE = os.path.join(
    os.path.dirname( __file__ ),
    FNAME
)
CONFIG_FILE_HOME = os.path.join(
    get_configdir(),
    FNAME
)

@dataclass
class CkFigureConfig:
    png: bool
    svg: bool
    csv: bool
    use_mplstyle_base: bool
    show_mplstyle_src: bool
    show_savefname: bool
    inline_show: bool
    close: bool
    mplstyle_font: str
    cycle: str
    legend_bbox_to_anchor: tuple
    png_dpi: int
    svg_dpi: int

    def __post_init__( self ):
        if self.cycle == 'mpl':
            # self.default_cycle = mpl_cycle
            self.default_cycle = None
        else:
            self.default_cycle = ck_cycle

        # is_error = False
        # if is_error:
        #     print( '[error] ckplotlib.config' )
        #     print( f'{error_msg} in the ".ini" file' )
        #     sys.exit(1)



def _str2tuple( liststr: str ) -> tuple:
    return tuple( map(
        float,
        liststr.strip('()').strip('[]').split(',')
    ))


#==============================================================#
# read initialization files
#==============================================================#
config_files = [ CONFIG_FILE ]
if os.path.isfile( CONFIG_FILE_HOME ):
    config_files.append( CONFIG_FILE_HOME )

iniread = configparser.RawConfigParser()
iniread.read( config_files )

ini_ckfigure = iniread[ 'ckfigure' ]
ini_save     = iniread[ 'save' ]


#==============================================================#
# get ckFigureConfig
#==============================================================#
ckFigureConfig = CkFigureConfig(
    png = ini_save.getboolean( 'png' ),
    svg = ini_save.getboolean( 'svg' ),
    csv = ini_save.getboolean( 'csv' ),
    png_dpi = int( ini_save[ 'png_dpi' ] ),
    svg_dpi = int( ini_save[ 'svg_dpi' ] ),
    use_mplstyle_base = ini_ckfigure.getboolean( 'use_mplstyle_base' ),
    show_mplstyle_src = ini_ckfigure.getboolean( 'show_mplstyle_src' ),
    show_savefname    = ini_ckfigure.getboolean( 'show_savefname' ),
    inline_show       = ini_ckfigure.getboolean( 'inline_show' ),
    close             = ini_ckfigure.getboolean( 'close' ),
    mplstyle_font     = ini_ckfigure[ 'mplstyle_font' ],
    cycle             = ini_ckfigure[ 'cycle' ],
    legend_bbox_to_anchor = _str2tuple( ini_ckfigure[ 'legend_bbox_to_anchor' ] )
)

# from pprint import pprint
# pprint( vars( ckFigureConfig ) )
