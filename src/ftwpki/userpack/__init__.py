"""
FTW-PKI userpack Tool.

"""
# DOC - 
from importlib.metadata import PackageNotFoundError, version

try:  
    __version__ = version("ftw-pki-unpacker")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
