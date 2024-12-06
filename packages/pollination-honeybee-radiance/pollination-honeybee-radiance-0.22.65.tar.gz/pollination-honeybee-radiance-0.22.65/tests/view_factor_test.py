from pollination.honeybee_radiance.viewfactor import ViewFactorModifiers, \
    SphericalViewFactorContribution
from queenbee.plugin.function import Function


def test_view_factor_modifiers():
    function = ViewFactorModifiers().queenbee
    assert function.name == 'view-factor-modifiers'
    assert isinstance(function, Function)


def test_spherical_view_factor_contribution():
    function = SphericalViewFactorContribution().queenbee
    assert function.name == 'spherical-view-factor-contribution'
    assert isinstance(function, Function)
