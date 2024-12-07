# Chromophile Python module
#
# Written in 2022 by Kyle Hofmann
#
# To the extent possible under law, the author(s) have dedicated
# all copyright and related and neighboring rights to this
# software to the public domain worldwide. This software is
# distributed without any warranty.
#
# You should have received a copy of the CC0 Public Domain
# Dedication along with this software. If not, see
# <http://creativecommons.org/publicdomain/zero/1.0/>.

"""
Chromophile color maps
======================

The Chromophile color maps are designed for the accurate display
of quantitative data.  This package contains the Chromophile
color maps in both `Matplotlib <https://matplotlib.org/>`_ and
`Bokeh <https://bokeh.org/>`_ formats.

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
"""

import importlib.resources
import itertools


__version__ = '1.0.7'
__all__ = ('cmap', 'palette')

_INDEX = (
    ('cp_cyc_isolum_dark', 360),
    ('cp_cyc_isolum_light', 360),
    ('cp_cyc_isolum_wide', 360),
    ('cp_cyc_red_cyan_valley', 360),
    ('cp_div_blue_orange_valley', 512),
    ('cp_div_green_blue_hill', 512),
    ('cp_div_green_cyan_valley', 512),
    ('cp_div_orange_blue_hill', 512),
    ('cp_div_pink_orange_valley', 512),
    ('cp_isolum_purple_orange_dark', 256),
    ('cp_isolum_purple_orange_light', 256),
    ('cp_isolum_purple_orange_wide', 256),
    ('cp_isolum_yellow_blue_dark', 256),
    ('cp_isolum_yellow_blue_light', 256),
    ('cp_isolum_yellow_blue_wide', 256),
    ('cp_mseq_green_blue', 512),
    ('cp_mseq_green_purple', 512),
    ('cp_mseq_green_red', 512),
    ('cp_mseq_orange_blue', 512),
    ('cp_mseq_orange_blue_purple', 768),
    ('cp_mseq_orange_green_blue', 768),
    ('cp_mseq_orange_green_blue_purple', 1024),
    ('cp_mseq_orange_teal', 512),
    ('cp_mseq_purple_orange', 512),
    ('cp_mseq_red_blue', 512),
    ('cp_mseq_teal_purple', 512),
    ('cp_seq_blue_cyan_ccw', 256),
    ('cp_seq_blue_cyan_cw', 256),
    ('cp_seq_blue_pink_ccw1', 256),
    ('cp_seq_blue_pink_ccw2', 256),
    ('cp_seq_blue_yellow_ccw', 256),
    ('cp_seq_blue_yellow_cw', 256),
    ('cp_seq_gray', 256),
    ('cp_seq_green_cyan_ccw', 256),
    ('cp_seq_green_green_cw', 256),
    ('cp_seq_green_yellow_cw', 256),
    ('cp_seq_red_cyan_ccw', 256),
    ('cp_seq_red_cyan_cw', 256),
    ('cp_seq_red_pink_cw1', 256),
    ('cp_seq_red_pink_cw2', 256),
    ('cp_seq_red_yellow_ccw', 256),
    ('cp_seq_red_yellow_cw', 256),
    )

_ALIASES = (
    ('cp_isolum_cyc_dark', 'cp_cyc_isolum_dark'),
    ('cp_isolum_cyc_light', 'cp_cyc_isolum_light'),
    ('cp_isolum_cyc_wide', 'cp_cyc_isolum_wide'),
    ('cp_blue', 'cp_seq_blue_cyan_cw'),
    ('cp_purple', 'cp_seq_blue_pink_ccw1'),
    ('cp_dawn', 'cp_seq_blue_yellow_ccw'),
    ('cp_peacock', 'cp_seq_blue_yellow_cw'),
    ('cp_gray', 'cp_seq_gray'),
    ('cp_grey', 'cp_seq_gray'),
    ('cp_seq_grey', 'cp_seq_gray'),
    ('cp_teal', 'cp_seq_green_cyan_ccw'),
    ('cp_green', 'cp_seq_green_green_cw'),
    ('cp_lemon_lime', 'cp_seq_green_yellow_cw'),
    ('cp_red', 'cp_seq_red_pink_cw1'),
    ('cp_orange', 'cp_seq_red_yellow_ccw'),
    )


class _attrdict(dict):
    """Redirect attribute access to item lookup"""

    def __dir__(self):
        return self.keys()

    def __getattr__(self, k):
        if k.startswith('_'):
            return super().__getattr__(k)
        try:
            return self[k]
        except KeyError:
            raise AttributeError(f"No color map named {k!r}") from None

    def __setattr__(self, k, v):
        if k.startswith('_'):
            super().__setattr__(k, v)
        else:
            self[k] = v


def _expand_aliases(aliases):
    new_aliases = []
    for alias, name in aliases:
        new_aliases.append((alias + "_r", name + "_r"))
    return new_aliases


