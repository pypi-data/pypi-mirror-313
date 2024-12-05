import astropy
from astropy.nddata import CCDData
from madcubapy.io import MadcubaMap
from madcubapy.visualization import add_wcs_axes
from madcubapy.visualization import add_manual_wcs_axes
from madcubapy.visualization import append_colorbar
from madcubapy.visualization import add_colorbar
from madcubapy.visualization import parse_clabel
import matplotlib as mpl
import matplotlib.pyplot as plt
from pathlib import Path
import pytest

@pytest.fixture
def example_madcuba_map():
    # Create and return a Map instance to be used in tests
    return MadcubaMap.read(
        "madcubapy/io/tests/data/IRAS16293_SO_2-1_moment0_madcuba.fits"
    )

def test_add_wcs_axes(example_madcuba_map):
    fig = plt.figure(figsize=(10,5))
    ax, img = add_wcs_axes(fig, 1, 2, 1, fitsmap=example_madcuba_map)
    assert isinstance(ax, astropy.visualization.wcsaxes.WCSAxes)
    assert isinstance(img, mpl.image.AxesImage)

def test_add_wcs_axes_without_arguments(example_madcuba_map):
    fig = plt.figure(figsize=(10,5))
    with pytest.raises(TypeError):
        add_wcs_axes(nrows=1, ncols=2, number=1, fitsmap=example_madcuba_map)
    with pytest.raises(TypeError):
        add_wcs_axes(fig=fig, nrows=1, ncols=2, number=1)

def test_add_wcs_axes_with_incorrect_types(example_madcuba_map):
    fig = plt.figure(figsize=(10,5))
    with pytest.raises(TypeError):
        add_wcs_axes(fig=3, nrows=1, ncols=2, number=1, fitsmap=example_madcuba_map)
    with pytest.raises(TypeError):
        add_wcs_axes(fig=fig, nrows=1, ncols=2, number=1, fitsmap=4)

def test_add_colorbar(example_madcuba_map):
    fig = plt.figure(figsize=(10,5))
    ax, img = add_wcs_axes(fig, 1, 2, 1, fitsmap=example_madcuba_map)
    cbar = add_colorbar(ax=ax, location='top', label='custom units')
    assert isinstance(cbar, mpl.colorbar.Colorbar)

def test_parse_clabel(example_madcuba_map):
    label = parse_clabel(example_madcuba_map)
    assert label == r'$I \ {\rm (Jy \ beam^{-1} \ m \ s^{-1})}$'
