# -*- coding: utf-8 -*-
# Copyright (c) 2015 Spotify AB

from __future__ import absolute_import, division, print_function

import os

import pytest

from griffin.cli import build
from griffin.config import setup_config
from .base import EXAMPLES, CONFIG


@pytest.fixture(scope="session")
def raml():
    return os.path.join(EXAMPLES, "spotify.raml")


@pytest.fixture(scope="session")
def config():
    return setup_config(os.path.join(CONFIG, "simple_config.yaml"))


def test_build(raml, config, tmpdir):
    tmp_output = tmpdir.mkdir("output")

    build(raml, config, str(tmp_output))

    # TODO: test the existance of assets & asset dirs

    # TODO: test the existance of genderated HTML & parent dirs
