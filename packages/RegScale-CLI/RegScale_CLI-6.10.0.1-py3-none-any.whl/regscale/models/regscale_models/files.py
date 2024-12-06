#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" [Deprecated] Model for Files in the application """

import warnings
from .file import File  # Import everything from the new module

# Issue a deprecation warning
warnings.warn(
    "The module 'files' is deprecated and will be removed in future versions. Use 'file' instead.",
    DeprecationWarning,
    stacklevel=2,
)
