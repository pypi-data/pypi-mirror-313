from dataclasses import dataclass
from pollination_dsl.function import Function, command, Inputs, Outputs


@dataclass
class EPWtoDaylightHours(Function):
    """Convert EPW to EN 17037 schedule as a CSV file.
    
    This function generates a valid schedule for EN 17037, also known as daylight hours.
    Rather than a typical occupancy schedule, the daylight hours is half the year with
    the largest quantity of daylight.
    """

    epw = Inputs.file(
        description='Path to epw file.', path='weather.epw', extensions=['epw']
    )

    @command
    def create_daylight_hours(self):
        return 'honeybee-radiance schedule epw-to-daylight-hours weather.epw ' \
            '--name daylight_hours'

    daylight_hours = Outputs.file(
        description='Path to daylight hours schedule.', path='daylight_hours.csv'
    )
