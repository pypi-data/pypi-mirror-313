from pollination.honeybee_radiance.contrib import DaylightContribution
from queenbee.plugin.function import Function


def test_daylight_contribution():
    function = DaylightContribution().queenbee
    assert function.name == 'daylight-contribution'
    assert isinstance(function, Function)
