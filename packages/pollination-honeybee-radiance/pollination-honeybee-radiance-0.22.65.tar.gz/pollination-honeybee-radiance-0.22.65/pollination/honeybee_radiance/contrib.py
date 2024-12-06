from dataclasses import dataclass
from pollination_dsl.function import Function, command, Inputs, Outputs


@dataclass
class DaylightContribution(Function):
    """
    Calculate daylight contribution for a grid of sensors from a series of modifiers
    using rcontrib command.
    """

    radiance_parameters = Inputs.str(
        description='Radiance parameters. -I and -aa 0 are already included in '
        'the command.', default=''
    )

    fixed_radiance_parameters = Inputs.str(
        description='Radiance parameters. -I and -aa 0 are already included in '
        'the command.', default='-aa 0'
    )

    calculate_values = Inputs.str(
        description='A switch to indicate if the values should be multiplied. '
        'Otherwise the contribution is calculated as a coefficient. Default is set to '
        'value. Use coeff for contribution', default='value',
        spec={'type': 'string', 'enum': ['value', 'coeff']}
    )

    conversion = Inputs.str(
        description='Conversion values as a string which will be passed to rmtxop -c.',
        default=''
    )

    order_by = Inputs.str(
        description='An option to change how results are grouped in each row. By '
        'default each row are the results for each sensor during all the datetimes. '
        'Valid options are sensor and datetime.',
        default='sensor', spec={'type': 'string', 'enum': ['sensor', 'datetime']}
    )

    header = Inputs.str(
        default='keep',
        description='An input to indicate if header should be kept or removed from the'
        'output matrix.', spec={'type': 'string', 'enum': ['keep', 'remove']}
    )

    output_format = Inputs.str(
        description='Output format for converted results. Valid inputs are a, f and '
        'd for ASCII, float or double. If conversion is not provided you can change the '
        'output format using rad-params options.', default='a',
        spec={'type': 'string', 'enum': ['a', 'd', 'f']}
    )

    sensor_count = Inputs.int(
        description='Number of maximum sensors in each generated grid.',
        spec={'type': 'integer', 'minimum': 1}
    )

    modifiers = Inputs.file(
        description='Path to modifiers file. In most cases modifiers are sun modifiers.',
        path='suns.mod'
    )

    sensor_grid = Inputs.file(
        description='Path to sensor grid files.', path='grid.pts',
        extensions=['pts']
    )

    scene_file = Inputs.file(
        description='Path to an octree file to describe the scene.', path='scene.oct',
        extensions=['oct']
    )

    bsdf_folder = Inputs.folder(
        description='Folder containing any BSDF files needed for ray tracing.',
        path='model/bsdf', optional=True
    )

    @command
    def run_daylight_coeff(self):
        return 'honeybee-radiance dc scontrib scene.oct grid.pts suns.mod ' \
            '--{{self.calculate_values}} --sensor-count {{self.sensor_count}} ' \
            '--rad-params "{{self.radiance_parameters}}" --rad-params-locked ' \
            '"{{self.fixed_radiance_parameters}}" --conversion "{{self.conversion}}" ' \
            '--output-format {{self.output_format}} --output results.ill ' \
            '--order-by-{{self.order_by}} --{{self.header}}-header'

    result_file = Outputs.file(description='Output result file.', path='results.ill')
