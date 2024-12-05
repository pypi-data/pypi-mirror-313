import astropy
import astropy.units as u
import numpy as np


def create_spectral_array(nchan, cdelt, crpix, crval):
    """
    Create a spectral axis array.

    Parameters
    ----------
    nchan : int
        Number of channels in the spectrum.
    cdelt : float or astropy.units.Quantity
        Width of a channel.
    crpix : float
        Reference channel in the spectrum.
    crval : float
        Value of the reference channel in the spectrum.
    
    Return
    ------
    spectral_array : np.array or astropy.units.Quantity
        Returned spectral axis array with units if cdelt is a quantity

    """

    # if cdelt has units
    if isinstance(cdelt, astropy.units.Quantity):
        first_chan = crval - (cdelt.value * crpix)
        last_chan = crval + (cdelt.value * (nchan-1 - crpix))
        spectral_array = np.linspace(first_chan, last_chan, nchan) * cdelt.unit
    # if cdelt is adimensional
    else:
        first_chan = crval - (cdelt * crpix)
        last_chan = crval + (cdelt * (nchan-1 - crpix))
        spectral_array = np.linspace(first_chan, last_chan, nchan)

    return spectral_array
    