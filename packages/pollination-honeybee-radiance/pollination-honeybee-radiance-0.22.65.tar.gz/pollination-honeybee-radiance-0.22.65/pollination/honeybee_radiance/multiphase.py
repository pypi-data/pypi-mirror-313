from dataclasses import dataclass
from pollination_dsl.function import Function, command, Inputs, Outputs


@dataclass
class ViewMatrix(Function):
    """Calculate view matrix for a receiver file."""

    radiance_parameters = Inputs.str(
        description='Radiance parameters. -I, -c 1 and -aa 0 are already included in '
        'the command.', default=''
    )

    fixed_radiance_parameters = Inputs.str(
        description='Radiance parameters. -I, -c 1 and -aa 0 are already included in '
        'the command.', default='-aa 0 -I -c 1'
    )

    sensor_count = Inputs.int(
        description='Minimum number of sensors in each generated grid.',
        spec={'type': 'integer', 'minimum': 1}
    )

    receiver_file = Inputs.file(
        description='Path to a receiver file.', path='receiver.rad',
        extensions=['rad']
    )

    sensor_grid = Inputs.file(
        description='Path to sensor grid files.', path='grid.pts',
        extensions=['pts']
    )

    scene_file = Inputs.file(
        description='Path to an octree file to describe the scene.', path='scene.oct',
        extensions=['oct']
    )

    receivers_folder = Inputs.folder(
        description='Folder containing any receiver files needed for ray tracing. '
        'This folder is usually the aperture group folder inside the model folder.',
        path='model/aperture_group'
    )

    bsdf_folder = Inputs.folder(
        description='Folder containing any BSDF files needed for ray tracing.',
        path='model/bsdf', optional=True
    )

    @command
    def run_view_mtx(self):
        return 'honeybee-radiance multi-phase view-matrix receiver.rad scene.oct ' \
            'grid.pts --sensor-count {{self.sensor_count}} ' \
            '--rad-params "{{self.radiance_parameters}}" --rad-params-locked ' \
            '"{{self.fixed_radiance_parameters}}"'

    view_mtx = Outputs.folder(
        description='Output view matrix folder.', path='vmtx'
    )


