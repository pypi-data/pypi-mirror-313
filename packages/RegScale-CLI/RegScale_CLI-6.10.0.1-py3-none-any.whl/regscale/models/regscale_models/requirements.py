#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" [Deprecated] Model for Requirements in the application """

import warnings
from .requirement import Requirement  # Import everything from the new module

# Issue a deprecation warning
warnings.warn(
    "The module 'requirements' is deprecated and will be removed in future versions. Use 'requirement' instead.",
    DeprecationWarning,
    stacklevel=2,
)
