#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" [Deprecated] Model for Custom Fields in the application """

import warnings
from .custom_field import (
    CustomFieldsData,
    CustomField as CustomFields,
    CustomFieldsSelectItem as CustomFieldsSelectItems,
)  # Import everything from the new module

# Issue a deprecation warning
warnings.warn(
    "The module 'custom_fields' is deprecated and will be removed in future versions. Use 'custom_field' instead.",
    DeprecationWarning,
    stacklevel=2,
)
