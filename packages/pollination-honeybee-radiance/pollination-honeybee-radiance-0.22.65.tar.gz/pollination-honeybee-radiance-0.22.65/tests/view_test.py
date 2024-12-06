from pollination.honeybee_radiance.view import SplitViewCount, SplitView, MergeImages
from queenbee.plugin.function import Function


def test_split_view_count():
    function = SplitViewCount().queenbee
    assert function.name == 'split-view-count'
    assert isinstance(function, Function)


def test_split_view():
    function = SplitView().queenbee
    assert function.name == 'split-view'
    assert isinstance(function, Function)


def test_merge_images():
    function = MergeImages().queenbee
    assert function.name == 'merge-images'
    assert isinstance(function, Function)
