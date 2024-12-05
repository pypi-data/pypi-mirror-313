from astropy.nddata import CCDData
from astropy.stats import sigma_clipped_stats
from madcubapy.io import MadcubaMap
import matplotlib as mpl
import matplotlib.axes as maxes
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable


def add_wcs_axes(
        fig=None,
        nrows=1,
        ncols=1,
        number=1,
        fitsmap=None,
        use_std=False,
        **kwargs):
    """Add an axes object with WCS coordinates into an existing figure.

    A figure with no axes has to be set before calling this function.
    This is due to the inability to change axis coordinates after it has been
    called. The coordinates have to be called when creating the axes object.
    The function returns objects for the axes and the image.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        Figure object.
    nrows : int
        Number of rows on the subplot grid.
    ncols : int
        Number of columns on the subplot grid.
    number : int
        Number of subplot in the grid in which to paint the axes.
    fitsmap : madcubapy.io.MadcubaMap or astropy.nddata.CCDData
        Map to be displayed.
    use_std : boolean
        If true, set color limits to +- three times the standard
        deviation of the image data.

    Return
    ------
    ax : astropy.visualization.wcsaxes.WCSAxesSubplot
        Axes object with the selected map coordinates.
    img : matplotlib.image.AxesImage
        Image object of the selected map.

    Other Parameters
    ----------------
    **kwargs
        Parameters to pass to the matplotlib.pyplot.imshow() function.

    """
    
    if not fig:
        raise TypeError(
            "add_wcs_axes() missing 1 required positional argument: 'fig'"
        )
    elif not isinstance(fig, mpl.figure.Figure):
        raise TypeError(
            f"'fig' argument must be a {mpl.figure.Figure}"
        )
    if fitsmap == None:
        raise TypeError(
            f"Need to specify a fitsmap parameter.")
    elif (not isinstance(fitsmap, MadcubaMap) and
          not isinstance(fitsmap, CCDData)):
        raise TypeError(
            f"'fitsmap' argument must be a {MadcubaMap} or {CCDData}")
    if fitsmap.wcs is None:
        raise TypeError(
            f"This fits file has problems in its WCS parameters.")

    data = fitsmap.data
    wcs = fitsmap.wcs.celestial
    # store BUNIT in a global variable
    global last_bunit
    last_bunit = parse_clabel(fitsmap)

    # Slice extra dimensions from data
    if fitsmap.header['NAXIS'] == 3:
        data = data[0, :, :]
    elif fitsmap.header['NAXIS'] == 4:
        data = data[0, 0, :, :]
    # Dimensions are: stokes, freq, Y, X for ALMA datacubes

    if use_std:
        mean, median, std= sigma_clipped_stats(data, sigma=3.0)
        kwargs['vmin'] = median - 3 * std
        kwargs['vmax'] = median + 3 * std

    # Create the WCS axes
    ax = fig.add_subplot(nrows, ncols, number, projection=wcs)
    img = ax.imshow(data, **kwargs)
    ax.coords[0].set_axislabel("RA (ICRS)")
    ax.coords[1].set_axislabel("DEC (ICRS)")
    # Vertical ticklabel for DEC
    ax.coords[1].set_ticklabel(rotation='vertical', rotation_mode='default')

    return ax, img


