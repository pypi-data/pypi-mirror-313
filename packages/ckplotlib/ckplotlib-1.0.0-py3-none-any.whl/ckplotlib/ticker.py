"""
* Written by CK
"""
import numpy as np
from matplotlib.ticker import LogLocator, MaxNLocator, AutoMinorLocator

class WideLogAutoMinorLocator( AutoMinorLocator ):

    def __call__( self ):

        majorlocs = self.axis.get_majorticklocs()
        len_majorlocs = len( majorlocs )

        if self.ndivs is None:
            if len_majorlocs > 8:
                ndivs = 2
            else:
                ndivs = 5
        else:
            ndivs = self.ndivs

        exponent_majorstep = int( np.log10(
            majorlocs[1] / majorlocs[0]
        ))
        exponent_minorstep = exponent_majorstep / ndivs

        vmin, vmax = self.axis.get_view_interval()
        if vmin > vmax:
            vmin, vmax = vmax, vmin

        exponent_vmin = np.log10( vmin )
        exponent_vmax = np.log10( vmax )

        t0 = np.log10( majorlocs[0] )
        tmin = ((exponent_vmin - t0) // exponent_minorstep + 1) * exponent_minorstep
        tmax = ((exponent_vmax - t0) // exponent_minorstep + 1) * exponent_minorstep
        exponent_locs = np.arange(tmin, tmax, exponent_minorstep) + t0
        locs = 10**exponent_locs

        return self.raise_if_exceeds(locs)


class WideLogLocator( LogLocator ):

    def __init__(
            self,
            nbins   = 9,
            steps   = [5, 10],
            **kwargs
        ):
        self.maxNLocator = MaxNLocator(
            nbins   = nbins,
            steps   = steps,
            integer = True
        )
        super().__init__( **kwargs )

    def __call__(self):
        """Return the locations of the ticks."""
        vmin, vmax = self.axis.get_view_interval()
        tick_values = self.maxNLocator.tick_values(
            vmin = np.log10( vmin ),
            vmax = np.log10( vmax )
        )
        return 10**tick_values
