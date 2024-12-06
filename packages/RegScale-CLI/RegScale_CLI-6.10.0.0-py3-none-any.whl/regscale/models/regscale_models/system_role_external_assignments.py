#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" [Deprecated] Model for System Role External Assignments in the application """

import warnings
from .system_role_external_assignment import (
    SystemRoleExternalAssignment as SystemRoleExternalAssignments,
)  # Import everything from the new module

# Issue a deprecation warning
warnings.warn(
    "The module 'system_role_external_assignments' is deprecated and will be removed in future versions. "
    "Use 'system_role_external_assignment' instead.",
    DeprecationWarning,
    stacklevel=2,
)
