#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" [Deprecated] Model for StakeHolders in the application """

import warnings
from .stake_holder import (
    StakeHolder as StakeHolders,
)  # Import everything from the new module

# Issue a deprecation warning
warnings.warn(
    "The module 'stakeholders' is deprecated and will be removed in future versions. Use 'stake_holder' instead.",
    DeprecationWarning,
    stacklevel=2,
)
