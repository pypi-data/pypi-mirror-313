"""
Helper module to get package version.
"""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version('empty-decorator')
except PackageNotFoundError:
    __version__ = '0.0.0 (source)'