def add_manual_wcs_axes(
        fig=None,
        left=0, 
        bottom=0, 
        width=1, 
        height=1,
        fitsmap=None,
        use_std=False,
        **kwargs):
    """Add an axes object with WCS coordinates in a manually set position into
    an existing figure.

    A figure with no axes has to be set before calling this function.
    This is due to the inability to change axis coordinates after it has been
    called. The coordinates have to be called when creating the axes object.
    The function returns objects for the axes and the image.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        Figure object.
    left : float
        X coordinate to begin the axes subplot.
    bottom : float
        Y coordinate to begin the axes subplot.
    width : float
        Width of the axes subplot.
    height : float
        Height of the axes subplot.
    fitsmap : madcubapy.io.MadcubaMap or astropy.nddata.CCDData
        Map to be displayed.
    use_std : boolean
        If true, set color limits to +- three times the standard
        deviation of the image data.

    Return
    ------
    ax : astropy.visualization.wcsaxes.WCSAxesSubplot
        Axes object with the selected map coordinates.
    img : matplotlib.image.AxesImage
        Image object of the selected map.

    Other Parameters
    ----------------
    **kwargs
        Parameters to pass to the matplotlib.pyplot.imshow() function.

    """
    
    if not fig:
        raise TypeError(
            "add_manual_wcs_axes() missing 1 required positional argument: 'fig'"
        )
    elif not isinstance(fig, mpl.figure.Figure):
        raise TypeError(
            f"'fig' argument must be a {mpl.figure.Figure}"
        )
    if fitsmap == None:
        raise TypeError(
            f"Need to specify a fitsmap parameter.")
    elif (not isinstance(fitsmap, MadcubaMap) and
          not isinstance(fitsmap, CCDData)):
        raise TypeError(
            f"'fitsmap' argument must be a {MadcubaMap} or {CCDData}")
    if fitsmap.wcs is None:
        raise TypeError(
            f"This fits file has problems in its WCS parameters.")
    
    data = fitsmap.data
    wcs = fitsmap.wcs.celestial
    # store BUNIT in a global variable
    global last_bunit
    last_bunit = parse_clabel(fitsmap)

    # Slice extra dimensions from data
    if fitsmap.header['NAXIS'] == 3:
        data = data[0, :, :]
    elif fitsmap.header['NAXIS'] == 4:
        data = data[0, 0, :, :]
    # Dimensions are: stokes, freq, Y, X for ALMA datacubes

    if use_std:
        mean, median, std= sigma_clipped_stats(data, sigma=3.0)
        kwargs['vmin'] = median - 3 * std
        kwargs['vmax'] = median + 3 * std

    # Create the WCS axes
    ax = fig.add_axes([left, bottom, width, height], projection=wcs)
    img = ax.imshow(data, **kwargs)
    ax.coords[0].set_axislabel("RA (ICRS)")
    ax.coords[1].set_axislabel("DEC (ICRS)")
    # Vertical ticklabel for DEC
    ax.coords[1].set_ticklabel(rotation='vertical', rotation_mode='default')

    return ax, img


def parse_clabel(fitsmap):
    """Parse colorbar text from a MadcubaMap or CCDData unit attribute.

    Parameters
    ----------
    fitsmap : madcubapy.io.MadcubaMap or astropy.nddata.CCDData
        MadcubaMap or CCDData object to extract units information.

    Return
    ------
    label : str
        Label to be used in the colorbar.

    """

    units = fitsmap.unit.to_string()
    if units == 'Jy / beam':
        label = r'$I \ {\rm (Jy \ beam^{-1})}$'
    elif units == 'Jy m / (beam s)':
        label = r'$I \ {\rm (Jy \ beam^{-1} \ m \ s^{-1})}$'
    elif units == 'km mJy / (beam s)':
        label = r'$I \ {\rm (mJy \ beam^{-1} \ km \ s^{-1})}$'
    elif units == 'Jy km / (beam s)':
        label = r'$I \ {\rm (Jy \ beam^{-1} \ km \ s^{-1})}$'
    elif units == 'm mJy / (beam s)':
        label = r'$I \ {\rm (mJy \ beam^{-1} \ m \ s^{-1})}$'
    else:
        label = 'units not parsed'

    return label


