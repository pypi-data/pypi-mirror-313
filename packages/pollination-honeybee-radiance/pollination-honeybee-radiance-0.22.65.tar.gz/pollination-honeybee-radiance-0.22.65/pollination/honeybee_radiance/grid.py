from dataclasses import dataclass
from pollination_dsl.function import Function, command, Inputs, Outputs


@dataclass
class SplitGrid(Function):
    """Split a single sensor grid file into multiple smaller grids."""

    sensor_count = Inputs.int(
        description='Number of maximum sensors in each generated grid.',
        spec={'type': 'integer', 'minimum': 1}
    )

    input_grid = Inputs.file(description='Input grid file.', path='grid.pts')

    @command
    def split_grid(self):
        return 'honeybee-radiance grid split grid.pts ' \
            '{{self.sensor_count}} --folder output --log-file output/grids_info.json'

    grids_list = Outputs.list(
        description='A JSON array that includes information about generated sensor '
        'grids.', path='output/grids_info.json'
    )

    output_folder = Outputs.folder(
        description='Output folder with new sensor grids.', path='output'
    )


@dataclass
class SplitGridFolder(Function):
    """Create new sensor grids folder with evenly distributed sensors.

    This function creates a new folder with evenly distributed sensor grids. The folder
    will include a ``_redist_info.json`` file which has the information to recreate the
    original input files from this folder and the results generated based on the grids
    in this folder.
    """

    input_folder = Inputs.folder(
        description='Input sensor grids folder.',
        path='input_folder'
    )

    cpu_count = Inputs.int(
        description='The number of processors to be used as a result of the '
        'grid-splitting operation. This value is equivalent to the number of '
        'sensor grids that will be generated when the cpus-per-grid is left as 1.',
        spec={'type': 'integer', 'minimum': 1}
    )

    cpus_per_grid = Inputs.int(
        description='An integer to be divided by the cpu-count to yield a final number '
        'of grids to generate. This is useful in workflows where there are multiple '
        'processors acting on a single grid. To ignore this limitation, set the '
        'value to 1.', spec={'type': 'integer', 'minimum': 1}, default=1
    )

    min_sensor_count = Inputs.int(
        description='The minimum number of sensors in each output grid. Use this '
        'number to ensure the number of sensors in output grids never gets very '
        'small. This input will take precedence over the input cpu-count and '
        'cpus-per-grid when specified. To ignore this limitation, set the value to 1. '
        'Otherwise the number of grids will be adjusted based on minimum sensor '
        'count if needed. Default: 2000.', default=2000,
        spec={'type': 'integer', 'minimum': 1}
    )

    @command
    def split_grid_folder(self):
        return 'honeybee-radiance grid split-folder ./input_folder ./output_folder ' \
            '{{self.cpu_count}} --grid-divisor {{self.cpus_per_grid}} ' \
            '--min-sensor-count {{self.min_sensor_count}}'

    sensor_grids = Outputs.list(
        description='A JSON array that includes information about generated sensor '
        'grids.', path='output_folder/_info.json'
    )

    sensor_grids_file = Outputs.file(
        description='A JSON file with information about generated sensor grids.',
        path='output_folder/_info.json'
    )

    dist_info = Outputs.file(
        description='A JSON file with distribution information.',
        path='output_folder/_redist_info.json'
    )

    output_folder = Outputs.folder(
        description='Output folder with new sensor grids.', path='output_folder'
    )


@dataclass
class SplitDataFolder(Function):
    """Split an optional folder of data using the same logic as SplitGridFolder."""

    input_folder = Inputs.folder(
        description='Input folder containing CSV files coordinated with sensor grids.',
        path='input_folder', optional=True
    )

    extension = Inputs.str(
        description='File extension including the . before the extension '
        '(e.g. .csv, .ill)', default='.pts'
    )

    cpu_count = Inputs.int(
        description='The number of processors to be used as a result of the '
        'grid-splitting operation. This value is equivalent to the number of '
        'sensor grids that will be generated when the cpus-per-grid is left as 1.',
        spec={'type': 'integer', 'minimum': 1}
    )

    cpus_per_grid = Inputs.int(
        description='An integer to be divided by the cpu-count to yield a final number '
        'of grids to generate. This is useful in workflows where there are multiple '
        'processors acting on a single grid. To ignore this limitation, set the '
        'value to 1.', spec={'type': 'integer', 'minimum': 1}, default=1
    )

    min_sensor_count = Inputs.int(
        description='The minimum number of sensors in each output grid. Use this '
        'number to ensure the number of sensors in output grids never gets very '
        'small. This input will take precedence over the input cpu-count and '
        'cpus-per-grid when specified. To ignore this limitation, set the value to 1. '
        'Otherwise the number of grids will be adjusted based on minimum sensor '
        'count if needed. Default: 2000.', default=2000,
        spec={'type': 'integer', 'minimum': 1}
    )

    grid_info_file = Inputs.file(
        description='Optional input JSON file containing information about '
        'the sensor grids to be split. If unspecified, it will be assumed that this '
        'JSON already exists in the input-folder with the name _info.json.',
        path='grid_info.json', optional=True
    )

    @command
    def split_grid_folder(self):
        return 'honeybee-radiance grid split-folder ./input_folder ./output_folder ' \
            '{{self.cpu_count}} {{self.extension}} ' \
            '--grid-divisor {{self.cpus_per_grid}} ' \
            '--min-sensor-count {{self.min_sensor_count}} ' \
            '--grid-info-file grid_info.json'

    output_folder = Outputs.folder(
        description='Output folder with new sensor grids.',
        path='output_folder', optional=True
    )


