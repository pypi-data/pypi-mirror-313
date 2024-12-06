from pollination.honeybee_radiance.coefficient import DaylightCoefficient, \
    DaylightCoefficientNoSkyMatrix
from queenbee.plugin.function import Function


def test_daylight_coefficient():
    function = DaylightCoefficient().queenbee
    assert function.name == 'daylight-coefficient'
    assert isinstance(function, Function)


def test_daylight_no_sky_matrix_coefficient():
    function = DaylightCoefficientNoSkyMatrix().queenbee
    assert function.name == 'daylight-coefficient-no-sky-matrix'
    assert isinstance(function, Function)
