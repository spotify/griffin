# -*- coding: utf-8 -*-
# Copyright (c) 2015 Spotify AB

from __future__ import absolute_import, division, print_function

from six import iteritems, iterkeys
import yaml


class DocConfigError(Exception):
    pass


DEFAULT_CONFIG = {
    "theme_path": None,
    "template_dir": "templates",
    "static_dir": "assets",
    "endpoint_order": "preserve",
    "base_url": "http://localhost:8080",
    "theme_name": "default",
    "title": "MISSING",
    "description": "MISSING",
    "author": "MISSING",
    "canonical_url": "MISSING",
    "favicon": "images/default.png",
    "brand_image": "images/default.png",
    "output_dir": "output"
}


def _set_defaults(config):
    """Add defaults where custom isn't set"""
    for k, v in iteritems(DEFAULT_CONFIG):
        if k not in iterkeys(config):
            config[k] = v
        if config[k] is None:
            config[k] = v
    return config


def setup_config(config_file):
    with open(config_file) as c:
        config = yaml.load(c)

    config = _set_defaults(config)
    return config
