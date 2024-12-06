from dataclasses import dataclass
from pollination_dsl.function import Function, command, Inputs, Outputs


@dataclass
class ConvertToBinary(Function):
    """Convert a Radiance matrix to a new matrix with 0-1 values."""

    # inputs
    input_mtx = Inputs.file(
        description='Input Radiance matrix in ASCII format',
        path='input.mtx'
    )

    minimum = Inputs.float(
        description='Minimum range for the values that will be converted to 1.',
        default=-1 * 10**100
    )

    maximum = Inputs.float(
        description='Maximum range for the values that will be converted to 1.',
        default=10**100
    )

    include_min = Inputs.str(
        description='A flag to include the minimum threshold itself. By default the '
        'threshold value will be included.', default='include',
        spec={'type': 'string', 'enum': ['include', 'exclude']}
    )

    include_max = Inputs.str(
        description='A flag to include the maximum threshold itself. By default the '
        'threshold value will be included.', default='include',
        spec={'type': 'string', 'enum': ['include', 'exclude']}
    )

    reverse = Inputs.str(
        description='A flag to reverse the selection logic. This is useful for cases '
        'that you want to all the values outside a certain range to be converted to 1. '
        'By default the input logic will be used as is.', default='comply',
        spec={'type': 'string', 'enum': ['comply', 'reverse']}
    )

    @command
    def convert_to_zero_one(self):
        return 'honeybee-radiance post-process convert-to-binary input.mtx ' \
            '--output binary.mtx --maximum {{self.maximum}} ' \
            '--minimum {{self.minimum}} --{{self.reverse}} ' \
            '--{{self.include_min}}-min --{{self.include_max}}-max'

    # outputs
    output_mtx = Outputs.file(
        description='Newly created binary matrix.', path='binary.mtx'
    )


@dataclass
class Count(Function):
    """Count values in a row that meet a certain criteria."""

    # inputs
    input_mtx = Inputs.file(
        description='Input Radiance matrix in ASCII format',
        path='input.mtx'
    )

    minimum = Inputs.float(
        description='Minimum range for the values that should be counted.',
        default=-1 * 10**100
    )

    maximum = Inputs.float(
        description='Maximum range for the values that should be counted.',
        default=10**100
    )

    include_min = Inputs.str(
        description='A flag to include the minimum threshold itself. By default the '
        'threshold value will be included.', default='include',
        spec={'type': 'string', 'enum': ['include', 'exclude']}
    )

    include_max = Inputs.str(
        description='A flag to include the maximum threshold itself. By default the '
        'threshold value will be included.', default='include',
        spec={'type': 'string', 'enum': ['include', 'exclude']}
    )

    reverse = Inputs.str(
        description='A flag to reverse the selection logic. This is useful for cases '
        'that you want to all the values outside a certain range. By default the input '
        'logic will be used as is.', default='comply',
        spec={'type': 'string', 'enum': ['comply', 'reverse']}
    )

    @command
    def count_values(self):
        return 'honeybee-radiance post-process count input.mtx ' \
            '--output counter.mtx --maximum {{self.maximum}} ' \
            '--minimum {{self.minimum}} --{{self.reverse}} ' \
            '--{{self.include_min}}-min --{{self.include_max}}-max'

    # outputs
    output_mtx = Outputs.file(
        description='Newly created binary matrix.', path='counter.mtx'
    )


@dataclass
class SumRow(Function):
    """Postprocess a Radiance matrix and add all the numbers in each row.

    This function is useful for translating Radiance results to outputs like radiation
    to total radiation. Input matrix must be in ASCII format. The header in the input
    file will be ignored.
    """

    # inputs
    input_mtx = Inputs.file(
        description='Input Radiance matrix in ASCII format',
        path='input.mtx'
    )

    divisor = Inputs.float(
        description='An optional number, that the summed row will be divided by. '
        'For example, this can be a timestep, which can be used to ensure that a '
        'summed row of irradiance yields cumulative radiation over the entire '
        'time period of the matrix.',
        default=1
    )

    @command
    def sum_mtx_row(self):
        return 'honeybee-radiance post-process sum-row input.mtx ' \
            '--divisor {{self.divisor}} --output sum.mtx'

    # outputs
    output_mtx = Outputs.file(description='Newly created sum matrix.', path='sum.mtx')


