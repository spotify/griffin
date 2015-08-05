# -*- coding: utf-8 -*-
# Copyright (c) 2015 Spotify AB

from __future__ import absolute_import, division, print_function

from collections import OrderedDict
import os
import shutil


class OrderedDefaultDict(OrderedDict):
    """
    Creates an ordered ``defaultdict``.
    """
    def __init__(self, *args, **kwargs):
        if not args:
            self.default_factory = None
        else:
            if not (args[0] is not None or callable(args[0])):
                raise TypeError("First argument must be callable or None")
            self.default_factory = args[0]
            args = args[1:]
        super(OrderedDefaultDict, self).__init__(*args, **kwargs)

    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        self[key] = default = self.default_factory()
        return default


def _pretty_compact_json(obj, indent=2, max_strlen=20):
    """
    Converts objects to stringified JSON with compact arrays.
    Will flatten array items onto the same line if:
    - items are all integers, or
    - items are all floats, or
    - items are all strings less than max_strlen characters.
    """

    space = " "
    newline = "\n"

    def to_json(o, level=0):
        ret = ""
        if isinstance(o, list):
            # Compact lists
            if all(isinstance(item, int) for item in o):
                ret += "[" + ", ".join(map(str, o)) + "]"
            elif all(isinstance(item, float) for item in o):
                ret += "[" + ", ".join(map(lambda x: '%.7g' % x, o)) + "]"
            elif all((isinstance(item, basestring) and
                     len(item) < max_strlen) for item in o):
                ret += "[" + ", ".join(map(lambda x: '"%s"' % x, o)) + "]"
            # Expanded lists
            else:
                ret += "[" + newline
                comma = ""
                for v in o:
                    ret += comma
                    comma = ",\n"
                    ret += space * indent * (level + 1)
                    ret += to_json(v, level + 1)
                ret += newline + space * indent * level + "]"
        # The rest is conventional JSON pretty-print
        elif isinstance(o, dict):
            ret += "{" + newline
            comma = ""
            for k, v in o.iteritems():
                ret += comma
                comma = ",\n"
                ret += space * indent * (level + 1)
                ret += '"' + str(k) + '":' + space
                ret += to_json(v, level + 1)
            ret += newline + space * indent * level + "}"
        elif isinstance(o, basestring):
            ret += '"' + o + '"'
        elif isinstance(o, bool):
            ret += "true" if o else "false"
        elif isinstance(o, int):
            ret += str(o)
        elif isinstance(o, float):
            ret += '%.7g' % o
        elif o is None:
            ret += "null"
        else:
            msg = "Unknown type '{0}' for json serialization".format(type(o))
            raise TypeError(msg)
        return ret

    return to_json(obj)


def _is_markdown_file(path):
    """
    Return ``True`` if the given file is a Markdown file.
    """
    ext = os.path.splitext(path)[1].lower()
    return ext in [
        '.markdown',
        '.mdown',
        '.mkdn',
        '.mkd',
        '.md',
    ]


def _is_html_file(path):
    """
    Return ``True`` if the given file is an HTML file.
    """
    ext = os.path.splitext(path)[1].lower()
    return ext in [
        '.html',
        '.htm',
    ]


def _copy_file(source_path, output_path):
    """
    Copy ``source_path`` to ``output_path``, preserving parent
    directories.
    """
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    shutil.copy(source_path, output_path)


def _copy_media_files(from_dir, to_dir):
    """
    Copy media files from ``from_dir`` to ``to_dir``.
    """
    for (source_dir, dirnames, filenames) in os.walk(from_dir):
        relative_path = os.path.relpath(source_dir, from_dir)
        output_dir = os.path.normpath(os.path.join(to_dir, relative_path))

        # Ignore filenames starting with a '.'
        filenames = [f for f in filenames if not f.startswith('.')]

        # Ignore dirnames that start with a '.'
        dirnames[:] = [d for d in dirnames if not d.startswith('.')]

        for filename in filenames:
            if not _is_markdown_file(filename) and not _is_html_file(filename):
                source_path = os.path.join(source_dir, filename)
                output_path = os.path.join(output_dir, filename)
                _copy_file(source_path, output_path)
