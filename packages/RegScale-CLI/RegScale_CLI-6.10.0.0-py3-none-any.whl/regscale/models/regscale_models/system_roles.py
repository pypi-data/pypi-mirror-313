#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" [Deprecated] Model for System Roles in the application """

import warnings
from .system_role import (
    SystemRole as SystemRoles,
)  # Import everything from the new module

# Issue a deprecation warning
warnings.warn(
    "The module 'system_roles' is deprecated and will be removed in future versions. Use 'system_role' instead.",
    DeprecationWarning,
    stacklevel=2,
)