@dataclass
class AverageRow(Function):
    """Postprocess a Radiance matrix and average all the numbers in each row."""

    # inputs
    input_mtx = Inputs.file(
        description='Input Radiance matrix in ASCII format',
        path='input.mtx'
    )

    @command
    def average_mtx_row(self):
        return 'honeybee-radiance post-process average-row input.mtx ' \
            '--output average.mtx'

    # outputs
    output_mtx = Outputs.file(
        description='Newly created average matrix.', path='average.mtx'
    )


@dataclass
class CumulativeRadiation(Function):
    """Postprocess average irradiance (W/m2) into cumulative radiation (kWh/m2)."""

    # inputs
    average_irradiance = Inputs.file(
        description='A single-column matrix of average irradiance values in '
        'ASCII format', path='avg_irr.mtx'
    )

    wea = Inputs.file(
        description='The .wea file that was used in the simulation. This will be '
        'used to determine the duration of the analysis. This can also be an '
        '.epw file.', path='weather.epw'
    )

    timestep = Inputs.int(
        description='The timestep of the Wea file, which is used to to compute '
        'cumulative radiation over the time period of the Wea.', default=1
    )

    @command
    def average_mtx_row(self):
        return 'honeybee-radiance post-process cumulative-radiation avg_irr.mtx ' \
            'weather.epw --timestep {{self.timestep}} --output radiation.mtx'

    # outputs
    radiation = Outputs.file(
        description='Newly created matrix of cumulative radiation.',
        path='radiation.mtx'
    )


@dataclass
class AnnualIrradianceMetrics(Function):
    """Calculate annual irradiance metrics for annual irradiance simulation."""

    folder = Inputs.folder(
        description='A folder output from and annual irradiance recipe.',
        path='raw_results'
    )

    wea = Inputs.file(
        description='The .wea file that was used in the annual irradiance simulation. '
        'This will be used to determine the duration of the analysis for computing '
        'average irradiance. This can also be an .epw file.', path='weather.epw'
    )

    timestep = Inputs.int(
        description='The timestep of the Wea file, which is used to ensure the '
        'summed row of irradiance yields cumulative radiation over the time '
        'period of the Wea.', default=1
    )

    @command
    def calculate_irradiance_metrics(self):
        return 'honeybee-radiance post-process annual-irradiance raw_results ' \
            'weather.epw --timestep {{self.timestep}} --sub-folder ../metrics'

    # outputs
    metrics = Outputs.folder(
        description='Annual irradiance metrics folder. This folder includes all '
        'the other subfolders which are exposed as separate outputs.', path='metrics'
    )

    average_irradiance = Outputs.folder(
        description='Average irradiance in W/m2 for each sensor over the wea period.',
        path='metrics/average_irradiance'
    )

    peak_irradiance = Outputs.folder(
        description='The highest irradiance value in W/m2 for each sensor during '
        'the wea period.', path='metrics/average_irradiance'
    )

    cumulative_radiation = Outputs.folder(
        description='The cumulative radiation in kWh/m2 for each sensor over '
        'the wea period.', path='metrics/cumulative_radiation'
    )

    timestep_file = Outputs.file(
        description='File to track the timestep of the results. Useful for '
        'further result post-processing', path='raw_results/timestep.txt'
    )


