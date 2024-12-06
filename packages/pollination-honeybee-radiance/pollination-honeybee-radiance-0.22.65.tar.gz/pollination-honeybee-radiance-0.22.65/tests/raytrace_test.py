from pollination.honeybee_radiance.raytrace import RayTracingDaylightFactor, \
    RayTracingPointInTime, RayTracingSkyView
from queenbee.plugin.function import Function


def test_ray_tracing_daylight_factor():
    function = RayTracingDaylightFactor().queenbee
    assert function.name == 'ray-tracing-daylight-factor'
    assert isinstance(function, Function)


def test_ray_tracing_point_in_time():
    function = RayTracingPointInTime().queenbee
    assert function.name == 'ray-tracing-point-in-time'
    assert isinstance(function, Function)


def test_ray_tracing_sky_view():
    function = RayTracingSkyView().queenbee
    assert function.name == 'ray-tracing-sky-view'
    assert isinstance(function, Function)
