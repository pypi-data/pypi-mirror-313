#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" [Deprecated] Model for Catalog in the application """

import warnings
from .catalog import Catalog  # Import everything from the new module

# Issue a deprecation warning
warnings.warn(
    "The module 'calatlog' is deprecated and will be removed in future versions. Use 'catalog' instead.",
    DeprecationWarning,
    stacklevel=2,
)
