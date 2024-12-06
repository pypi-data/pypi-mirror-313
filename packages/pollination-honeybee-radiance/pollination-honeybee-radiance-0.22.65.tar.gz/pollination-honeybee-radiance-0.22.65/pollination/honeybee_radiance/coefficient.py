from dataclasses import dataclass
from pollination_dsl.function import Function, command, Inputs, Outputs


@dataclass
class DaylightCoefficient(Function):
    """Calculate daylight coefficient for a grid of sensors from a sky matrix."""

    radiance_parameters = Inputs.str(
        description='Radiance parameters. -I, -c 1 and -aa 0 are already included in '
        'the command.', default=''
    )

    fixed_radiance_parameters = Inputs.str(
        description='Radiance parameters. -I, -c 1 and -aa 0 are already included in '
        'the command.', default='-aa 0'
    )

    sensor_count = Inputs.int(
        description='Number of maximum sensors in each generated grid.',
        spec={'type': 'integer', 'minimum': 1}
    )

    sky_matrix = Inputs.file(
        description='Path to a sky matrix.', path='sky.mtx',
        extensions=['mtx', 'smx']
    )

    sky_dome = Inputs.file(
        description='Path to a sky dome.', path='sky.dome'
    )

    sensor_grid = Inputs.file(
        description='Path to sensor grid files.', path='grid.pts',
        extensions=['pts']
    )

    scene_file = Inputs.file(
        description='Path to an octree file to describe the scene.', path='scene.oct',
        extensions=['oct']
    )

    conversion = Inputs.str(
        description='Conversion values as a string which will be passed to rmtxop -c.'
        'This option is useful to post-process the results from 3 RGB components into '
        'one as part of this command.', default=''
    )

    order_by = Inputs.str(
        description='An option to change how results are ordered in each row. By '
        'default each row are the results for each sensor during all the datetime. '
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
        'd for ASCII, float or double.', default='f',
        spec={'type': 'string', 'enum': ['a', 'd', 'f']}
    )

    bsdf_folder = Inputs.folder(
        description='Folder containing any BSDF files needed for ray tracing.',
        path='model/bsdf', optional=True
    )

    @command
    def run_daylight_coeff(self):
        return 'honeybee-radiance dc scoeff scene.oct grid.pts sky.dome sky.mtx ' \
            '--sensor-count {{self.sensor_count}} --output results.ill --rad-params ' \
            '"{{self.radiance_parameters}}" --rad-params-locked '\
            '"{{self.fixed_radiance_parameters}}" --conversion "{{self.conversion}}" ' \
            '--output-format {{self.output_format}} --order-by-{{self.order_by}} ' \
            '--{{self.header}}-header'

    result_file = Outputs.file(description='Output result file.', path='results.ill')


@dataclass
class DaylightCoefficientNoSkyMatrix(Function):
    """Calculate daylight coefficient for a grid of sensors."""

    radiance_parameters = Inputs.str(
        description='Radiance parameters. -I, -c 1 and -aa 0 are already included in '
        'the command.', default=''
    )

    fixed_radiance_parameters = Inputs.str(
        description='Radiance parameters. -I, -c 1 and -aa 0 are already included in '
        'the command.', default='-aa 0'
    )

    sensor_count = Inputs.int(
        description='Number of maximum sensors in each generated grid.',
        spec={'type': 'integer', 'minimum': 1}
    )

    sky_dome = Inputs.file(
        description='Path to a sky dome.', path='sky.dome'
    )

    sensor_grid = Inputs.file(
        description='Path to sensor grid files.', path='grid.pts',
        extensions=['pts']
    )

    scene_file = Inputs.file(
        description='Path to an octree file to describe the scene.', path='scene.oct',
        extensions=['oct']
    )

    conversion = Inputs.str(
        description='Conversion values as a string which will be passed to rmtxop -c.'
        'This option is useful to post-process the results from 3 RGB components into '
        'one as part of this command.', default=''
    )

    header = Inputs.str(
        default='keep',
        description='An input to indicate if header should be kept or removed from the'
        'output matrix.', spec={'type': 'string', 'enum': ['keep', 'remove']}
    )

    input_format = Inputs.str(
        description='Format type for input. Valid inputs are a, f and d for '
        'ASCII, float or double.', default='a',
        spec={'type': 'string', 'enum': ['a', 'd', 'f']}
    )

    output_format = Inputs.str(
        description='Output format for converted results. Valid inputs are a, f and '
        'd for ASCII, float or double.', default='f',
        spec={'type': 'string', 'enum': ['a', 'd', 'f']}
    )

    bsdf_folder = Inputs.folder(
        description='Folder containing any BSDF files needed for ray tracing.',
        path='model/bsdf', optional=True
    )

    @command
    def run_daylight_coeff(self):
        return 'honeybee-radiance dc coeff scene.oct grid.pts sky.dome ' \
            '--sensor-count {{self.sensor_count}} --output results.mtx --rad-params ' \
            '"{{self.radiance_parameters}}" --rad-params-locked ' \
            '"{{self.fixed_radiance_parameters}}" --conversion "{{self.conversion}}" ' \
            '--input-format {{self.input_format}} --output-format {{self.output_format}} ' \
            '--{{self.header}}-header'

    result_file = Outputs.file(description='Output result file.', path='results.mtx')
