#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" [Deprecated] Model for Control Test Plan in the application """

import warnings
from .control_test_plan import ControlTestPlan  # Import everything from the new module

# Issue a deprecation warning
warnings.warn(
    "The module 'control_testplan' is deprecated and will be removed in future versions. "
    "Use 'control_test_plan' instead.",
    DeprecationWarning,
    stacklevel=2,
)