@dataclass
class AnnualDaylightMetrics(Function):
    """Calculate annual daylight metrics for annual daylight simulation."""

    folder = Inputs.folder(
        description='This folder is an output folder of annual daylight recipe. Folder '
        'should include grids_info.json and sun-up-hours.txt. The command uses the list '
        'in grids_info.json to find the result files for each sensor grid.',
        path='raw_results'
    )

    schedule = Inputs.file(
        description='Path to an annual schedule file. Values should be 0-1 separated '
        'by new line. If not provided an 8-5 annual schedule will be created.',
        path='schedule.txt', optional=True
    )

    thresholds = Inputs.str(
        description='A string to change the threshold for daylight autonomy and useful '
        'daylight illuminance. Valid keys are -t for daylight autonomy threshold, -lt '
        'for the lower threshold for useful daylight illuminance and -ut for the upper '
        'threshold. The defult is -t 300 -lt 100 -ut 3000. The order of the keys is not '
        'important and you can include one or all of them. For instance if you only '
        'want to change the upper threshold to 2000 lux you should use -ut 2000 as '
        'the input.', default='-t 300 -lt 100 -ut 3000'
    )

    @command
    def calculate_annual_metrics(self):
        return 'honeybee-radiance post-process annual-daylight raw_results ' \
            '--schedule schedule.txt {{self.thresholds}} --sub_folder ../metrics'

    # outputs
    annual_metrics = Outputs.folder(
        description='Annual metrics folder. This folder includes all the other '
        'subfolders which are also exposed as separate outputs.', path='metrics'
    )

    metrics_info = Outputs.file(
        description='A config file with metrics subfolders information for '
        'visualization. This config file is compatible with honeybee-vtk config.',
        path='metrics/config.json'
    )

    daylight_autonomy = Outputs.folder(
        description='Daylight autonomy results.', path='metrics/da'
    )

    continuous_daylight_autonomy = Outputs.folder(
        description='Continuous daylight autonomy results.', path='metrics/cda'
    )

    useful_daylight_illuminance_lower = Outputs.folder(
        description='Lower useful daylight illuminance results.',
        path='metrics/udi_lower'
    )

    useful_daylight_illuminance = Outputs.folder(
        description='Useful daylight illuminance results.', path='metrics/udi'
    )

    useful_daylight_illuminance_upper = Outputs.folder(
        description='Upper useful daylight illuminance results.',
        path='metrics/udi_upper'
    )


@dataclass
class AnnualDaylightEN17037Metrics(Function):
    """Calculate annual daylight EN 173037 metrics for annual daylight simulation."""

    folder = Inputs.folder(
        description='This folder is an output folder of annual daylight recipe. Folder '
        'should include grids_info.json and sun-up-hours.txt. The command uses the list '
        'in grids_info.json to find the result files for each sensor grid.',
        path='raw_results'
    )

    schedule = Inputs.file(
        description='Path to an annual schedule file. Values should be 0-1 separated '
        'by new line. This should be a daylight hours schedule according to EN 17037.',
        path='schedule.txt'
    )

    @command
    def calculate_annual_metrics_en17037(self):
        return 'honeybee-radiance post-process annual-daylight-en17037 raw_results ' \
            'schedule.txt --sub_folder ../metrics'

    # outputs
    annual_en17037_metrics = Outputs.folder(
        description='Annual EN 17037 metrics folder. This folder includes all the other '
        'subfolders which are also exposed as separate outputs.', path='metrics'
    )

    metrics_info = Outputs.file(
        description='A config file with metrics subfolders information for '
        'visualization. This config file is compatible with honeybee-vtk config.',
        path='metrics/config.json'
    )

    target_illuminance = Outputs.folder(
        description='Target illuminance results.', path='metrics/target_illuminance'
    )

    minimum_illuminance = Outputs.folder(
        description='Minimum illuminance results.', path='metrics/minimum_illuminance'
    )


