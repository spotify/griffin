# -*- coding: utf-8 -*-
# Copyright (c) 2015 Spotify AB

from __future__ import absolute_import, division, print_function

import markdown2


def dictionary(item):
    if isinstance(item, dict):
        return True
    return False


def a_list(item):
    if isinstance(item, list):
        return True
    return False


def map_schemes(item):
    try:
        return {
            "oauth_2_0": "OAuth 2.0",
            "oauth_1_0": "OAuth 1.0",
            "http_basic": "Basic Authentication",
            "basic": "Basic Authentication",
            "basic_auth": "Basic Authentication",
            "basicAuth": "Basic Authentication",
            "basicAuthentication": "Basic Authentication",
            "http_digest": "Digest Authentication",
            "digest": "Digest Authentication",
            "digest_auth": "Digest Authentication",
            "digestAuth": "Digest Authentication",
            "digestAuthentication": "Digest Authentication"
        }[item]
    except KeyError:
        return item


def markdown(text):
    if text:
        return markdown2.markdown(text)[3:-5]
    return text


def attrs(param):
    if param.default and param.default is not None:
        return True
    if param.minimum and param.minimum is not None:
        return True
    if param.maximum and param.maximum is not None:
        return True
    if param.max_length and param.max_length is not None:
        return True
    if param.min_length and param.min_length is not None:
        return True
    return False