def append_colorbar(
        ax=None,
        location='right',
        width='5%',
        pad=0.05,
        **kwargs):
    """Append a colorbar to an axes, fitting it into the same space.

    Parameters
    ----------
    ax : astropy.visualization.wcsaxes.WCSAxes
        Axes object in which to add the colorbar.
    location : str
        Set the location of cbar: 'top', 'right', 'bottom', or 'left'.
    width : str
        Set percentage of axes box to use as width for cbar.
    pad : float
        Set the separation between the colorbar bar and the axes.

    Return
    ------
    cbar : matplotlib.colorbar.Colorbar
        Colorbar object.

    Other Parameters
    ----------------
    **kwargs
        Parameters to pass to the matplotlib.Figure.colorbar() function.

    """

    if ax == None:
        raise TypeError(
            f"Need to specify an axes object with 'ax' keyword.")

    # Get figure and image objects from the axes
    fig = ax.get_figure()
    img = ax.get_images()[0]

    # Add colorbar
    if location == 'left' or location == 'right':
        orientation = 'vertical'
    elif location == 'top' or location == 'bottom':
        orientation = 'horizontal'
    else:
        raise ValueError(
            f"location can only be 'top', 'right', 'bottom', or 'left'")
    # Use bunit from last fitsmap plotted if present
    if 'label' not in kwargs:
        try:
            last_bunit
        except NameError:
            kwargs['label'] = 'units not found'
        else:
            kwargs['label'] = last_bunit
    divider = make_axes_locatable(ax)
    cax = divider.append_axes(location, size=width, 
                                pad=pad, axes_class=maxes.Axes)
    if location == 'right':
        colorbar = fig.colorbar(img, cax=cax,
                                orientation='vertical', **kwargs)
        colorbar.ax.tick_params(
            axis="y",
            which="both",
            left=False,
            right=True,
            labelleft=False,
            labelright=True,
        )
        colorbar.ax.yaxis.set_label_position('right')
        ax.coords[1].tick_params(
            axis="y",
            which="both",
            labelleft=True,
            labelright=False,
        )
        ax.coords[1].set_axislabel_position('l')
    elif location == 'left':
        colorbar = fig.colorbar(img, cax=cax,
                                orientation='vertical', **kwargs)
        colorbar.ax.tick_params(
            axis="y",
            which="both",
            left=True,
            right=False,
            labelleft=True,
            labelright=False,
        )
        colorbar.ax.yaxis.set_label_position('left')
        ax.coords[1].tick_params(
            axis="y",
            which="both",
            labelleft=False,
            labelright=True,
        )
        ax.coords[1].set_axislabel_position('r')
    elif location == 'top':
        colorbar = fig.colorbar(img, cax=cax,
                                orientation='horizontal', **kwargs)
        colorbar.ax.tick_params(
            axis="x",
            which="both",
            top=True,
            bottom=False,
            labeltop=True,
            labelbottom=False,
        )
        colorbar.ax.xaxis.set_label_position('top')
        ax.coords[0].tick_params(
            axis="x",
            which="both",
            labeltop=False,
            labelbottom=True,
        )
        ax.coords[0].set_axislabel_position('b')
    elif location == 'bottom':
        colorbar = fig.colorbar(img, cax=cax,
                                orientation='horizontal', **kwargs)
        colorbar.ax.tick_params(
            axis="x",
            which="both",
            top=False,
            bottom=True,
            labeltop=False,
            labelbottom=True,
        )
        colorbar.ax.xaxis.set_label_position('bottom')
        ax.coords[0].tick_params(
            axis="x",
            which="both",
            labeltop=True,
            labelbottom=False
        )
        ax.coords[0].set_axislabel_position('t')
    # colorbar.ax.set_ylabel(ylabel=cbar_label, fontsize=12)  # default 10
    # colorbar.ax.tick_params(labelsize=11)  # default 10

    return colorbar


