from pathlib import Path

from ladybug.futil import nukedir

from pollination.honeybee_radiance.study import StudyInfo
from queenbee.plugin.function import Function


def test_study_info_function():
    function = StudyInfo().queenbee
    assert function.name == 'study-info'
    assert isinstance(function, Function)


def test_study_info_wea():
    function = StudyInfo()
    inputs = {
        'wea': './tests/assets/study-info/wea.wea',
        'timestep': 1
    }
    folder = Path('./tests/assets/temp')
    if not folder.exists():
        folder.mkdir(parents=True)
    output = folder.joinpath('study_info.json')
    function._try(inputs=inputs, folder=folder)
    assert output.exists()
    nukedir(folder)


def test_study_info_epw():
    function = StudyInfo()
    inputs = {
        'wea': './tests/assets/study-info/sky.epw',
        'timestep': 1
    }
    folder = Path('./tests/assets/temp')
    if not folder.exists():
        folder.mkdir(parents=True)
    output = folder.joinpath('study_info.json')
    function._try(inputs=inputs, folder=folder)
    assert output.exists()
    nukedir(folder)


def test_study_info_timestep_2():
    function = StudyInfo()
    inputs = {
        'wea': './tests/assets/wea/Boston-Logan Intl AP_0_8759_t2.wea',
        'timestep': 2
    }
    folder = Path('./tests/assets/temp')
    if not folder.exists():
        folder.mkdir(parents=True)
    output = folder.joinpath('study_info.json')
    function._try(inputs=inputs, folder=folder)
    assert output.exists()
    nukedir(folder)


def test_study_info_timestep_3():
    function = StudyInfo()
    inputs = {
        'wea': './tests/assets/wea/Boston-Logan Intl AP_0_8759_t3.wea',
        'timestep': 3
    }
    folder = Path('./tests/assets/temp')
    if not folder.exists():
        folder.mkdir(parents=True)
    output = folder.joinpath('study_info.json')
    function._try(inputs=inputs, folder=folder)
    assert output.exists()
    nukedir(folder)