@dataclass
class FluxTransfer(Function):
    """Calculate flux transfer matrix between a sender and a receiver file."""

    radiance_parameters = Inputs.str(
        description='Radiance parameters. -aa 0 is already included in '
        'the command. Note that -c should not be 1.', default=''
    )

    fixed_radiance_parameters = Inputs.str(
        description='Radiance parameters.'
        'the command.', default='-aa 0'
    )

    receiver_file = Inputs.file(
        description='Path to a receiver file.', path='receiver.rad',
        extensions=['rad']
    )

    sender_file = Inputs.file(
        description='Path to sender file.', path='sender.rad',
        extensions=['rad']
    )

    senders_folder = Inputs.folder(
        description='Folder containing any senders files needed for ray tracing. '
        'This folder is usually the aperture group folder inside the model folder.',
        path='model/aperture_group'
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
    def run_flux_mtx(self):
        return 'honeybee-radiance multi-phase flux-transfer sender.rad receiver.rad ' \
               'scene.oct  --output output.dmx ' \
            '--rad-params "{{self.radiance_parameters}}" --rad-params-locked '\
            '"{{self.fixed_radiance_parameters}}"'

    flux_mtx = Outputs.file(
        description='Output daylight matrix file.', path='output.dmx'
    )


@dataclass
class MultiPhaseCombinations(Function):
    """Create two JSON files for multiplication combinations and results mapper."""

    sender_info = Inputs.file(
        description='Path to a JSON file that includes the information for senders. '
        'This file is created as an output of the daylight matrix grouping command.',
        path='sender_info.json', extensions=['json']
    )

    receiver_info = Inputs.file(
        description='Path to a JSON file that includes the information for receivers. '
        'This file is written to model/receiver folder.',
        path='receiver_info.json', extensions=['json']
    )

    states_info = Inputs.file(
        description='Path to a JSON file that includes the state information for all '
        'the aperture groups. This file is created under model/aperture_groups.',
        path='states_info.json', extensions=['json']
    )

    @command
    def calculate_multiphase_combs(self):
        return 'honeybee-radiance multi-phase three-phase combinations ' \
            'sender_info.json receiver_info.json states_info.json --folder combs ' \
            '-rn 3phase_results_info -cn 3phase_multiplication_info'

    multiplication_file = Outputs.file(
        description='The combination of matrix multiplication for 3 Phase studies.',
        path='combs/3phase_multiplication_info.json'
    )

    multiplication_info = Outputs.list(
        description='The combination of matrix multiplication for 3 Phase studies.',
        path='combs/3phase_multiplication_info.json'
    )

    results_mapper = Outputs.file(
        description='Results mapper for each sensor grid in the model.',
        path='combs/3phase_results_info.json'
    )


@dataclass
class DaylightMatrixGrouping(Function):
    """Group apertures for daylight matrix."""

    model_folder = Inputs.folder(
        description='Radiance model folder', path='model'
    )

    scene_file = Inputs.file(
        description='Path to an octree file to describe the scene.', path='scene.oct',
        extensions=['oct']
    )

    sky_dome = Inputs.file(
        description='Path to rflux sky file.', path='sky.dome'
    )

    dmtx_group_params = Inputs.str(
        description='A string to change the parameters for aperture grouping for '
        'daylight matrix calculation. Valid keys are -s for aperture grid size, -t for '
        'the threshold that determines if two apertures/aperture groups can be '
        'clustered, and -ad for ambient divisions used in view factor calculation '
        'The default is -s 0.2 -t 0.001 -ad 1000. The order of the keys is not '
        'important and you can include one or all of them. For instance if you only '
        'want to change the aperture grid size to 0.5 you should use -s 0.5 as the '
        'input.', default='-s 0.2 -t 0.001 -ad 1000'
    )

    @command
    def group_apertures(self):
        return 'honeybee-radiance multi-phase dmtx-group model scene.oct sky.dome ' \
            '--output-folder output --name _info {{self.dmtx_group_params}}'

    grouped_apertures_folder = Outputs.folder(
        description='Output folder to grouped apertures.',
        path='output/groups'
    )

    grouped_apertures = Outputs.list(
        description='List of names for grouped apertures.',
        path='output/groups/_info.json'
    )

    grouped_apertures_file = Outputs.file(
        description='Grouped apertures information file.',
        path='output/groups/_info.json'
    )


@dataclass
class PrepareMultiphase(Function):
    """Generate several octrees from a Radiance folder as well as evenly distributed
    grids.

    Use this function to create octrees and grids for multi-phase simulations.
    """

    # inputs
    model = Inputs.folder(description='Path to Radiance model folder.', path='model')

    phase = Inputs.int(
        description='Select a multiphase study for which octrees will be created. '
        '3-phase includes 2-phase, and 5-phase includes 3-phase and 2-phase. The valid '
        'values are 2, 3 and 5',
        default=5
    )

    sunpath = Inputs.file(
        description='Path to sunpath file.', path='sun.path', optional=True
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

    static = Inputs.str(
        description='An input to indicate if static apertures should be excluded or '
        'included. If excluded static apertures will not be treated as its own dynamic '
        'state.', spec={'type': 'string', 'enum': ['exclude', 'include']},
        default='exclude'
    )

    default_states = Inputs.str(
        description='An input to indicate if all aperture group states should be '
        'simulated or if only the default states should be simulated.',
        spec={'type': 'string', 'enum': ['default', 'all']},
        default='all'
    )

    @command
    def prepare_multiphase(self):
        return 'honeybee-radiance multi-phase prepare-multiphase model ' \
            '{{self.cpu_count}} --grid-divisor {{self.cpus_per_grid}} ' \
            '--min-sensor-count {{self.min_sensor_count}} --sun-path sun.path ' \
            '--phase {{self.phase}} --octree-folder octree --grid-folder grid ' \
            '--{{self.static}}-static --{{self.default_states}}-states'

    # outputs
    scene_folder = Outputs.folder(
        description='Output octrees folder.', path='octree', optional=True)

    scene_info = Outputs.dict(
        description='Output octree files list.', path='multi_phase.json'
    )

    grid_folder = Outputs.folder(
        description='Output grid folder.', path='grid', optional=True)

    two_phase_info = Outputs.file(
        description='Output octree files and grid information file for the 2-Phase '
        'studies.', path='two_phase.json'
    )

    two_phase_info_list = Outputs.list(
        description='Output octree files and grid information file for the 2-Phase '
        'studies.', path='two_phase.json'
    )

    three_phase_info = Outputs.file(
        description='Output octree files and grid information file for the 3-Phase studies.',
        path='three_phase.json'
    )

    three_phase_info_list = Outputs.list(
        description='Output octree files and grid information file for the 3-Phase studies.',
        path='three_phase.json'
    )

    five_phase_info = Outputs.file(
        description='Output octree files and grid information file for the 5-Phase studies.',
        path='five_phase.json'
    )

    five_phase_info_list = Outputs.list(
        description='Output octree files and grid information file for the 5-Phase studies.',
        path='five_phase.json'
    )

    grid_states_file = Outputs.file(
        description='Grid and states information for aperture groups.',
        path='grid_states.json',
        optional=True
    )


@dataclass
class AddApertureGroupBlinds(Function):
    """Add a state geometry to aperture groups.

    This command adds state geometry to all aperture groups in the model. The
    geometry is the same as the aperture geometry but the modifier is changed.
    The geometry is translated inward by a distance which by default is 0.001
    in model units.
    """

    # inputs
    model = Inputs.folder(
        description='Path to Radiance model folder.',
        path='model.hbjson'
    )

    diffuse_transmission = Inputs.float(
        description='Diffuse transmission of the aperture group blinds. Default '
        'is 0.05 (5%).',
        default=0.05
    )

    specular_transmission = Inputs.float(
        description='Specular transmission of the aperture group blinds. Default '
        'is 0 (0%).',
        default=0
    )

    distance = Inputs.float(
        description='Distance from the aperture parent surface to the blind '
        'surface.',
        default=0.001
    )

    scale = Inputs.float(
        description='Scaling value to scale blind geometry at the center point '
        'of the aperture.',
        default=1.005
    )

    @command
    def add_aperture_group_blinds(self):
        return 'honeybee-radiance multi-phase add-aperture-group-blinds ' \
            'model.hbjson --diffuse-transmission {{self.diffuse_transmission}} ' \
            '--specular-transmission {{self.specular_transmission}} ' \
            '--distance {{self.distance}} --scale {{self.scale}} ' \
            '--output-model model_blinds.hbjson'

    # outputs
    output_model = Outputs.file(
        description='Model file with blind geometry.', path='model_blinds.hbjson'
    )
