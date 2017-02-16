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

EXCLUDE_VALUE = {
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
source_suffix = [source_suffix, '.md']

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

qsp_extensions = [
    sphinx_fontawesome_extension,
    sphinx_commonmark_extension,
    sphinx_commonmark_autostructify_extension,
    sphinx_sphinx_rtd_theme_extension,
    sphinx_autobuild_extension,
    nbsphinx_extension,
]


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
    home_dir = os.path.join(os.path.expanduser('~'), ".sphinx_qsp")
    if not os.path.isdir(home_dir):
        os.mkdir(home_dir)

    json_path = os.path.join(home_dir, JSON_NAME)
    if os.path.isfile(json_path):
        d = json.load(open(json_path))
    else:
        d = {}

    ask_user(d)

    save_d = d.copy()
    for key in EXCLUDE_VALUE.keys():
        try:
            del save_d[key]
        except KeyError:
            pass

    json.dump(save_d, open(json_path, "w"), indent=4)

    generate(d, templatedir="test_output")

    conf_path = os.path.join(d["path"], "conf.py")
    make_path = os.path.join(d["path"], "Makefile")

    with open(conf_path, "a+") as fc, open(make_path, "a+") as fm:
        for ext in qsp_extensions:
            if "conf_py" in ext:
                fc.write(ext["conf_py"])
            if "makefile" in ext:
                fm.write(ext["makefile"])
