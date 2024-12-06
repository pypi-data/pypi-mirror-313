#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" RegScale Azure Package """

import click
from .intune import intune


@click.group()
def azure():
    """Azure Integrations"""


azure.add_command(intune)
