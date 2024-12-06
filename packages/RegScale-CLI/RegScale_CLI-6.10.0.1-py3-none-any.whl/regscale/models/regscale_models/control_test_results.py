#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" [Deprecated] Model for Control Test Results in the application """

import warnings
from .control_test_result import (
    ControlTestResult as ControlTestResults,
)  # Import everything from the new module

# Issue a deprecation warning
warnings.warn(
    "The module 'control_test_results' is deprecated and will be removed in future versions. "
    "Use 'control_test_result' instead.",
    DeprecationWarning,
    stacklevel=2,
)
