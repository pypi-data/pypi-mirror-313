import chromophile as cp

import pytest


_CMAPS = (
    'cp_cyc_isolum_dark',
    'cp_cyc_isolum_light',
    'cp_cyc_isolum_wide',
    'cp_cyc_red_cyan_valley',
    'cp_div_blue_orange_valley',
    'cp_div_green_blue_hill',
    'cp_div_green_cyan_valley',
    'cp_div_orange_blue_hill',
    'cp_div_pink_orange_valley',
    'cp_isolum_purple_orange_dark',
    'cp_isolum_purple_orange_light',
    'cp_isolum_purple_orange_wide',
    'cp_isolum_yellow_blue_dark',
    'cp_isolum_yellow_blue_light',
    'cp_isolum_yellow_blue_wide',
    'cp_mseq_green_blue',
    'cp_mseq_green_purple',
    'cp_mseq_green_red',
    'cp_mseq_orange_blue',
    'cp_mseq_orange_blue_purple',
    'cp_mseq_orange_green_blue',
    'cp_mseq_orange_green_blue_purple',
    'cp_mseq_orange_teal',
    'cp_mseq_purple_orange',
    'cp_mseq_red_blue',
    'cp_mseq_teal_purple',
    'cp_seq_blue_cyan_ccw',
    'cp_seq_blue_cyan_cw',
    'cp_seq_blue_pink_ccw1',
    'cp_seq_blue_pink_ccw2',
    'cp_seq_blue_yellow_ccw',
    'cp_seq_blue_yellow_cw',
    'cp_seq_gray',
    'cp_seq_green_cyan_ccw',
    'cp_seq_green_green_cw',
    'cp_seq_green_yellow_cw',
    'cp_seq_red_cyan_ccw',
    'cp_seq_red_cyan_cw',
    'cp_seq_red_pink_cw1',
    'cp_seq_red_pink_cw2',
    'cp_seq_red_yellow_ccw',
    'cp_seq_red_yellow_cw',
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


def test_version():
    assert cp.__version__ == '1.0.7'


def test_palette_cmap_name_consistency():
    _ = pytest.importorskip("matplotlib")
    for name in cp.palette.keys():
        assert name in cp.cmap.keys()
    for name in cp.cmap.keys():
        assert name in cp.palette.keys()


def key_attr_consistency(map_obj):
    for name in map_obj.keys():
        assert name in dir(map_obj)
    for name in dir(map_obj):
        assert name in map_obj.keys()
    for name, val in map_obj.items():
        assert val is getattr(map_obj, name)


def test_key_attr_consistency_bokeh():
    key_attr_consistency(cp.palette)


def test_key_attr_consistency_matplotlib():
    _ = pytest.importorskip("matplotlib")
    key_attr_consistency(cp.cmap)


def test_base_cmaps():
    _ = pytest.importorskip("matplotlib")
    for name in _CMAPS:
        assert name in cp.cmap.keys()
        assert cp.cmap[name].name == name


def test_base_palettes():
    for name in _CMAPS:
        assert name in cp.palette.keys()


def test_cmap_aliases():
    _ = pytest.importorskip("matplotlib")
    for alias, name in _ALIASES:
        assert alias in cp.cmap.keys()
        assert cp.cmap[alias].name == alias
        assert (cp.cmap[name].colors == cp.cmap[alias].colors).all()


def test_palette_aliases():
    for alias, name in _ALIASES:
        assert alias in cp.palette.keys()
        assert cp.palette[alias] == cp.palette[name]