@dataclass
class LeedIlluminanceCredits(Function):
    """Estimate LEED daylight credits from two point-in-time illuminance folders."""

    folder = Inputs.folder(
        description='Project folder for a LEED illuminance simulation. It should '
        'contain a HBJSON model and two sub-folders of complete point-in-time '
        'illuminance simulations labeled "9AM" and "3PM". These two sub-folders should '
        'each have results folders that include a grids_info.json and .res files with '
        'illuminance values for each sensor. If Meshes are found for the sensor '
        'grids in the HBJSON file, they will be used to compute percentages '
        'of occupied floor area that pass vs. fail. Otherwise, all sensors will '
        'be assumed to represent an equal amount of floor area.',
        path='raw_results'
    )

    glare_control_devices = Inputs.str(
        description='A switch to note whether the model has "view-preserving automatic '
        '(with manual override) glare-control devices," which means that illuminance '
        'only needs to be above 300 lux and not between 300 and 3000 lux.',
        default='glare-control',
        spec={'type': 'string', 'enum': ['glare-control', 'no-glare-control']}
    )

    @command
    def calculate_leed_credits(self):
        return 'honeybee-radiance post-process leed-illuminance raw_results ' \
            '--{{self.glare_control_devices}} --sub-folder ../pass_fail ' \
            '--output-file credit_summary.json'

    # outputs
    pass_fail_results = Outputs.folder(
        description='Pass/Fail results folder. This folder includes results for '
        'each sensor indicating whether they pass or fail the LEED criteria.',
        path='pass_fail'
    )

    credit_summary = Outputs.folder(
        description='JSON file containing the number of LEED credits achieved and '
        'a summary of the percentage of the sensor grid area that meets the criteria.',
        path='credit_summary.json'
    )


@dataclass
class SolarTrackingSynthesis(Function):
    """Synthesize a list of result folders to account for dynamic solar tracking."""

    folder = Inputs.folder(
        description='Results folder containing sub-folders that each represent a state '
        'of the dynamic solar tracking system. Each sub-folder should contain .ill '
        'files for that state and the names of these .ill files should be the '
        'same across all sub-folders.',
        path='raw_results'
    )

    sun_up_hours = Inputs.file(
        description='The .txt file containing the sun-up hours that were simulated.',
        path='sun-up-hours.txt'
    )

    wea = Inputs.file(
        description='The .wea file that was used in the annual irradiance simulation. '
        'This will be used to determine the solar positions.', path='weather.wea'
    )

    north = Inputs.int(
        description='An angle for north direction. Default is 0.',
        default=0, spec={'type': 'integer', 'maximum': 360, 'minimum': 0}
    )

    tracking_increment = Inputs.int(
        description='An integer for the increment angle of each state in degrees.',
        default=5, spec={'type': 'integer', 'maximum': 90, 'minimum': 1}
    )

    @command
    def solar_tracking_synthesis(self):
        return 'honeybee-radiance post-process solar-tracking raw_results ' \
            'sun-up-hours.txt weather.wea --north {{self.north}} ' \
            '--tracking-increment {{self.tracking_increment}} --sub-folder ../final'

    # outputs
    results = Outputs.folder(
        description='Result folder containing synthesized .ill files that correspond '
        'to the tracking behavior.', path='final'
    )


@dataclass
class AnnualGlareAutonomy(Function):
    """Calculate annual glare autonomy for imageless annual glare simulation."""

    folder = Inputs.folder(
        description='This folder is an output folder of imageless annual glare recipe. '
        'Folder should include grids_info.json and sun-up-hours.txt. The command uses '
        'the list in grids_info.json to find the result files for each sensor grid.',
        path='raw_results'
    )

    schedule = Inputs.file(
        description='Path to an annual schedule file. Values should be 0-1 separated '
        'by new line. If not provided an 8-5 annual schedule will be created.',
        path='schedule.txt', optional=True
    )

    glare_threshold = Inputs.float(
        description='A fractional number for the threshold of DGP above which '
        'conditions are considered to induce glare. This value is used when '
        'calculating glare autonomy (the fraction of hours in which the view is free '
        'of glare). Common values are 0.35 (Perceptible Glare), 0.4 (Disturbing '
        'Glare), and 0.45 (Intolerable Glare).', default=0.4,
        spec={'type': 'number', 'minimum': 0, 'maximum': 1}
    )

    @command
    def calculate_annual_glare_autonomy(self):
        return 'honeybee-radiance post-process annual-glare raw_results ' \
            '--schedule schedule.txt --glare-threshold {{self.glare_threshold}} ' \
            '--sub_folder ../metrics'

    # outputs
    annual_metrics = Outputs.folder(
        description='Annual metrics folder. This folder includes all the other '
        'subfolders which are also exposed as separate outputs.', path='metrics'
    )

    metrics_info = Outputs.file(
        description='A config file with metrics subfolders information for '
        'visualization. This config file is compatible with honeybee-vtk config.',
        path='metrics/config.json'
    )

    glare_autonomy = Outputs.folder(
        description='Glare autonomy results.', path='metrics/ga'
    )


