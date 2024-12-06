#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" [Deprecated] Model for Ports Protocols in the application """

import warnings
from .ports_protocol import (
    PortsProtocol as PortsProtocols,
)  # Import everything from the new module

# Issue a deprecation warning
warnings.warn(
    "The module 'ports_protocols' is deprecated and will be removed in future versions. "
    "Use 'ports_protocol' instead.",
    DeprecationWarning,
    stacklevel=2,
)
