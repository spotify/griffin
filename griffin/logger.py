# -*- coding: utf-8 -*-
# Copyright (c) 2015 Spotify AB

from __future__ import absolute_import, division, print_function


import logging


# TODO: colorize logs
class ColorLogFormat(logging.Formatter):
    pass


def configure_log(quiet):
    """
    If `-q | --quiet` is passed into the command line, set logger
    to only return warnings and higher.  Otherwise, set logger level to
    info and higher.
    """
    logger = logging.getLogger('griffin')
    sh = logging.StreamHandler()
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    sh.setFormatter(formatter)
    logger.addHandler(sh)
    if quiet:
        logger.setLevel(logging.WARNING)
    else:
        logger.setLevel(logging.INFO)
