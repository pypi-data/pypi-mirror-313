from ._version import version
import os
__version__ = version


def get_configdir() -> str:
    CONFIGDIR = os.path.join(
        os.path.expanduser( '~' ),
        '.config'
    )
    return os.path.join(
        CONFIGDIR,
        'ckplotlib'
    )
