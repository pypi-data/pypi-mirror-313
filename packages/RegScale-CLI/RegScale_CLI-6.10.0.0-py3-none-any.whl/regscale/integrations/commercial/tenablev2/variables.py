#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Tenable Variables """

from regscale.core.app.utils.variables import RsVariableType, RsVariablesMeta


class TenableVariables(metaclass=RsVariablesMeta):
    """
    Tenable Variables class to define class-level attributes with type annotations and examples
    """

    # Define class-level attributes with type annotations and examples
    tenableAccessKey: RsVariableType(str, "xxxxxxxxxxxxxxxxxxxxxx", sensitive=True)  # type: ignore # noqa: F722,F821
    tenableSecretKey: RsVariableType(str, "xxxxxxxxxxxxxxxxxxxxxx", sensitive=True)  # type: ignore # noqa: F722,F821
    tenableUrl: RsVariableType(str, "https://cloud.tenable.com")  # type: ignore # noqa: F722,F821
    tenableMinimumSeverityFilter: RsVariableType(str, "critical")  # type: ignore # noqa: F722,F821
