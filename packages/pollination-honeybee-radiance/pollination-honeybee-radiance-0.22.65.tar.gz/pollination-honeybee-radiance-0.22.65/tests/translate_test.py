from pollination.honeybee_radiance.translate import CreateRadianceFolderGrid, \
    CreateRadianceFolderView, CreateRadiantEnclosureInfo, CreateRadianceFolder

from queenbee.plugin.function import Function


def test_create_radiance_folder():
    function = CreateRadianceFolder().queenbee
    assert function.name == 'create-radiance-folder'
    assert isinstance(function, Function)


def test_create_radiance_folder_grid():
    function = CreateRadianceFolderGrid().queenbee
    assert function.name == 'create-radiance-folder-grid'
    assert isinstance(function, Function)


def test_create_radiance_folder_view():
    function = CreateRadianceFolderView().queenbee
    assert function.name == 'create-radiance-folder-view'
    assert isinstance(function, Function)


def test_create_radiant_enclosure_info():
    function = CreateRadiantEnclosureInfo().queenbee
    assert function.name == 'create-radiant-enclosure-info'
    assert isinstance(function, Function)
