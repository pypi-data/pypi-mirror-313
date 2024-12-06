from dataclasses import dataclass
from pollination_dsl.function import Function, command, Inputs, Outputs


@dataclass
class RayTracingDaylightFactor(Function):
    """Run ray-tracing and post-process the results for a daylight factor simulation."""

    radiance_parameters = Inputs.str(
        description='Radiance parameters to be exposed within recipes. -I and -h are '
        'usually already included in the fixed_radiance_parameters.',
        default='-ab 2'
    )

    sky_illum = Inputs.int(
        description='Sky illuminance level for the sky included in octree.',
        default=100000
    )

    fixed_radiance_parameters = Inputs.str(
        description='Parameters that are meant to be fixed for a given recipe and '
        'should not be overwritten by radiance_parameters input.', default='-I -h'
    )

    grid = Inputs.file(description='Input sensor grid.', path='grid.pts')

    scene_file = Inputs.file(
        description='Path to an octree file to describe the scene.', path='scene.oct'
    )

    bsdf_folder = Inputs.folder(
        description='Folder containing any BSDF files needed for ray tracing.',
        path='model/bsdf', optional=True
    )

    @command
    def ray_tracing(self):
        return 'honeybee-radiance raytrace daylight-factor scene.oct grid.pts ' \
            '--rad-params "{{self.radiance_parameters}}" --rad-params-locked ' \
            '"{{self.fixed_radiance_parameters}}" --sky-illum {{self.sky_illum}} ' \
            '--output grid.res'

    result = Outputs.file(
        description='Daylight factor results file. The results for each sensor is in a '
        'new line.', path='grid.res'
    )


@dataclass
class RayTracingPointInTime(Function):
    """Run ray-tracing and post-process the results for a point-in-time simulation."""

    radiance_parameters = Inputs.str(
        description='Radiance parameters to be exposed within recipes. -h is '
        'usually already included in the fixed_radiance_parameters and -I will '
        'be overwritten based on the input metric.', default='-ab 2'
    )

    metric = Inputs.str(
        description='Text for the type of metric to be output from the calculation. '
        'Choose from: illuminance, irradiance, luminance, radiance.',
        default='illuminance',
        spec={'type': 'string',
              'enum': ['illuminance', 'irradiance', 'luminance', 'radiance']}
    )

    fixed_radiance_parameters = Inputs.str(
        description='Parameters that are meant to be fixed for a given recipe and '
        'should not be overwritten by radiance_parameters input.', default='-h'
    )

    grid = Inputs.file(description='Input sensor grid.', path='grid.pts')

    scene_file = Inputs.file(
        description='Path to an octree file to describe the scene.', path='scene.oct'
    )

    bsdf_folder = Inputs.folder(
        description='Folder containing any BSDF files needed for ray tracing.',
        path='model/bsdf', optional=True
    )

    @command
    def ray_tracing(self):
        return 'honeybee-radiance raytrace point-in-time scene.oct grid.pts ' \
            '--rad-params "{{self.radiance_parameters}}" --rad-params-locked ' \
            '"{{self.fixed_radiance_parameters}}" --metric {{self.metric}} ' \
            '--output grid.res'

    result = Outputs.file(
        description='Point-in-time result file. The result for each sensor is in a '
        'new line of the file. Values are in standard SI units of the input '
        'metric (lux, W/m2, cd/m2, W/m2-sr).', path='grid.res'
    )


@dataclass
class RayTracingSkyView(Function):
    """Run ray-tracing and post-process the results for a skyview simulation."""

    radiance_parameters = Inputs.str(
        description='Radiance parameters to be exposed within recipes. -I and -h are '
        'usually already included in the fixed_radiance_parameters.',
        default='-aa 0.1 -ad 2048 -ar 64'
    )

    fixed_radiance_parameters = Inputs.str(
        description='Parameters that are meant to be fixed for a given recipe and '
        'should not be overwritten by radiance_parameters input.',
        default='-I -ab 1 -h'
    )

    grid = Inputs.file(description='Input sensor grid.', path='grid.pts')

    scene_file = Inputs.file(
        description='Path to an octree file to describe the scene.', path='scene.oct'
    )

    bsdf_folder = Inputs.folder(
        description='Folder containing any BSDF files needed for ray tracing.',
        path='model/bsdf', optional=True
    )

    @command
    def ray_tracing(self):
        return 'honeybee-radiance raytrace daylight-factor scene.oct grid.pts ' \
            '--rad-params "{{self.radiance_parameters}}" --rad-params-locked ' \
            '"{{self.fixed_radiance_parameters}}" --output grid.res'

    result = Outputs.file(
        description='Sky view/exposure results file. The percentage values for '
        'each sensor is in a new line.', path='grid.res'
    )
