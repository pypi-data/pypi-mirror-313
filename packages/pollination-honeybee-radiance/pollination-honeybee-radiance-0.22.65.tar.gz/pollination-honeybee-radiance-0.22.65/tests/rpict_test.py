from pollination.honeybee_radiance.rpict import RayTracingPicture
from queenbee.plugin.function import Function


def test_ray_tracing_picture():
    function = RayTracingPicture().queenbee
    assert function.name == 'ray-tracing-picture'
    assert isinstance(function, Function)
