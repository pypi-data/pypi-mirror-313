from pathlib import Path
from shutil import rmtree

from pollination.honeybee_radiance.grid import SplitGrid, MergeFiles, \
    SplitGridFolder, MergeFolderData, MirrorGrid, RadiantEnclosureInfo
from queenbee.plugin.function import Function


def test_split_grid_function():
    function = SplitGrid().queenbee
    assert function.name == 'split-grid'
    assert isinstance(function, Function)


def test_split_grid():
    function = SplitGrid()
    inputs = {
        'input_grid': './tests/assets/grid/sensor_grid_split.pts',
        'sensor_count': 5
    }
    folder = Path('./tests/assets/temp')
    output_folder = folder.joinpath('output')
    if not folder.exists():
        folder.mkdir(parents=True)
    function._try(inputs=inputs, folder=folder)
    assert output_folder.is_dir()

    for path in folder.glob('*'):
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            rmtree(path)


def test_merge_files_function():
    function = MergeFiles().queenbee
    assert function.name == 'merge-files'
    assert isinstance(function, Function)


def test_merge_files():
    function = MergeFiles()
    input_folder = './tests/assets/grid'
    inputs = {
        'extension': '.ill',
        'folder': input_folder
    }
    folder = Path('./tests/assets/temp')
    output = folder.joinpath('grid.ill')
    if not folder.exists():
        folder.mkdir(parents=True)
    function._try(inputs=inputs, folder=folder)
    assert output.exists()

    for path in folder.glob('*'):
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            rmtree(path)


def test_split_folder():
    function = SplitGridFolder().queenbee
    assert function.name == 'split-grid-folder'
    assert isinstance(function, Function)


def test_merge_folder():
    function = MergeFolderData().queenbee
    assert function.name == 'merge-folder-data'
    assert isinstance(function, Function)


def test_mirror_grid():
    function = MirrorGrid().queenbee
    assert function.name == 'mirror-grid'
    assert isinstance(function, Function)


def test_radiant_enclosure_info():
    function = RadiantEnclosureInfo().queenbee
    assert function.name == 'radiant-enclosure-info'
    assert isinstance(function, Function)