def _init_cmaps(index):
    pkg_traversable = importlib.resources.files(__package__)
    cmaps_file = pkg_traversable / '_cmaps.dat'
    with open(cmaps_file, 'rb') as fp:
        data = fp.read()

    if len(data) % 3 != 0:
        raise ImportError(
            "Corrupt color maps file with length not a multiple of 3"
            )

    all_cmap_data = memoryview(data).cast('B', (len(data) // 3, 3)).tolist()

    idx = 0
    parsed_cmap_data = []
    for name, length in index:
        parsed_cmap_data.append((name, all_cmap_data[idx:idx + length]))
        idx += length
        if idx > len(all_cmap_data):
            missing_cols = idx - len(all_cmap_data)
            raise ImportError(
                "Corrupt color maps file with"
                f" {missing_cols} colors missing from {name}"
                )

    if idx != len(all_cmap_data):
        extra_cols = len(all_cmap_data) - idx
        raise ImportError(
            f"Corrupt color maps file with {extra_cols} extra colors"
            )

    return parsed_cmap_data


def _make_rearrangements(name, data):
    yield (name, data)

    if name.startswith("cp_seq_"):
        yield (name + "_r", data[::-1])
    elif name.startswith("cp_mseq_"):
        _, _, *colors = name.split('_')

        num_colors = len(colors)
        seq_len = len(data) // num_colors
        data_r = []
        for i in range(num_colors):
            data_r.extend(data[i * seq_len:(i + 1) * seq_len][::-1])
        yield (name + "_r", data_r)

        if num_colors == 2:
            yield (
                f"{name}_hill",
                [*data[:seq_len], *data_r[seq_len:]],
                )
            yield (
                f"{name}_valley",
                [*data_r[:seq_len], *data[seq_len:]],
                )
            yield (
                f"cp_mseq_{colors[1]}_{colors[0]}",
                [*data[seq_len:], *data[:seq_len]],
                )
            yield (
                f"cp_mseq_{colors[1]}_{colors[0]}_r",
                [*data_r[seq_len:], *data_r[:seq_len]],
                )
            yield (
                f"cp_mseq_{colors[1]}_{colors[0]}_hill",
                [*data[seq_len:], *data_r[:seq_len]],
                )
            yield (
                f"cp_mseq_{colors[1]}_{colors[0]}_valley",
                [*data_r[seq_len:], *data[:seq_len]]
                )
    elif name.startswith("cp_div_"):
        _, _, color0, color1, div_type = name.split('_')
        yield (f"cp_div_{color1}_{color0}_{div_type}", data[::-1])
    elif name.startswith("cp_cyc_"):
        yield (name + "_r", data[::-1])

        _, _, *all_colors, cyc_type = name.split('_')
        if cyc_type == 'valley':
            yield (
                f"cp_cyc_{'_'.join(all_colors)}_hill",
                [*data[len(data) // 2:], *data[:len(data) // 2]]
                )
            yield (
                f"cp_cyc_{'_'.join(all_colors)}_hill_r",
                [*data[:len(data) // 2][::-1], *data[len(data) // 2:][::-1]]
                )


def _init_mpl(cmaps):
    import numpy as np
    from matplotlib.colors import ListedColormap

    mpl_ver = (*map(int, matplotlib.__version__.split('.')),)
    if mpl_ver >= (3, 6, 0):
        register = matplotlib.colormaps.register
    else:
        from matplotlib.cm import register_cmap as register

    cmap = _attrdict()
    for name, data in cmaps:
        mpl_colors = np.array(data, dtype=np.float64)
        mpl_colors /= 255.
        mpl_colors += 1./(2.*255.)
        np.clip(mpl_colors, 0.0, 1.0, out=mpl_colors)
        mpl_colors.setflags(write=False)

        mpl_cmap = ListedColormap(mpl_colors, name=name)
        register(cmap=mpl_cmap, name=name)
        cmap[name] = mpl_cmap

    for alias, name in _expanded_aliases:
        aliased_cmap = ListedColormap(cmap[name].colors, name=alias)
        register(cmap=aliased_cmap, name=alias)
        cmap[alias] = aliased_cmap

    return cmap


def _init_bokeh(cmaps):
    palette = _attrdict()
    for name, data in cmaps:
        palette[name] = (
            *itertools.starmap("#{0:02x}{1:02x}{2:02x}".format, data),
            )

    for alias, name in _expanded_aliases:
        palette[alias] = palette[name]
    return palette


_parsed_cmap_data = _init_cmaps(_INDEX)
_cmaps = (*itertools.chain.from_iterable(
    itertools.starmap(_make_rearrangements, _parsed_cmap_data)
    ),)
_expanded_aliases = (*_ALIASES, *_expand_aliases(_ALIASES))

palette = _init_bokeh(_cmaps)
palette.__doc__ = """Chromophile color maps stored as Bokeh palettes

Color maps can be accessed as dictionary items or attributes."""

try:
    import matplotlib
except ImportError:
    cmap = None
else:
    cmap = _init_mpl(_cmaps)
    cmap.__doc__ = (
        """Chromophile color maps stored as Matplotlib color map objects

Color maps can be accessed as dictionary items or attributes."""
        )

    del matplotlib

del itertools
del importlib
