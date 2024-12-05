from astropy.table import Table
import numpy as np
import pytest
from madcubapy.io.madcubafits import MadcubaFits

@pytest.fixture
def example_madcuba_fits_hist():
    # Create and return a Fits instance with hist table to be used in tests
    data = {
        'Index': [1, 2, 3],
        'FITS': ['C', 'C', 'C'],
        'Macro': ['Line 1', 'Line 2', 'Line 3'],
        'Type': ['Line 1', 'Line 2', 'Line 3'],
        'FROM_ROW': [np.ma.masked, np.ma.masked, np.ma.masked],
        'TO_ROW': [np.ma.masked, np.ma.masked, np.ma.masked],
        'Roi_Range': [np.ma.masked, np.ma.masked, np.ma.masked],
        'User': ['Line 1', 'Line 2', 'Line 3'],
        'Date': ['Line 1', 'Line 2', 'Line 3'],
    }
    table = Table(data)
    return MadcubaFits(hist=table)

def test_initialization_with_none():
    madcuba_fits = MadcubaFits()
    assert madcuba_fits.hist is None

def test_initialization_with_table():
    data = {'col1': [1, 2, 3], 'col2': [4, 5, 6]}
    table = Table(data)
    madcuba_fits = MadcubaFits(hist=table)
    assert isinstance(madcuba_fits.hist, Table)
    assert len(madcuba_fits.hist) == 3  # Check table length

def test_invalid_initialization_type():
    with pytest.raises(TypeError):
        MadcubaFits(hist="string")
    with pytest.raises(TypeError):
        MadcubaFits(hist=3)
    with pytest.raises(TypeError):
        MadcubaFits(hist=0.4)
    with pytest.raises(TypeError):
        MadcubaFits(hist=np.zeros(4,5))

def test_hist_setter():
    data = {'col1': [1, 2], 'col2': [3, 4]}
    table = Table(data)
    madcuba_fits = MadcubaFits()
    # Set hist to a valid table
    madcuba_fits.hist = table
    assert isinstance(madcuba_fits.hist, Table)
    assert len(madcuba_fits.hist) == 2
    # Set hist to None
    madcuba_fits.hist = None
    assert madcuba_fits.hist is None

def test_add_invalid_hist_file():
    madcuba_fits = MadcubaFits()
    with pytest.raises(FileNotFoundError):
        madcuba_fits.add_hist("nonexistent_file.csv")

def test_update_hist(example_madcuba_fits_hist):
    example_madcuba_fits_hist._update_hist(action="Fix temp", FITS='S')
    assert example_madcuba_fits_hist.hist[-1]['Index'] == 4
    assert example_madcuba_fits_hist.hist[-1]['FITS'] == 'S'
    assert example_madcuba_fits_hist.hist[-1]['Macro'] == '//PYTHON: Fix temp'
    assert example_madcuba_fits_hist.hist[-1]['Type'] == 'Py'
    assert example_madcuba_fits_hist.hist[-1]['FROM_ROW'] is np.ma.masked
    assert example_madcuba_fits_hist.hist[-1]['TO_ROW'] is np.ma.masked
    assert example_madcuba_fits_hist.hist[-1]['Roi_Range'] is np.ma.masked

def test_update_hist_protected(example_madcuba_fits_hist):
    with pytest.raises(ValueError):
        example_madcuba_fits_hist._update_hist(action="Fix temp", Index='S')
    with pytest.raises(ValueError):
        example_madcuba_fits_hist._update_hist(action="Fix temp", Macro='S')
    with pytest.raises(ValueError):
        example_madcuba_fits_hist._update_hist(action="Fix temp", User='S')
    with pytest.raises(ValueError):
        example_madcuba_fits_hist._update_hist(action="Fix temp", Date='S')

def test_update_hist_invalid(example_madcuba_fits_hist):
    with pytest.raises(ValueError):
        example_madcuba_fits_hist._update_hist(action="Fix temp", Any_name='S')

def test_update_hist_none():
    madcuba_fits = MadcubaFits()
    with pytest.raises(ValueError):
        madcuba_fits._update_hist(action="Fix temp")
