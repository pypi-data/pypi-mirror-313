from dataclasses import dataclass
from pollination_dsl.function import Function, command, Inputs, Outputs


@dataclass
class RayTracingPicture(Function):
    """Run ray-tracing with rpict command for an input octree and a view file.."""

    view = Inputs.file(description='Input view file.', path='view.vf')

    scene_file = Inputs.file(
        description='Path to an octree file to describe the scene.', path='scene.oct'
    )

    radiance_parameters = Inputs.str(
        description='Radiance parameters to be exposed within recipes. -h is '
        'usually already included in the fixed_radiance_parameters and -I will '
        'be overwritten based on the input metric.', default='-ab 2'
    )

    metric = Inputs.str(
        description='Text for the type of metric to be output from the calculation. '
        'Choose from: illuminance, irradiance, luminance, radiance.',
        default='luminance',
        spec={'type': 'string',
              'enum': ['illuminance', 'irradiance', 'luminance', 'radiance']}
    )

    resolution = Inputs.int(
        description='An integer for the maximum dimension of the image in pixels '
        '(either width or height depending on the input view angle and type).',
        spec={'type': 'integer', 'minimum': 1}, default=800
    )

    scale_factor = Inputs.float(
        description='A number that will be multiplied by the input resolution to '
        'scale the dimensions of the output image. This is useful in workflows if '
        'one plans to re-scale the image after the ray tracing calculation to '
        'improve anti-aliasing.', default=1
    )

    ambient_cache = Inputs.file(
        description='Path to the ambient cache if an overture calculation was '
        'specified. If unspecified, no ambient cache will be used.',
        path='view.amb', optional=True
    )

    bsdf_folder = Inputs.folder(
        description='Folder containing any BSDF files needed for ray tracing.',
        path='model/bsdf', optional=True
    )

    @command
    def ray_tracing(self):
        return 'honeybee-radiance rpict rpict scene.oct view.vf ' \
            '--rad-params "{{self.radiance_parameters}}" --metric {{self.metric}} ' \
            '--resolution {{self.resolution}} --scale-factor {{self.scale_factor}} ' \
            '--output view.HDR'

    result_image = Outputs.file(
        description='Path to the High Dynamic Range (HDR) image file of the '
        'input view.', path='view.HDR'
    )
