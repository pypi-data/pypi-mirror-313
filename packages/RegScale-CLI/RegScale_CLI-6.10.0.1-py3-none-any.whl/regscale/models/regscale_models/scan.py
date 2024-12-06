#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" [Deprecated] Model for ScanHistory in the application """

import warnings
from .scan_history import Scan  # type: ignore # Import everything from the new module

# Issue a deprecation warning
warnings.warn(
    "The module 'Scan' is deprecated and will be removed in future versions. Use 'ScanHistory' instead.",
    DeprecationWarning,
    stacklevel=2,
)
