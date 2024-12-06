from dataclasses import dataclass
from pollination_dsl.function import Function, command, Inputs, Outputs


@dataclass
class SplitViewCount(Function):
    """Get the number of times to split each view in a model using a CPU count."""

    views_file = Inputs.file(
        description='Views information JSON file.', path='view_info.json'
    )

    cpu_count = Inputs.int(
        description='The number of processors to be used as a result of the '
        'grid-splitting operation.',
        spec={'type': 'integer', 'minimum': 1}
    )

    @command
    def split_view_count(self):
        return 'honeybee-radiance view split-count view_info.json ' \
            '{{self.cpu_count}} --output-file view-split-count.txt'

    split_count = Outputs.int(
        description='An integer for the number of times to split the view.',
        path='view-split-count.txt'
    )


@dataclass
class SplitView(Function):
    """Split a single view file (.vf) into multiple smaller views."""

    input_view = Inputs.file(description='Input view file.', path='view.vf')

    view_count = Inputs.int(
        description='Number of views into which the input view will be subdivided.',
        spec={'type': 'integer', 'minimum': 1}
    )

    resolution = Inputs.int(
        description='An optional integer for the maximum dimension of the image in '
        'pixels. This value will automatically lower the input view_count to ensure '
        'the resulting images can be combined to meet this dimension.',
        spec={'type': 'integer', 'minimum': 1}, default=800
    )

    overture = Inputs.str(
        description='A switch to note whether an ambient file (.amb) should be '
        'generated for an overture calculation before the view is split into smaller '
        'views. With an overture calculation, the ambient file (aka ambient cache) is '
        'first populated with values. Thereby ensuring that - when reused to create '
        'an image - Radiance uses interpolation between already calculated values '
        'rather than less reliable extrapolation. The overture calculation has '
        'comparatively small computation time to full rendering but is single-core '
        'can become time consuming in situations with very high numbers of '
        'rendering multiprocessors.', default='overture',
        spec={'type': 'string', 'enum': ['overture', 'skip-overture']}
    )

    scene_file = Inputs.file(
        description='Path to an octree file for the overture calculation. This must be '
        'specified when the overture is not skipped.', path='scene.oct', optional=True
    )

    radiance_parameters = Inputs.str(
        description='Radiance parameters for the overture calculation. '
        'If unspecified, default rpict paramters will be used.',
        default='-ab 2'
    )

    bsdf_folder = Inputs.folder(
        description='Folder containing any BSDF files needed for ray tracing.',
        path='model/bsdf', optional=True
    )

    @command
    def split_view(self):
        return 'honeybee-radiance view split view.vf ' \
            '{{self.view_count}} --resolution {{self.resolution}} --{{self.overture}} ' \
            '--octree scene.oct --rad-params "{{self.radiance_parameters}}" ' \
            '--folder output --log-file output/views_info.json'

    views_list = Outputs.list(
        description='A JSON array that includes information about generated '
        'views.', path='output/views_info.json'
    )

    output_folder = Outputs.folder(
        description='Output folder with new view files.', path='output'
    )

    ambient_cache = Outputs.file(
        description='Path to the ambient cache if an overture calculation was '
        'specified.', path='output/view.amb', optional=True
    )


@dataclass
class MergeImages(Function):
    """Merge several .HDR image files with similar starting name into one."""

    folder = Inputs.folder(
        description='Target folder with the input .HDR image files.',
        path='input_folder'
    )

    name = Inputs.str(
        description='Base name for files to be merged.',
        default='view'
    )

    extension = Inputs.str(
        description='File extension including the . before the extension '
        '(e.g. .HDR, .pic, .unf)', default='.unf'
    )

    scale_factor = Inputs.float(
        description='A number that will be used to scale the dimensions of the '
        'output image as it is filtered for anti-aliasing.', default=1
    )

    original_view = Inputs.file(
        description='Full path to the original view file.',
        path='original-view.vf',
        optional=True
    )

    @command
    def merge_files(self):
        return 'honeybee-radiance view merge input_folder view ' \
            '{{self.extension}} --scale-factor {{self.scale_factor}} ' \
            '--name {{self.name}} --view original-view.vf'

    result_image = Outputs.file(
        description='Output combined image file.', path='{{self.name}}.HDR'
    )
