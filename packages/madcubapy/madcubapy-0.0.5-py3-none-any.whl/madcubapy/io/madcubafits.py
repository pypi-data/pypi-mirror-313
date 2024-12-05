import astropy
from astropy.table import Table
from datetime import datetime
import numpy as np
import os
from pathlib import Path


class MadcubaFits:
    """A basic class describing a MADCUBA Fits object with its hist file.

    The MadcubaFits class contains the only object shared by MADCUBA maps,
    cubes, and spectra: an Astropy Table describing the history file exported
    by MADCUBA.

    Parameters
    ----------
    hist : `astropy.table.Table`
        An astropy Table object containing the history information of the fits
        file, which is stored in a separate _hist.csv file.

    """
    def __init__(
        self,
        hist: astropy.table.Table = None,
    ):
        if hist is not None and not isinstance(hist, astropy.table.Table):
            raise TypeError(
                "The hist must be an astropy Table")
        self._hist = hist

    @property
    def hist(self):
        return self._hist

    @hist.setter
    def hist(self, value):
        if value is not None and not isinstance(value, astropy.table.Table):
            raise TypeError(
                "The hist must be an astropy Table")
        self._hist = value

    def add_hist(self, filename):
        """Load the hist table from a CSV file.

        Parameters
        ----------
        filename : str or pathlib.Path
            Path of the history csv file.

        """
        if not os.path.isfile(filename):
            raise FileNotFoundError(f"file not found.")
        self._hist = Table.read(filename, format='csv')

    def _update_hist(self, action, **hist_keys):
        """Add a new row with information to the hist table.

        Parameters
        ----------
        faction : str
            String describing the performed action.
        **hist_keys
            Additional parameters passed to the new row of the hist table.
            Allowed arguments for columns are: FITS, Type, FROM_ROW, TO_ROW,
            and Roi_Range.

        """
        if not self._hist:
            raise ValueError(
                f"This object does not have a hist table."
            )
        # Fixed keys
        index = self._hist[-1]['Index'] + 1
        current_datetime = datetime.now()
        user = os.getlogin()
        formatted_datetime = (current_datetime.strftime(f"%Y-%m-%dT%H:%M:%S")
                            + f".{current_datetime.microsecond // 1000:03d}")
        # Define the default values for the new_row dictionary
        new_row = {
            'Index': index,
            'FITS': 'C',
            'Macro': f'//PYTHON: {action}',
            'Type': 'Py',
            'FROM_ROW': np.ma.masked,
            'TO_ROW': np.ma.masked,
            'Roi_Range': np.ma.masked,
            'User': user,
            'Date': formatted_datetime,
        }
        all_keys = list(new_row)
        provided_keys = list(hist_keys)
        protected_keys = ['Index', 'Macro', 'User', 'Date']
        # Check if any of the protected keys are in hist_keys and raise an error
        for key in provided_keys:
            if key in protected_keys:
                raise ValueError(
                    f"'{key}' is a protected key and cannot be set manually."
                )
        # Ensure only the allowed keys are in hist_keys
        allowed_keys = [item for item in all_keys if item not in protected_keys]
        invalid_keys = [item for item in provided_keys if item not in allowed_keys]
        if invalid_keys:
            raise ValueError((f"Invalid key(s) provided: {', '.join(invalid_keys)}. "
                            + f"Only {', '.join(allowed_keys)} are allowed."))
        # Update the new_row dictionary with any valid hist_keys
        new_row.update(hist_keys)
        # Add new row to history
        self._hist.add_row(new_row)

    def __repr__(self):
        # If hist is None, display that it's missing
        if self._hist is None:
            hist_repr = "None"
        # If hist is present, display a summary of the table
        else: hist_repr = (
            f"<Table length={len(self._hist)} rows, " +
            f"{len(self._hist.columns)} columns>"
        )
        return f"<MadcubaFits(hist={hist_repr})>"
