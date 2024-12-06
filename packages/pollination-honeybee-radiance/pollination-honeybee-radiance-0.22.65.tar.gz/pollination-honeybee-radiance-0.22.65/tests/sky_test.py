from pollination.honeybee_radiance.sky import AddRemoveSkyMatrix, \
    GenSky, GenSkyWithCertainIllum, CreateSkyDome, CreateSkyMatrix, \
    AdjustSkyForMetric, CreateLeedSkies, AbntNbr15575Skies

from queenbee.plugin.function import Function


def test_add_remove_sky_matrix():
    function = AddRemoveSkyMatrix().queenbee
    assert function.name == 'add-remove-sky-matrix'
    assert isinstance(function, Function)


def test_gen_sky():
    function = GenSky().queenbee
    assert function.name == 'gen-sky'
    assert isinstance(function, Function)


def test_gen_sky_with_certain_illum():
    function = GenSkyWithCertainIllum().queenbee
    assert function.name == 'gen-sky-with-certain-illum'
    assert isinstance(function, Function)


def test_create_sky_dome():
    function = CreateSkyDome().queenbee
    assert function.name == 'create-sky-dome'
    assert isinstance(function, Function)


def test_create_sky_matrix():
    function = CreateSkyMatrix().queenbee
    assert function.name == 'create-sky-matrix'
    assert isinstance(function, Function)


def test_adjust_sky_for_metric():
    function = AdjustSkyForMetric().queenbee
    assert function.name == 'adjust-sky-for-metric'
    assert isinstance(function, Function)


def test_create_leed_skies():
    function = CreateLeedSkies().queenbee
    assert function.name == 'create-leed-skies'
    assert isinstance(function, Function)


def test_abnt_nbr_15575_skies():
    function = AbntNbr15575Skies().queenbee
    assert function.name == 'abnt-nbr15575-skies'
    assert isinstance(function, Function)
