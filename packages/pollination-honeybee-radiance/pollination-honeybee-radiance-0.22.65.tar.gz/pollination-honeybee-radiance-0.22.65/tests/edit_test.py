from pollination.honeybee_radiance.edit import MirrorModelSensorGrids

from queenbee.plugin.function import Function


def test_mirror_model_sensor_grids():
    function = MirrorModelSensorGrids().queenbee
    assert function.name == 'mirror-model-sensor-grids'
    assert isinstance(function, Function)
