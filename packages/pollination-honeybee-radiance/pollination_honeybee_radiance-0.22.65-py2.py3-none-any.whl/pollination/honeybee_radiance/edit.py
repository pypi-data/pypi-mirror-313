from dataclasses import dataclass
from pollination_dsl.function import Inputs, Outputs, Function, command


@dataclass
class MirrorModelSensorGrids(Function):
    """Mirror a honeybee Model's SensorGrids and format them for thermal mapping.

    This involves setting the direction of every sensor to point up (0, 0, 1) and
    then adding a mirrored sensor grid with the same sensor positions that all
    point downward. In thermal mapping workflows, the upward-pointing grids are
    used to account for direct and diffuse shortwave irradiance while the
    downward pointing grids account for ground-reflected shortwave irradiance.
    """

    model = Inputs.file(
        description='Honeybee model in JSON format.', path='model.hbjson',
        extensions=['hbjson', 'json']
    )

    @command
    def mirror_sensor_grids(self):
        return 'honeybee-radiance edit mirror-model-sensors model.hbjson ' \
            '--output-file new_model.hbjson'

    new_model = Outputs.file(
        description='Model JSON with its sensor grids mirrored.', path='new_model.hbjson'
    )
