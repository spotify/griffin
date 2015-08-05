# -*- coding: utf-8 -*-
# Copyright (c) 2015 Spotify AB

from __future__ import absolute_import, division, print_function

import os

import pytest
from ramlfications import parameters, raml
from six import iterkeys

from griffin.core import create_context

from .base import EXAMPLES


@pytest.fixture(scope="session")
def ramlfile():
    return os.path.join(EXAMPLES, "spotify.raml")


def test_create_context(ramlfile):
    context = create_context(ramlfile)
    meta = context.metadata
    collections = context.groupings

    assert repr(context) == "Spotify Web API"

    _meta_context(meta)
    _collections_context(collections)


def _meta_context(meta):
    assert meta.get("title") == "Spotify Web API"
    assert meta.get("version") == "v1"
    assert meta.get("protocols") == ["HTTPS"]

    assert len(meta.get("docs")) == 1
    assert meta.get("docs")[0].title.raw == "Spotify Web API Docs"
    assert meta.get("docs")[0].content.raw == (
        "Welcome to the _Spotify Web API_ specification. For more information "
        "about\nhow to use the API, check out [developer site]"
        "(https://developer.spotify.com/web-api/).\n"
    )
    assert isinstance(meta.get("docs")[0], parameters.Documentation)

    assert meta.get("uri") == "https://api.spotify.com/v1"
    assert meta.get("b_params") is None
    assert meta.get("u_params") is None

    assert len(meta.get("traits")) == 2
    filterable = meta.get("traits")[0]
    paged = meta.get("traits")[1]

    assert isinstance(filterable, raml.TraitNode)
    assert filterable.name == "filterable"

    assert isinstance(paged, raml.TraitNode)
    assert paged.name == "paged"

    assert len(meta.get("types")) == 4
    base_get = meta.get("types")[0]
    base_post = meta.get("types")[1]
    item = meta.get("types")[2]
    collection = meta.get("types")[3]

    assert base_get.name == "base"
    assert base_get.method == "get"
    assert base_post.name == "base"
    assert base_post.method == "post"
    assert item.name == "item"
    assert collection.name == "collection"

    assert isinstance(base_get, raml.ResourceTypeNode)
    assert isinstance(base_post, raml.ResourceTypeNode)
    assert isinstance(item, raml.ResourceTypeNode)
    assert isinstance(collection, raml.ResourceTypeNode)

    assert meta.get("secured") is None

    assert len(meta.get("sec_schemes")) == 1
    assert meta.get("sec_schemes")[0].name == "oauth_2_0"

    assert meta.get("media_type") == "application/json"


def _collections_context(collections):
    exp_parents = [
        "albums",
        "artists",
        "tracks",
        "search",
        "me",
        "users/{user_id}",
        "browse"
    ]
    assert exp_parents == list(iterkeys(collections))
