"""Tests for mcpdoc_split imports."""


def test_imports():
    """Test that main modules can be imported."""
    from mcpdoc_split import main  # noqa
    from mcpdoc_split import cli  # noqa
    from mcpdoc_split import _version  # noqa

    assert True


def test_version_import():
    """Test that version can be imported."""
    from mcpdoc_split import __version__

    # Version should be a string
    assert isinstance(__version__, str)