@dataclass
class DaylightFactorVisMetadata(Function):
    """Create a visualization metadata file for daylight factor."""

    @command
    def create_daylight_factor_vis_data(self):
        return 'honeybee-radiance post-process daylight-factor-vis-metadata ' \
            '--output-file vis_metadata.json'

    # outputs
    cfg_file = Outputs.file(
        description='Output visualization metadata file.', path='vis_metadata.json')


@dataclass
class DaylightFactorConfig(Function):
    """Create a config file for daylight factor results."""

    folder = Inputs.str(
        description='Name of the results folder.', path='daylight-factor'
    )

    @command
    def create_daylight_factor_config(self):
        return 'honeybee-radiance post-process daylight-factor-config ' \
            '-o config.json -f "{{self.folder}}"'

    # outputs
    cfg_file = Outputs.file(description='Output config file.', path='config.json')


@dataclass
class PointInTimeVisMetadata(Function):
    """Create a visualization metadata file for point-in-time."""

    metric = Inputs.str(
        description='Text for the type of metric to be output from the calculation. '
        'Choose from: illuminance, irradiance, luminance, radiance.',
        default='illuminance',
        spec={'type': 'string',
              'enum': ['illuminance', 'irradiance', 'luminance', 'radiance']}
    )

    @command
    def create_point_in_time_vis_data(self):
        return 'honeybee-radiance post-process point-in-time-vis-metadata ' \
            '--metric {{self.metric}} --output-file vis_metadata.json'

    # outputs
    cfg_file = Outputs.file(
        description='Output visualization metadata file.', path='vis_metadata.json')


@dataclass
class PointInTimeConfig(Function):
    """Create a config file for point-in-time results."""

    folder = Inputs.str(
        description='Name of the results folder.', path='point-in-time'
    )

    metric = Inputs.str(
        description='Text for the type of metric to be output from the calculation. '
        'Choose from: illuminance, irradiance, luminance, radiance.',
        default='illuminance',
        spec={'type': 'string',
              'enum': ['illuminance', 'irradiance', 'luminance', 'radiance']}
    )

    @command
    def create_point_in_time_config(self):
        return 'honeybee-radiance post-process point-in-time-config ' \
            '-o config.json -f "{{self.folder}}" --metric {{self.metric}}'

    # outputs
    cfg_file = Outputs.file(description='Output config file.', path='config.json')


@dataclass
class CumulativeRadiationVisMetadata(Function):
    """Create a visualization metadata file for cumulative radiation."""

    @command
    def create_cumulative_radiation_vis_data(self):
        return 'honeybee-radiance post-process cumulative-radiation-vis-metadata ' \
            '--output-file vis_metadata.json'

    # outputs
    cfg_file = Outputs.file(
        description='Output visualization metadata file.', path='vis_metadata.json')


@dataclass
class AverageIrradianceVisMetadata(Function):
    """Create a visualization metadata file for average irradiance."""

    @command
    def create_average_irradiance_vis_data(self):
        return 'honeybee-radiance post-process average-irradiance-vis-metadata ' \
            '--output-file vis_metadata.json'

    # outputs
    cfg_file = Outputs.file(
        description='Output visualization metadata file.', path='vis_metadata.json')


