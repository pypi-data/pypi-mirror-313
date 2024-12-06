from pathlib import Path

from ladybug.futil import nukedir
from pollination.honeybee_radiance.post_process import ConvertToBinary, SumRow, \
    AnnualIrradianceMetrics, AnnualDaylightMetrics, LeedIlluminanceCredits, \
    SolarTrackingSynthesis, DaylightFactorConfig, DaylightFactorVisMetadata, \
    ImagelessAnnualGlareVisMetadata, PointInTimeVisMetadata, \
    CumulativeRadiationVisMetadata, AverageIrradianceVisMetadata, \
    SkyViewVisMetadata

from queenbee.plugin.function import Function


def test_convert_to_binary():
    function = ConvertToBinary().queenbee
    assert function.name == 'convert-to-binary'
    assert isinstance(function, Function)


def test_sum_row():
    function = SumRow().queenbee
    assert function.name == 'sum-row'
    assert isinstance(function, Function)


def test_annual_irradiance_metrics():
    function = AnnualIrradianceMetrics().queenbee
    assert function.name == 'annual-irradiance-metrics'
    assert isinstance(function, Function)


def test_annual_daylight_metrics():
    function = AnnualDaylightMetrics().queenbee
    assert function.name == 'annual-daylight-metrics'
    assert isinstance(function, Function)


def test_leed_illuminance_credits():
    function = LeedIlluminanceCredits().queenbee
    assert function.name == 'leed-illuminance-credits'
    assert isinstance(function, Function)


def test_solar_tracking_synthesis():
    function = SolarTrackingSynthesis().queenbee
    assert function.name == 'solar-tracking-synthesis'
    assert isinstance(function, Function)


def test_daylight_factor_config():
    function = DaylightFactorConfig().queenbee
    assert function.name == 'daylight-factor-config'
    assert isinstance(function, Function)


def test_daylight_factor_vis_metadata():
    function = DaylightFactorVisMetadata()
    qb_function = function.queenbee
    assert qb_function.name == 'daylight-factor-vis-metadata'
    assert isinstance(qb_function, Function)

    inputs = {}  # inputs is empty for this function
    folder = Path('./tests/assets/temp')
    if not folder.exists():
        folder.mkdir(parents=True)
    output_file = folder.joinpath('vis_metadata.json')
    function._try(inputs, folder=folder)
    assert output_file.is_file()

    nukedir(folder)


def test_imageless_annual_glare_vis_metadata():
    function = ImagelessAnnualGlareVisMetadata()
    qb_function = function.queenbee
    assert qb_function.name == 'imageless-annual-glare-vis-metadata'
    assert isinstance(qb_function, Function)

    inputs = {}  # inputs is empty for this function
    folder = Path('./tests/assets/temp')
    if not folder.exists():
        folder.mkdir(parents=True)
    output_file = folder.joinpath('vis_metadata.json')
    function._try(inputs, folder=folder)
    assert output_file.is_file()

    nukedir(folder)


def test_point_in_time_vis_metadata():
    function = PointInTimeVisMetadata()
    qb_function = function.queenbee
    assert qb_function.name == 'point-in-time-vis-metadata'
    assert isinstance(qb_function, Function)

    inputs = {'metric': 'illuminance'}
    folder = Path('./tests/assets/temp')
    if not folder.exists():
        folder.mkdir(parents=True)
    output_file = folder.joinpath('vis_metadata.json')
    function._try(inputs, folder=folder)
    assert output_file.is_file()

    nukedir(folder)


def test_cumulative_radiation_vis_metadata():
    function = CumulativeRadiationVisMetadata()
    qb_function = function.queenbee
    assert qb_function.name == 'cumulative-radiation-vis-metadata'
    assert isinstance(qb_function, Function)

    inputs = {}  # inputs is empty for this function
    folder = Path('./tests/assets/temp')
    if not folder.exists():
        folder.mkdir(parents=True)
    output_file = folder.joinpath('vis_metadata.json')
    function._try(inputs, folder=folder)
    assert output_file.is_file()

    nukedir(folder)


def test_average_irradiance_vis_metadata():
    function = AverageIrradianceVisMetadata()
    qb_function = function.queenbee
    assert qb_function.name == 'average-irradiance-vis-metadata'
    assert isinstance(qb_function, Function)

    inputs = {}  # inputs is empty for this function
    folder = Path('./tests/assets/temp')
    if not folder.exists():
        folder.mkdir(parents=True)
    output_file = folder.joinpath('vis_metadata.json')
    function._try(inputs, folder=folder)
    assert output_file.is_file()

    nukedir(folder)


def test_sky_view_vis_metadata():
    function = SkyViewVisMetadata()
    qb_function = function.queenbee
    assert qb_function.name == 'sky-view-vis-metadata'
    assert isinstance(qb_function, Function)

    inputs = {}  # inputs is empty for this function
    folder = Path('./tests/assets/temp')
    if not folder.exists():
        folder.mkdir(parents=True)
    output_file = folder.joinpath('vis_metadata.json')
    function._try(inputs, folder=folder)
    assert output_file.is_file()

    nukedir(folder)
