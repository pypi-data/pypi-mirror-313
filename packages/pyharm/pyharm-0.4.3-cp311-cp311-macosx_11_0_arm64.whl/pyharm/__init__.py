"""
PyHarm is a Python wrapper for CHarm.
"""


import os as _os
from ._lib import _load_lib

# Name of the shared CHarm library to load
_libcharmname = 'libcharm'

# Directory of "_libcharmname"
_libcharmdir = _os.path.join(_os.path.dirname(__file__), '')

# Load the shared CHarm library
_libcharm = _load_lib(_libcharmdir, _libcharmname)

# Prefix to be added to the CHarm function names.  Depends on the format of
# floating point numbers used to compile CHarm (single or double precision).
_CHARM = 'charm_'

# Prefix to be added to the PyHarm functions when calling "__repr__" methods
_pyharm = 'pyharm'

# The "err" module is intentionally not imported, as users do not interact with
# it in PyHarm.
from . import crd, glob, integ, leg, misc, sha, shc, shs
__all__ = ['crd', 'glob', 'integ', 'leg', 'misc', 'sha', 'shc', 'shs']

