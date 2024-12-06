# ruff: noqa: E402
"""
.. include:: ../README.md
"""

try:
    from tcloud._version import __version__ as __version__, __version_tuple__ as __version_tuple__  # type: ignore
except ImportError:
    pass
