"""A module for 🪄🧙 magic 🪄🧙"""
# All IPython-dependent code should be in this folder

# ruff: noqa: F401

import pandas

from .._udf.context import context
from .output import output

try:
    import IPython

    from .magics import load_ipython_extension

    ipython = IPython.get_ipython()

    if ipython is None:
        raise ImportError("Not running inside IPython.")

    # automatically load the %%fused magic into the environment
    # This takes the place of %load_ext fused
    load_ipython_extension(ipython)
except ImportError:
    pass  # Not in IPython

# We set pandas' 2.0 copy_on_write to ON by default to avoid pesky
# SettingWithCopyWarningErrors
pandas.options.mode.copy_on_write = True
