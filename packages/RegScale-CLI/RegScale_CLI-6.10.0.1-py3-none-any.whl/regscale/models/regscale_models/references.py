#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" [Deprecated] Model for References in the application """

import warnings
from .reference import Reference as References  # Import everything from the new module

# Issue a deprecation warning
warnings.warn(
    "The module 'references' is deprecated and will be removed in future versions. Use 'reference' instead.",
    DeprecationWarning,
    stacklevel=2,
)
