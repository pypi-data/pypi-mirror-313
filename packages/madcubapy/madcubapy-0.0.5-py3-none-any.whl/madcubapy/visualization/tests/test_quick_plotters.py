import astropy
from astropy.nddata import CCDData
from madcubapy.io import MadcubaMap
from madcubapy.visualization import are_equal
from pathlib import Path
import pytest

@pytest.fixture
def example_madcuba_map():
    # Create and return a Map instance to be used in tests
    return MadcubaMap.read(
        "madcubapy/io/tests/data/IRAS16293_SO_2-1_moment0_madcuba.fits"
    )

def test_are_equal(example_madcuba_map):
    assert are_equal(example_madcuba_map, example_madcuba_map.ccddata)