@dataclass
class MergeFiles(Function):
    """Merge several files with similar starting name into one."""

    name = Inputs.str(
        description='Base name for files to be merged.',
        default='grid'
    )

    extension = Inputs.str(
        description='File extension including the . before the extension (e.g. .res, '
        '.ill)'
    )

    folder = Inputs.folder(
        description='Target folder with the input files.',
        path='input_folder'
    )

    @command
    def merge_files(self):
        return 'honeybee-radiance grid merge input_folder grid ' \
            ' {{self.extension}} --name {{self.name}}'

    result_file = Outputs.file(
        description='Output result file.', path='{{self.name}}{{self.extension}}'
    )


@dataclass
class MergeFolderData(Function):
    """Restructure files in a distributed folder."""

    input_folder = Inputs.folder(
        description='Input sensor grids folder.',
        path='input_folder'
    )

    extension = Inputs.str(
        description='Extension of the files to collect data from. It will be ``pts`` '
        'for sensor files. Another common extension is ``ill`` for the results of '
        'daylight studies.'
    )

    dist_info = Inputs.file(
        description='Distribution information file.',
        path='dist_info.json', optional=True
    )

    @command
    def merge_files_in_folder(self):
        return 'honeybee-radiance grid merge-folder ./input_folder ./output_folder ' \
            ' {{self.extension}} --dist-info dist_info.json'

    output_folder = Outputs.folder(
        description='Output folder with newly generated files.', path='output_folder'
    )


@dataclass
class MirrorGrid(Function):
    """Split a single sensor grid file into multiple smaller grids."""

    input_grid = Inputs.file(description='Input grid file.', path='grid.pts')

    vector = Inputs.str(
        description='A string of three values (separated by spaces) to standardize '
        'the direction of all rays in the output files. For example, inputting '
        '"0 0 1" will ensure that the output sensor files all have vectors pointing '
        'up in the base file and down in the mirrored file. If unspecified, the '
        'direction of sensors in the input file will be used.', default='0 0 1'
    )

    @command
    def mirror_grid(self):
        return 'honeybee-radiance grid mirror grid.pts --vector "{{self.vector}}" ' \
            '--name result --suffix ref'

    base_file = Outputs.file(
        description='A sensor grid file facing the direction of the vector.',
        path='result.pts'
    )

    mirrored_file = Outputs.file(
        description='A sensor grid file facing the opposite direction of the vector.',
        path='result_ref.pts'
    )


@dataclass
class RadiantEnclosureInfo(Function):
    """Get a JSON of radiant enclosure information from a .pts file of a sensor grid.

    This enclosure info is intended to be consumed by thermal mapping functions.
    """

    model = Inputs.file(
        description='Path to input HBJSON or HBPkl file.',
        path='model.hbjson'
    )

    input_grid = Inputs.file(description='Input grid file.', path='grid.pts')

    air_boundary_distance = Inputs.str(
        description='A number to set the distance from air boundaries over which '
        'values should be interpolated. Using 0 will assume a hard edge between '
        'Rooms of the same radiant enclosures. This can include the units of '
        'the distance (eg. 3ft) or, if no units are provided the value will '
        'be interpreted in the honeybee model units.', default='2m'
    )

    @command
    def radiant_enclosure_info(self):
        return 'honeybee-radiance grid enclosure-info model.hbjson grid.pts ' \
            '--air-boundary-distance {{self.air_boundary_distance}} ' \
            '--output-file enclosure.json'

    enclosure_file = Outputs.file(
        description='A JSON file that includes radiant enclosure information '
        'for the sensors', path='enclosure.json'
    )
