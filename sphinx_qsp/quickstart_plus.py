#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    SphinxQuickStartPlus - sphinx-quickstart Utility
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

""" Font Awesome Extension
 Font Awesome: http://fontawesome.io/
 sphinx_fontawesome: https://github.com/fraoustin/sphinx_fontawesome
"""
sphinx_fontawesome_extension = {
    "conf_py": """
import sphinx_fontawesome
extensions.append('sphinx_fontawesome')
""",
    "package": ["sphinx_fontawesome"]
}

sphinx_commonmark_extension = {
    "conf_py": """
source_suffix.append('.md')

from recommonmark.parser import CommonMarkParser
source_parsers = {
    '.md': CommonMarkParser,
}
""",
    "package": ["commonmark", "recommonmark"]
}

sphinx_commonmark_autostructify_extension = {
    "conf_py": """
from recommonmark.transform import AutoStructify

github_doc_root = 'https://github.com/rtfd/recommonmark/tree/master/doc/'
def setup(app):
    app.add_config_value('recommonmark_config', {
            'url_resolver': lambda url: github_doc_root + url,
            'auto_toc_tree_section': 'Contents',
            }, True)
    app.add_transform(AutoStructify)
""",
    "package": ["recommonmark"],
}

sphinx_sphinx_rtd_theme_extension = {
    "conf_py": """
import sphinx_rtd_theme
html_theme = "sphinx_rtd_theme"
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
""",
    "package": ["sphinx_rtd_theme"],
}

sphinx_autobuild_extension = {
    "makefile": """
livehtml:
\tsphinx-autobuild -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html
""",
    "package": ["sphinx-autobuild"],
}

nbsphinx_extension = {
    "conf_py": """
extensions.append('nbsphinx')
exclude_patterns.append('**.ipynb_checkpoints')
""",
    "package": ["nbsphinx"],
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
