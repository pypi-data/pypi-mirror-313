Chromophile color maps
======================

The Chromophile color maps are designed for the accurate display
of quantitative data.  This package contains the Chromophile
color maps in both `Matplotlib <https://matplotlib.org/>`_ and
`Bokeh <https://bokeh.org/>`_ formats.

Installation
------------

The Chromophile color maps are distributed as a Python package.
To install it, open a terminal and execute:

   pip install chromophile

Or, in IPython or Jupyter, use the `%pip` magic command:

   %pip install chromophile

The `chromophile` package has no required dependencies.  To use
the Chromophile color maps with Matplotlib, the `matplotlib`
package must be available at the time `chromophile` is imported.

The tools used to develop the Chromophile color maps, and the
source for the online documentation, are in a separate package
called `chromophile-dev`.  Most users will not need this package.

Usage
-----

To use the color maps, import the Chromophile package:

>>> import chromophile as cp

The Chromophile color maps are stored in two formats:

* Matplotlib `Colormap` objects are stored in `cmap`.  If
  Matplotlib is not available, `cmap` will equal `None`.  The
  color maps are also added to Matplotlib's color map registry.

* Bokeh palettes are stored in `palette`.

Individual color maps can be accessed either as dictionary items
or as attributes of these objects.  For example:

>>> cp.cmap.cp_dawn
<matplotlib.colors.ListedColormap object at ...>
>>> cp.palette['cp_peacock']
('#06003c', '#06013d', '#06023e', '#07043e', ...)

The same color map is returned regardless of how it is accessed:

>>> cp.cmap.cp_lemon_lime is cp.cmap['cp_lemon_lime']
True
>>> cp.palette.cp_blue is cp.palette['cp_blue']
True

Most IDEs should support tab completion for `cmap` and `palette`.

The available color maps can be listed using the `.keys()` method
of `cmap` or `palette` or by calling `dir()` on either of these
objects.  They are also displayed in the online documentation.
