from dataclasses import dataclass
from pollination_dsl.function import Function, command, Inputs, Outputs


@dataclass
class CreateOctree(Function):
    """Generate an octree from a Radiance folder."""

    # inputs
    include_aperture = Inputs.str(
        default='include',
        description='A value to indicate if the static aperture should be included in '
        'octree. Valid values are include and exclude. Default is include.',
        spec={'type': 'string', 'enum': ['include', 'exclude']}
    )

    black_out = Inputs.str(
        default='default',
        description='A value to indicate if the black material should be used. Valid '
        'values are default and black. Default value is default.',
        spec={'type': 'string', 'enum': ['black', 'default']}
    )

    model = Inputs.folder(description='Path to Radiance model folder.', path='model')

    @command
    def create_octree(self):
        return 'honeybee-radiance octree from-folder model --output scene.oct ' \
            '--{{self.include_aperture}}-aperture --{{self.black_out}}'

    # outputs
    scene_file = Outputs.file(description='Output octree file.', path='scene.oct')


@dataclass
class CreateOctreeWithSky(CreateOctree):
    """Generate an octree from a Radiance folder and a sky!"""

    # inputs
    sky = Inputs.file(description='Path to sky file.', path='sky.sky')

    @command
    def create_octree(self):
        return 'honeybee-radiance octree from-folder model --output scene.oct ' \
            '--{{self.include_aperture}}-aperture --{{self.black_out}} ' \
            '--add-before sky.sky'


@dataclass
class CreateOctrees(Function):
    """Generate several octree from a Radiance folder.

    Use this function to create octrees for multi-phase simulations.
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

    @command
    def create_octrees(self):
        return 'honeybee-radiance octree from-folder-multiphase model ' \
            '--sun-path sun.path --output-folder octree --phase {{self.phase}}'

    # outputs
    scene_folder = Outputs.folder(
        description='Output octrees folder.', path='octree')

    scene_info = Outputs.list(
        description='Output octree files list.', path='octree/multi_phase.json'
    )

    two_phase_info = Outputs.list(
        description='Output octree files list for the 2-Phase studies.',
        path='octree/two_phase.json',
    )

    three_phase_info = Outputs.list(
        description='Output octree files list for the 3-Phase studies.',
        path='octree/three_phase.json',
        optional=True
    )

    five_phase_info = Outputs.list(
        description='Output octree files list for the 5-Phase studies.',
        path='octree/five_phase.json',
        optional=True
    )


@dataclass
class CreateOctreeAbstractedGroups(Function):
    """Generate a set of octrees from a folder containing abstracted aperture groups."""

    # inputs
    model = Inputs.folder(description='Path to Radiance model folder.', path='model')

    sunpath = Inputs.file(
        description='Path to sunpath file.', path='sunpath.mtx', optional=True
    )

    @command
    def create_octree(self):
        return 'honeybee-radiance octree from-abstracted-groups model ' \
            '--sun-path sunpath.mtx --output-folder octree'

    # outputs
    scene_folder = Outputs.folder(description='Output octrees folder.', path='octree')

    scene_info = Outputs.list(
        description='Output octree files list.', path='octree/group_info.json'
    )


@dataclass
class CreateOctreeShadeTransmittance(Function):
    """Generate a set of octrees from a folder containing shade transmittance groups."""

    # inputs
    model = Inputs.folder(description='Path to Radiance model folder.', path='model')

    sunpath = Inputs.file(
        description='Path to sunpath file.', path='sunpath.mtx', optional=True
    )

    @command
    def create_octree(self):
        return 'honeybee-radiance octree from-shade-trans-groups model ' \
            '--sun-path sunpath.mtx --output-folder octree'

    # outputs
    scene_folder = Outputs.folder(description='Output octrees folder.', path='octree')

    scene_info = Outputs.list(
        description='Output octree files list.', path='octree/trans_info.json'
    )


@dataclass
class CreateOctreeStatic(Function):
    """Generate an octree from a Radiance folder."""

    # inputs
    model = Inputs.folder(description='Path to Radiance model folder.', path='model')

    @command
    def create_octree(self):
        return 'honeybee-radiance octree from-folder-static model ' \
            '--output scene.oct'

    # outputs
    scene_file = Outputs.file(description='Output octree file.', path='scene.oct')


@dataclass
class CreateOctreeWithSkyStatic(CreateOctreeStatic):
    """Generate an octree from a Radiance folder and a sky."""

    # inputs
    sky = Inputs.file(description='Path to sky file.', path='sky.sky')

    @command
    def create_octree(self):
        return 'honeybee-radiance octree from-folder-static model ' \
            '--output scene.oct --add-before sky.sky'

    # outputs
    scene_file = Outputs.file(description='Output octree file.', path='scene.oct')