def add_colorbar(
        ax=None,
        location='right',
        width=0.05,
        pad=0.03,
        **kwargs):
    """Add a colorbar to the side of an axes.

    Parameters
    ----------
    ax : astropy.visualization.wcsaxes.WCSAxes
        Axes object in which to add the colorbar.
    location : str
        Set the location of cbar: 'top', 'right', 'bottom', or 'left'.
    width : float
        Set percentage of axes box to use as width for cbar.
    pad : float
        Set the separation between the colorbar bar and the axes.

    Return
    ------
    cbar : matplotlib.colorbar.Colorbar
        Colorbar object.

    Other Parameters
    ----------------
    **kwargs
        Parameters to pass to the matplotlib.Figure.colorbar() function.

    """

    if ax == None:
        raise TypeError(
            f"Need to specify an axes object with 'ax' keyword.")

    # Get figure and image objects from the axes
    fig = ax.get_figure()
    img = ax.get_images()[0]

    # Add colorbar
    if location == 'left' or location == 'right':
        orientation = 'vertical'
    elif location == 'top' or location == 'bottom':
        orientation = 'horizontal'
    else:
        raise ValueError(
            f"location can only be 'top', 'right', 'bottom', or 'left'")
    # Use bunit from last fitsmap plotted if present
    if 'label' not in kwargs:
        try:
            last_bunit
        except NameError:
            kwargs['label'] = 'units not found'
        else:
            kwargs['label'] = last_bunit
    ax_xini, ax_yini, ax_width, ax_height = ax.get_position(
        original=False).bounds

    if location == 'right':
        cax = fig.add_axes([ax_xini+ax_width+pad*(ax_width),
                            ax_yini,
                            width*ax_width,
                            ax_height])
        colorbar = fig.colorbar(img, cax=cax,
                                orientation='vertical', **kwargs)
        colorbar.ax.tick_params(
            axis="y",
            which="both",
            left=False,
            right=True,
            labelleft=False,
            labelright=True,
        )
        colorbar.ax.yaxis.set_label_position('right')
        ax.coords[1].tick_params(
            axis="y",
            which="both",
            labelleft=True,
            labelright=False,
        )
        ax.coords[1].set_axislabel_position('l')
    elif location == 'left':
        cax = fig.add_axes([ax_xini-pad*(ax_width)-width*(ax_width),
                            ax_yini,
                            width*ax_width,
                            ax_height])
        colorbar = fig.colorbar(img, cax=cax,
                                orientation='vertical', **kwargs)
        colorbar.ax.tick_params(
            axis="y",
            which="both",
            left=True,
            right=False,
            labelleft=True,
            labelright=False,
        )
        colorbar.ax.yaxis.set_label_position('left')
        ax.coords[1].tick_params(
            axis="y",
            which="both",
            labelleft=False,
            labelright=True,
        )
        ax.coords[1].set_axislabel_position('r')
    elif location == 'top':
        cax = fig.add_axes([ax_xini,
                            ax_yini+ax_height+pad*(ax_height),
                            ax_width,
                            width*ax_height])
        colorbar = fig.colorbar(img, cax=cax,
                                orientation='horizontal', **kwargs)
        colorbar.ax.tick_params(
            axis="x",
            which="both",
            top=True,
            bottom=False,
            labeltop=True,
            labelbottom=False,
        )
        colorbar.ax.xaxis.set_label_position('top')
        ax.coords[0].tick_params(
            axis="x",
            which="both",
            labeltop=False,
            labelbottom=True,
        )
        ax.coords[0].set_axislabel_position('b')
    elif location == 'bottom':
        cax = fig.add_axes([ax_xini,
                            ax_yini-pad*(ax_height)-width*(ax_height),
                            ax_width,
                            width*ax_height])
        colorbar = fig.colorbar(img, cax=cax,
                                orientation='horizontal', **kwargs)
        colorbar.ax.tick_params(
            axis="x",
            which="both",
            top=False,
            bottom=True,
            labeltop=False,
            labelbottom=True,
        )
        colorbar.ax.xaxis.set_label_position('bottom')
        ax.coords[0].tick_params(
            axis="x",
            which="both",
            labeltop=True,
            labelbottom=False
        )
        ax.coords[0].set_axislabel_position('t')
    # colorbar.ax.set_ylabel(ylabel=cbar_label, fontsize=12)  # default 10
    # colorbar.ax.tick_params(labelsize=11)  # default 10

    return colorbar