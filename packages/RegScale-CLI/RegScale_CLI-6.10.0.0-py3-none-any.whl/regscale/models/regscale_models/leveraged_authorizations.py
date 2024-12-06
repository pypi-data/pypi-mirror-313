#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" [Deprecated] Model for Leveraged Authorizations in the application """

import warnings
from .leveraged_authorization import (
    LeveragedAuthorization as LeveragedAuthorizations,
)  # Import everything from the new module

# Issue a deprecation warning
warnings.warn(
    "The module 'leveraged_authorizations' is deprecated and will be removed in future versions. "
    "Use 'leveraged_authorization' instead.",
    DeprecationWarning,
    stacklevel=2,
)
