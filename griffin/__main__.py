#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2015 Spotify AB

from __future__ import absolute_import, division, print_function

import click

from .cli import build as b
from .config import setup_config
from .logger import configure_log


@click.group()
def main():
    """The main interface"""


@main.command(help="Build documentation given a RAML file.")
@click.option("-r", "--ramlfile",
              type=click.Path(dir_okay=False,
                              exists=True,
                              resolve_path=True,
                              readable=True),
              default=".")
@click.option("-o", "--output",
              type=click.Path(file_okay=False,
                              resolve_path=True,
                              writable=True,
                              exists=False))
@click.option("-c", "--config",
              type=click.Path(exists=True,
                              dir_okay=False,
                              readable=True,
                              resolve_path=True),
              default="griffin.yaml")
@click.option("-R", "--ramlconfig",
              type=click.Path(exists=True,
                              dir_okay=False,
                              readable=True,
                              resolve_path=True))
@click.option("-q", "--quiet", is_flag=True)
def build(ramlfile, output, config, ramlconfig, quiet):
    """Builds documentation off of a given RAML file."""
    conf = setup_config(config)
    configure_log(quiet)
    b(ramlfile, conf, output, ramlconfig)
