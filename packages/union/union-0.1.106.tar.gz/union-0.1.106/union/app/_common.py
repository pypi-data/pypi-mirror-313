from contextlib import contextmanager

from flytekit.image_spec import default_builder

from union.ucimage import _image_builder


def _return_empty_str():
    return ""


@contextmanager
def patch_get_flytekit_for_pypi():
    """Mock out get_flytekit_for_pypi to return an empty string."""
    try:
        orig_get_flytekit_for_pypi = default_builder.get_flytekit_for_pypi
        default_builder.get_flytekit_for_pypi = _return_empty_str
        yield
        default_builder.get_flytekit_for_pypi = orig_get_flytekit_for_pypi
    except AttributeError:
        # Catch this error just in case `flytekit` changes the location of
        # get_flytekit_for_pypi
        yield


@contextmanager
def patch_get_unionai_for_pypi():
    """Mock out get_unionai_for_pypi to return an empty string."""
    orig_get_unionai_for_pypi = _image_builder.get_unionai_for_pypi
    _image_builder.get_unionai_for_pypi = _return_empty_str
    yield
    _image_builder.get_unionai_for_pypi = orig_get_unionai_for_pypi
