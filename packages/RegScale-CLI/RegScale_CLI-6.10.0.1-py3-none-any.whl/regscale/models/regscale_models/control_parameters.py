#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" [Deprecated] Model for Control Parameters in the application """

import warnings
from .control_parameter import ControlParameter  # Import everything from the new module

# Issue a deprecation warning
warnings.warn(
    "The module 'control_parameters' is deprecated and will be removed in future versions. "
    "Use 'control_parameter' instead.",
    DeprecationWarning,
    stacklevel=2,
)
