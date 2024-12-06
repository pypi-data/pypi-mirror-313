from dataclasses import dataclass
from pollination_dsl.function import Function, command, Inputs, Outputs


@dataclass
class SplitModifiers(Function):
    """Split a single sensor grid file into multiple smaller grids."""

    modifier_file = Inputs.file(
        description='Full path to a file with Radiance modifiers. The modifiers '
        'must be the identifiers of the modifiers and not the actual Radiance '
        'description of the modifiers.', path='scene.mod'
    )

    sensor_count = Inputs.int(
        description='The number of sensors in the sensor grid that will be '
        'used in rcontrib with the distributed modifiers.',
        spec={'type': 'integer', 'minimum': 1}, default=5000
    )

    grid_file = Inputs.file(
        description='Full path to a sensor grid file. This file is used to '
        'count the number of sensors and will override the sensor-count option.',
        path='grid.pts', optional=True
    )

    max_value = Inputs.int(
        description='An optional integer to define the maximum value allowed '
        'when multiplying the number of sensors with the number of modifiers '
        'in the distributed modifiers.',
        spec={'type': 'integer', 'minimum': 1}, default=40000000
    )

    sensor_multiplier = Inputs.int(
        description='An optional integer to be multiplied by the grid count to '
        'yield a final number of the sensor count. This is useful in workflows '
        'where the sensor grids are modified such as when calculating view factor',
        spec={'type': 'integer', 'minimum': 1}, default=6
    )

    @command
    def split_modifiers(self):
        return 'honeybee-radiance modifier split-modifiers scene.mod ' \
            './output_folder --sensor-count {{self.sensor_count}} ' \
            '--grid-file grid.pts --max-value {{self.max_value}} ' \
            '--sensor-multiplier {{self.sensor_multiplier}}'

    modifiers = Outputs.list(
        description='A JSON array that includes information about generated '
        'modifiers.', path='output_folder/_info.json'
    )

    modifiers_file = Outputs.file(
        description='A JSON file with information about generated modifiers.',
        path='output_folder/_info.json'
    )

    dist_info = Outputs.file(
        description='A JSON file with distribution information.',
        path='output_folder/_redist_info.json'
    )

    output_folder = Outputs.folder(
        description='Output folder with new sensor grids.', path='output_folder'
    )
