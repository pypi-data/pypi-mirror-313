import astropy.units as u
import numpy as np
import pytest
from madcubapy.utils.spectral import create_spectral_array

def test_create_spectral_array_without_units():
    # Test a specific array without units
    assert (create_spectral_array(8, 0.5, -3, 10).all()
         == np.array([11.5, 12, 12.5, 13, 13.5, 14, 14.5, 15]).all())

def test_create_spectral_array_with_units():
    # Test a specific array with units
    a = create_spectral_array(8, 0.5 * u.s, -3, 10)
    b = np.array([11.5, 12, 12.5, 13, 13.5, 14, 14.5, 15]) * u.s
    assert a.value.all() == b.value.all()
    assert a.unit == b.unit
