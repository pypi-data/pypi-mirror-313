from pollination.honeybee_radiance.octree import CreateOctree, \
    CreateOctreeWithSky, CreateOctreeAbstractedGroups, \
    CreateOctreeShadeTransmittance, CreateOctreeStatic, \
    CreateOctreeWithSkyStatic
from queenbee.plugin.function import Function


def test_create_octree():
    function = CreateOctree().queenbee
    assert function.name == 'create-octree'
    assert isinstance(function, Function)


def test_create_octree_with_sky():
    function = CreateOctreeWithSky().queenbee
    assert function.name == 'create-octree-with-sky'
    assert isinstance(function, Function)


def test_create_octree_abstracted_groups():
    function = CreateOctreeAbstractedGroups().queenbee
    assert function.name == 'create-octree-abstracted-groups'
    assert isinstance(function, Function)


def test_create_octree_shade_transmittance():
    function = CreateOctreeShadeTransmittance().queenbee
    assert function.name == 'create-octree-shade-transmittance'
    assert isinstance(function, Function)


def test_create_octree_static():
    function = CreateOctreeStatic().queenbee
    assert function.name == 'create-octree-static'
    assert isinstance(function, Function)


def test_create_octree_with_sky_static():
    function = CreateOctreeWithSkyStatic().queenbee
    assert function.name == 'create-octree-with-sky-static'
    assert isinstance(function, Function)
