# -*- coding: utf-8 -*-
# Copyright (c) 2015 Spotify AB

from __future__ import absolute_import, division, print_function

import sys
if sys.version_info[0] == 2:
    from io import open

import os

import jinja2
import markdown2

from ._filters import dictionary, a_list, map_schemes, markdown, attrs
from .core import create_context
from .utils import _copy_media_files, _pretty_compact_json


#####
# Little helper functions
#####

def _create_path_here(fileobj):
    here = os.path.dirname(__file__)
    return os.path.join(here, fileobj)


def _theme_path(rel_directory, config):
    if config.get("theme_path"):
        _theme_dir = config.get("theme_path")
        _theme_name = config.get("theme_name")
        _theme_path = os.path.join(_theme_dir, _theme_name)
        return os.path.join(rel_directory, _theme_path)
    _theme_dir = _create_path_here("themes")
    _theme_name = config.get("theme_name")
    return os.path.join(_theme_dir, _theme_name)


def _template_path(config):
    _temp_dir = config.get("template_dir")
    return _create_path_here(_temp_dir)


def _static_path(rel_directory, config):
    _static_dir = config.get("static_dir")
    return os.path.join(rel_directory, _static_dir)


def _save_template(template, output):
    if not os.path.exists(output):
        os.makedirs(output)

    save_as = os.path.join(output, "index.html")
    with open(save_as, "w", encoding="utf-8") as f:
        f.write(template)


#####
# Jinja templating-related
#####
def _set_jinja_env(template_path):
    loader = jinja2.FileSystemLoader(template_path)
    env = jinja2.Environment(loader=loader)
    env.tests["a_list"] = a_list
    env.tests["dictionary"] = dictionary
    env.filters["jsonify"] = _pretty_compact_json
    env.filters["schemes"] = map_schemes
    env.filters["markdown"] = markdown
    env.filters["attrs"] = attrs
    return env


def _create_template(context, env, tmpl_file):
    template = env.get_template(tmpl_file)
    return template.render(context)


def _create_landing_page(index_page, context, env):
    with open(index_page, "r") as f:
        context["index"] = markdown2.markdown(f.read())

    return _create_template(context, env, "index.html")


def _custom_css(config, template_path, output):
    custom_css = config.get("custom_css", {})
    rest_colors = custom_css.get("rest_colors", {})
    navbar_color = custom_css.get("navbar_color", {})
    fonts = custom_css.get("fonts", {})
    context = dict(rest_colors=rest_colors,
                   navbar_color=navbar_color,
                   fonts=fonts)
    loader = jinja2.FileSystemLoader(template_path)
    env = jinja2.Environment(loader=loader)

    _template = env.get_template("custom.css")
    template = _template.render(context)

    css_dir = os.path.join(output, "css")
    if not os.path.exists(css_dir):
        os.makedirs(css_dir)
    save_as = os.path.join(css_dir, "custom.css")

    with open(save_as, "w", encoding="utf-8") as f:
        f.write(template)


# Main build function for CLI
def build(ramlfile, config, output=None, ramlconfig=None):
    """
    Builds HTML templates from a RAML file and saves to desired output.

    :param str ramlfile: path to raml file
    :param dict config: documentation config
    :param str output: output of HTML files
    :param str ramlconfig: configuration for RAML parsing.  See \
        `ramlfications documentation \
        <https://ramlfications.readthedocs.org/en/latest/config.html>`_ \
        for more information.
    """
    # parse out RAML file & create context for templates
    context = create_context(ramlfile, ramlconfig)
    site_context = dict(site=config,
                        meta=context.metadata,
                        endpoints=context.groupings)

    if not output:
        output = config.get("output_dir")

    # set up Jinja templates
    template_path = _template_path(config)
    env = _set_jinja_env(template_path)

    # create main site template
    site_template = _create_template(site_context, env, "base.html")
    _save_template(site_template, output)

    # create endpoint templates
    for endpoint in context.endpoints:
        end_context = dict(site=config, meta=context.metadata,
                           endpoints=context.groupings, endpoint=endpoint)
        endp_template = _create_template(end_context, env,
                                         "endpoint/index.html")
        directory = endpoint.get("anchor")
        endpoint_out = os.path.join(output, directory)
        _save_template(endp_template, endpoint_out)

    # create landing page
    rel_directory = os.path.dirname(ramlfile)
    index_md = os.path.join(rel_directory, "index.md")
    landing_page = _create_landing_page(index_md, site_context, env)
    _save_template(landing_page, output)

    # save static/assets
    theme_path = _theme_path(rel_directory, config)
    static_path = _static_path(rel_directory, config)
    assets_path = os.path.join(output, "assets")

    if config.get("custom_css"):
        _custom_css(config, template_path, assets_path)
    _copy_media_files(theme_path, assets_path)
    _copy_media_files(static_path, assets_path)
