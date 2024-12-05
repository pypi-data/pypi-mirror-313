from astropy.table import Table
import astropy.units as u
from astropy.utils.diff import report_diff_values
import numpy as np
import pytest
from madcubapy.io.spectracontainer import SpectraContainer
from madcubapy.io.spectracontainer import parse_row_spectral_axis
from madcubapy.utils.spectral import create_spectral_array

@pytest.fixture
def example_init_spec():
    bintable = Table({
        'DATA': [np.array([[1, 2],[3, 4]]), np.array([[5, 6],[7, 8]])],
        'RESTFRQ': [1, 2],
        'CHANNELS': [5, 5],
        'CDELT3': [3, 3],
        'CRPIX3': [3, 3],
        'CRVAL3': [3, 3],
        'BUNIT': ['Jy    ', 'Jy    '],
    })
    hist = Table({
        'user': ['dh', 'dh'],
        'command': ['copy()', 'paste()'],
        'date': ['20241121', '20241122']
    })
    return SpectraContainer(bintable, hist)

@pytest.fixture
def example_init_nohist_spec():
    bintable = Table({
        'DATA': [np.array([[1, 2],[3, 4]]), np.array([[5, 6],[7, 8]])],
        'RESTFRQ': [1, 2],
        'CHANNELS': [5, 5],
        'CDELT3': [3, 3],
        'CRPIX3': [3, 3],
        'CRVAL3': [3, 3],
        'BUNIT': ['Jy    ', 'Jy    '],
    })
    return SpectraContainer(bintable)

@pytest.fixture
def example_read_spec():
    # Create and return a Map instance to be used in tests
    return SpectraContainer.read(
        "madcubapy/io/tests/data/IRAS16293_position_8_TM2_spectra.spec"
    )

def test_read_spec(example_read_spec):
    assert isinstance(example_read_spec.bintable, Table)
    assert isinstance(example_read_spec.hist, Table)

def test_invalid_file():
    with pytest.raises(FileNotFoundError):
        SpectraContainer.read("nonexistent_file.spec")

def test_parse_row_spectral_axis(example_read_spec):
    bintable = parse_row_spectral_axis(example_read_spec.bintable[0])
    assert isinstance(bintable, np.ndarray) or isinstance(bintable, u.Quantity)

def test_spectral_container_generate_spectral_axes(example_init_spec):
    # bintable without units
    example_init_spec._generate_spectral_axes()
    assert (example_init_spec.bintable[0]['XAXIS'].all()
            == np.array([-3.,  0.,  3.,  6.,  9.]).all())
    # bintable with units
    example_init_spec.bintable['RESTFRQ'].unit = u.Hz
    example_init_spec._generate_spectral_axes()
    assert (example_init_spec.bintable[0]['XAXIS'].all()
            == np.array([-3.,  0.,  3.,  6.,  9.]).all() and
            example_init_spec.bintable['XAXIS'].unit == u.Hz)

def test_spectral_container_parse_data_units(example_init_spec):
    # correctly parsed units
    example_init_spec._parse_data_units()
    assert example_init_spec.bintable['DATA'].unit == u.Jy
    # unequal strings for BUNIT
    example_init_spec.bintable["BUNIT"] = ["Jy  ", "Jy"]
    example_init_spec._parse_data_units()
    assert example_init_spec.bintable['DATA'].unit == None

def test_copy_read(example_read_spec):
    spectra_container_copy = example_read_spec.copy()
    assert report_diff_values(
        spectra_container_copy.hist, example_read_spec.hist
    )
    assert report_diff_values(
        spectra_container_copy.bintable, example_read_spec.bintable
    )

def test_copy_init(example_init_spec):
    spectra_container_copy = example_init_spec.copy()
    assert report_diff_values(
        spectra_container_copy.hist, example_init_spec.hist
    )
    assert report_diff_values(
        spectra_container_copy.bintable, example_init_spec.bintable
    )

def test_copy_init_nohist(example_init_nohist_spec):
    spectra_container_copy = example_init_nohist_spec.copy()
    assert report_diff_values(
        spectra_container_copy.bintable, example_init_nohist_spec.bintable
    )
    assert spectra_container_copy.hist == example_init_nohist_spec.hist
    assert spectra_container_copy.hist == None
