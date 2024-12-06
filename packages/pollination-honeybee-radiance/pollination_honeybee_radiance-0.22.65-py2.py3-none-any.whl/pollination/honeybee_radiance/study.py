from dataclasses import dataclass
from pollination_dsl.function import Function, command, Inputs, Outputs


@dataclass
class StudyInfo(Function):
    """Create a study info file.
    
    This function generates study info file with the timestep and the hoys of
    the wea.
    """

    wea = Inputs.file(
        description='Path to a wea file.', extensions=['wea', 'epw'], path='sky.epw'
    )

    timestep = Inputs.int(
        description='Timestep of the study.', default=1,
        spec={'type': 'integer', 'minimum': 1}
    )

    @command
    def create_study_info(self):
        return 'honeybee-radiance study study-info sky.epw {{self.timestep}} ' \
            '--name study_info'

    study_info = Outputs.file(
        description='Path to study info file.', path='study_info.json'
    )
