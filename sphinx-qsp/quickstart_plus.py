#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Sphinx - Python documentation toolchain
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    :copyright: Copyright 2007-2016 by the Sphinx team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from __future__ import print_function
from __future__ import absolute_import

import sys
import os
import shutil
import json
import argparse
from sphinx.quickstart import ask_user, generate, do_prompt, is_path, package_dir
import sphinx

package_template_dir = os.path.join(package_dir, 'templates', 'quickstart')
JSON_NAME = "setting.json"

TEMPORARY_VALUE = {
    'project': 'qsp',
    'author': 'qsp',
    'path': '.',
    'version': '1.0',
    'release': "1.0",
}


def main(argv=sys.argv):
    desc = 'Sphinx quick start plus.'
    parser = argparse.ArgumentParser(description=desc)

    # 文字列
    parser.add_argument(
        '-c', '--create_teplate',
        type=str,
        dest='create_template',
        required=False,
        help='create sphinx templete.'
    )

    args = parser.parse_args()

    if args.create_template:
        create_template()
    else:
        quick_start()


def create_template():
    d = TEMPORARY_VALUE.copy()
    ask_user(d)

    template_d = {
        'path': "test_output"
    }

    print('Enter the root path for template.')
    do_prompt(template_d, 'path', 'Root path for the template', template_d.get('path', '.'), is_path)

    for filename in os.listdir(package_template_dir):
        src = os.path.join(package_template_dir, filename)
        dst = os.path.join(template_d['path'], filename)
        shutil.copy2(src, dst)
        print("copy ", filename)

    json_obj = {
        "sphinx-version": sphinx.__version__,
        "quick_start_value": {key: value for key, value in d.items() if key not in TEMPORARY_VALUE},
    }
    json.dump(json_obj, open(os.path.join(template_d['path'], JSON_NAME), "w"), indent=4)


def quick_start():
    json_path = os.path.join("test_output", JSON_NAME)
    json_obj = json.load(open(json_path))
    d = json_obj.get("quick_start_value", {})

    ask_user(d)
    generate(d, templatedir="test_output")
