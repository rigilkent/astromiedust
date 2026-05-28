"""Compatibility layer for the old ``astrodust_optprops`` package name."""

from warnings import warn

warn(
    "astrodust_optprops has been renamed to astromiedust; "
    "please import astromiedust instead.",
    DeprecationWarning,
    stacklevel=2,
)

from astromiedust import *  # noqa: F401,F403
from astromiedust import utils  # noqa: F401
