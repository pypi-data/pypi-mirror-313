#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" [Deprecated] Model for Components in the application """

import warnings
from .component import Component  # Import everything from the new module

# Issue a deprecation warning
warnings.warn(
    "The module 'components' is deprecated and will be removed in future versions. Use 'component' instead.",
    DeprecationWarning,
    stacklevel=2,
)