@dataclass
class CumulativeRadiationConfig(Function):
    """Create a config file for cumulative-radiation results."""

    @command
    def create_point_in_time_config(self):
        return 'honeybee-radiance post-process cumulative-radiation-config ' \
            '-o config.json'

    # outputs
    cfg_file = Outputs.file(description='Output config file.', path='config.json')


@dataclass
class DirectSunHoursVisMetadata(Function):
    """Create a visualization metadata file for direct sun hours."""

    @command
    def direct_sun_hours_vis_data(self):
        return 'honeybee-radiance post-process direct-sun-hours-vis-metadata ' \
            '--output-file vis_metadata.json'

    # outputs
    cfg_file = Outputs.file(
        description='Output visualization metadata file.', path='vis_metadata.json')


@dataclass
class DirectSunHoursConfig(Function):
    """Create a config file for direct-sun-hours results."""

    folder = Inputs.str(
        description='Name of the results folder.', path='direct-sun-hours'
    )

    @command
    def create_point_in_time_config(self):
        return 'honeybee-radiance post-process direct-sun-hours-config ' \
            '-o config.json -f "{{self.folder}}"'

    # outputs
    cfg_file = Outputs.file(description='Output config file.', path='config.json')


@dataclass
class SkyViewVisMetadata(Function):
    """Create a visualization metadata file for sky view."""

    @command
    def create_sky_view_vis_data(self):
        return 'honeybee-radiance post-process sky-view-vis-metadata ' \
            '--output-file vis_metadata.json'

    # outputs
    cfg_file = Outputs.file(
        description='Output visualization metadata file.', path='vis_metadata.json')


@dataclass
class SkyViewConfig(Function):
    """Create a config file for sky-view results."""

    folder = Inputs.str(
        description='Name of the results folder.', path='sky-view'
    )

    @command
    def create_point_in_time_config(self):
        return 'honeybee-radiance post-process sky-view-config ' \
            '-o config.json -f "{{self.folder}}"'

    # outputs
    cfg_file = Outputs.file(description='Output config file.', path='config.json')


@dataclass
class ImagelessAnnualGlareVisMetadata(Function):
    """Create a visualization metadata file for imageless annual glare."""

    @command
    def create_imageless_annual_glare_vis_data(self):
        return 'honeybee-radiance post-process imageless-annual-glare-vis-metadata ' \
            '--output-file vis_metadata.json'

    # outputs
    cfg_file = Outputs.file(
        description='Output visualization metadata file.', path='vis_metadata.json')


@dataclass
class LeedDaylightOptionTwoVisMetadata(Function):
    """Create five visualization metadata files for LEED Daylight Option Two."""

    output_folder = Inputs.str(
        description='Name of the output folder.', default='visualization',
        path='visualization'
    )

    @command
    def create_leed_daylight_option_two_vis_data(self):
        return 'honeybee-radiance post-process leed-daylight-option-two-vis-metadata ' \
            '--output-folder "{{self.output_folder}}"'

    # outputs
    vis_metadata_folder = Outputs.folder(
        description='Output folder with visualization metadata files.',
        path='visualization'
    )


@dataclass
class AbntNbr15575DaylightVisMetadata(Function):
    """Create four visualization metadata files for ABNT NBR 15575."""

    output_folder = Inputs.str(
        description='Name of the output folder.', default='visualization',
        path='visualization'
    )

    @command
    def create_abnt_nbr_15575_daylight_vis_data(self):
        return 'honeybee-radiance post-process abnt-nbr-15575-daylight-vis-metadata ' \
            '--output-folder "{{self.output_folder}}"'

    # outputs
    vis_metadata_folder = Outputs.folder(
        description='Output folder with visualization metadata files.',
        path='visualization'
    )
