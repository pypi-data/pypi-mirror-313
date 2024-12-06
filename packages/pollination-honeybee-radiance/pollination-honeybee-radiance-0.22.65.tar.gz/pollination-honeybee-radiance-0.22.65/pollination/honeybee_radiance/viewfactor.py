from dataclasses import dataclass
from pollination_dsl.function import Function, command, Inputs, Outputs


@dataclass
class ViewFactorModifiers(Function):
    """Get a list of modifiers and a corresponding Octree for surface view factors.
    """

    model = Inputs.file(
        description='Path to input HBJSON or HBPkl file.',
        path='model.hbjson'
    )

    include_sky = Inputs.str(
        default='include',
        description='A value to indicate whether a sky dome should be included in '
        'the resulting octree. The inclusion of the sky dome enables the sky view '
        'to be computed in the resulting calculation. Default is include.',
        spec={'type': 'string', 'enum': ['include', 'exclude']}
    )

    include_ground = Inputs.str(
        default='include',
        description='A value to indicate whether a ground dome should be included in '
        'the resulting octree. The inclusion of the ground dome enables the ground view '
        'to be computed in the resulting calculation. Default is include.',
        spec={'type': 'string', 'enum': ['include', 'exclude']}
    )

    grouped_shades = Inputs.str(
        default='grouped',
        description='A value to indicate whether the shade geometries should be '
        'included in the list of modifiers. Note that they are still included in '
        'the resulting octree but are just excluded from the list of modifiers. '
        'Default is grouped.',
        spec={'type': 'string', 'enum': ['grouped', 'individual']}
    )

    @command
    def hbjson_to_view_factor_modifiers(self):
        return 'honeybee-radiance view-factor modifiers model.hbjson ' \
            '--{{self.include_sky}}-sky --{{self.include_ground}}-ground ' \
            '--{{self.grouped_shades}}-shades --name scene'

    modifiers_file = Outputs.file(
        description='Output modifiers list file.', path='scene.mod'
    )

    scene_file = Outputs.file(
        description='Output octree file that is aligned with the modifiers.',
        path='scene.oct'
    )


@dataclass
class SphericalViewFactorContribution(Function):
    """Calculate spherical view factor contribution for a grid of sensors."""

    radiance_parameters = Inputs.str(
        description='Radiance parameters. -I and -aa 0 are already included in '
        'the command.', default=''
    )

    fixed_radiance_parameters = Inputs.str(
        description='Radiance parameters. -I and -aa 0 are already included in '
        'the command.', default='-aa 0'
    )

    ray_count = Inputs.int(
        description='The number of rays to be equally distributed over a sphere '
        'to compute the view factor for each of the input sensors.', default=6,
        spec={'type': 'integer', 'minimum': 2}
    )

    modifiers = Inputs.file(
        description='Path to modifiers file. In most cases modifiers are sun modifiers.',
        path='scene.mod'
    )

    sensor_grid = Inputs.file(
        description='Path to sensor grid files.', path='grid.pts',
        extensions=['pts']
    )

    scene_file = Inputs.file(
        description='Path to an octree file to describe the scene.', path='scene.oct',
        extensions=['oct']
    )

    @command
    def run_daylight_coeff(self):
        return 'honeybee-radiance view-factor contrib scene.oct grid.pts scene.mod ' \
            '--ray-count {{self.ray_count}} --rad-params "{{self.radiance_parameters}}" ' \
            '--rad-params-locked "{{self.fixed_radiance_parameters}}" --name view_factor'

    view_factor_file = Outputs.file(
        description='Output file with a matrix of spherical view factors from the '
        'sensors to the modifiers.', path='view_factor.csv'
    )
