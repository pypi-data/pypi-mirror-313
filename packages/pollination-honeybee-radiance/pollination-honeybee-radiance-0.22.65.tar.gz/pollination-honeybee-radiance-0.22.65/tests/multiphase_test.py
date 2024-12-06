from pathlib import Path
from shutil import rmtree

from pollination.honeybee_radiance.multiphase import ViewMatrix, FluxTransfer, \
    AddApertureGroupBlinds
from queenbee.plugin.function import Function


def test_view_mtx():
    function = ViewMatrix().queenbee
    assert function.name == 'view-matrix'
    assert isinstance(function, Function)


def test_flux_transfer():
    function = FluxTransfer().queenbee
    assert function.name == 'flux-transfer'
    assert isinstance(function, Function)


def test_add_aperture_group_blinds():
    function = AddApertureGroupBlinds()
    model = './tests/assets/model/sample_model_grid_aperture_groups.hbjson'
    inputs = {
        'model': model
    }
    folder = Path('./tests/assets/temp')
    output = folder.joinpath('model_blinds.hbjson')
    if not folder.exists():
        folder.mkdir(parents=True)
    function._try(inputs=inputs, folder=folder)
    assert output.exists()

    for path in folder.glob('*'):
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            rmtree(path)
