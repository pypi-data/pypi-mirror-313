#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" [Deprecated] Model for Security Plan in the application """

import warnings
from .security_plan import SecurityPlan  # Import everything from the new module

# Issue a deprecation warning
warnings.warn(
    "The module 'securityplans' is deprecated and will be removed in future versions. Use 'security_plan' instead.",
    DeprecationWarning,
    stacklevel=2,
)
