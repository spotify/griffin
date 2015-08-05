# -*- coding: utf-8 -*-
# Copyright (c) 2015 Spotify AB

from __future__ import absolute_import, division, print_function

import os

from click.testing import CliRunner
import pytest

from griffin import __main__ as main

from .base import CONFIG, EXAMPLES


@pytest.fixture()
def runner():
    return CliRunner()


def check_result(exp_code, exp_msg, result):
    assert result.exit_code == exp_code
    if exp_msg:
        assert result.output == exp_msg


def test_build(runner, tmpdir):
    raml_file = os.path.join(EXAMPLES, "spotify.raml")
    config_file = os.path.join(CONFIG, "simple_config.yaml")
    output_dir = str(tmpdir.mkdir("output"))
    exp_code = 0
    exp_msg = None

    result = runner.invoke(main.build, [
                           "--ramlfile={0}".format(raml_file),
                           "--config={0}".format(config_file),
                           "--output={0}".format(output_dir)])
    check_result(exp_code, exp_msg, result)
