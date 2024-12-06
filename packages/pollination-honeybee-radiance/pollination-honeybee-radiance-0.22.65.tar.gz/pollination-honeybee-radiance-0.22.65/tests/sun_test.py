from pollination.honeybee_radiance.sun import CreateSunMatrix, ParseSunUpHours

from queenbee.plugin.function import Function


def test_parse_sun_up_hours():
    function = ParseSunUpHours().queenbee
    assert function.name == 'parse-sun-up-hours'
    assert isinstance(function, Function)


def test_create_sun_matrix():
    function = CreateSunMatrix().queenbee
    assert function.name == 'create-sun-matrix'
    assert isinstance(function, Function)
