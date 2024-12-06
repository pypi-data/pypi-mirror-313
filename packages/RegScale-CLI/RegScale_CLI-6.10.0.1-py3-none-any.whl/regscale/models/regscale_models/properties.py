#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" [Deprecated] Model for Properties in the application """

import warnings
from .property import Property as Properties  # Import everything from the new module

# Issue a deprecation warning
warnings.warn(
    "The module 'properties' is deprecated and will be removed in future versions. Use 'property' instead.",
    DeprecationWarning,
    stacklevel=2,
)
