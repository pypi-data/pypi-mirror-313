"""
PyHarm is a Python wrapper for CHarm.
"""


# start delvewheel patch
def _delvewheel_patch_1_9_0():
    import os
    if os.path.isdir(libs_dir := os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'pyharm.libs'))):
        os.add_dll_directory(libs_dir)


_delvewheel_patch_1_9_0()
del _delvewheel_patch_1_9_0
# end delvewheel patch

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
