#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" [Deprecated] Model for Risks in the application """

import warnings
from .risk import Risk as Risks  # Import everything from the new module

# Issue a deprecation warning
warnings.warn(
    "The module 'risks' is deprecated and will be removed in future versions. Use 'risk' instead.",
    DeprecationWarning,
    stacklevel=2,
)
