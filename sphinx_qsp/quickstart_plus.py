#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    SphinxQuickStartPlus - sphinx-quickstart Utility
    ------------------------------------------------

    sphinx:
        http://www.sphinx-doc.org/en/stable/

    extend sphix-quickstart.

    * Remember latest sphinx-quickstart settings.
    * More extensions

      * commonmark and recommonmark
      * Read the Docs theme
      * sphinx_fontawesome
      * sphinxcontrib-blockdiag
      * nbsphinx
      * sphinx-autobuild

    :author: pashango2
    :license: Free
"""
from __future__ import absolute_import
from __future__ import print_function
import sys
import copy
import json
import os

from sphinx import quickstart
from sphinx.quickstart import ask_user, generate, do_prompt, nonempty, boolean

__version__ = "0.6"


HOME_DIR = os.path.join(os.path.expanduser('~'), ".sphinx_qsp")
LATEST_SETTING_JSON_NAME = "setting.json"

EXCLUDE_VALUE = ['project', 'author', 'path', 'version', 'release', 'extensions']

AUTOBUILD_IGNORE = [
    '-r "___jb_.*?___$$"',   # for pycharm
    '-r "^~.*"',
    '-r ".*?\.(bak|BAK)$$"',
]

AUTO_BUILD_BATCH = """
@ECHO OFF

pushd %~dp0

REM Command file for Sphinx auto build

set SOURCEDIR={source_dir}
set BUILDDIR={build_dir}

sphinx-autobuild -b html {AUTOBUILD_IGNORE} %SOURCEDIR% %BUILDDIR%/html
goto end

:end
popd
""".strip()


class Extension(object):
    def __init__(self, key, description, conf_py=None, new_makefile=None,
                 makefile=None, package=None):
        self.key = key
        self.description = description
        self.conf_py = conf_py
        self.new_makefile = new_makefile
        self.makefile = makefile
        self.package = package or []

    # noinspection PyUnusedLocal
    def extend_conf_py(self, d):
        return self.conf_py

    def extend_makefile(self, d, make_mode):
        return self.new_makefile if make_mode else self.makefile


class AutoBuildExtension(Extension):
    def extend_makefile(self, d, make_mode):
        if d['batchfile']:
            batchfile_path = os.path.join(d['path'], 'auto_build.bat')
            source_dir = d['sep'] and 'source' or '.'
            build_dir = d['sep'] and 'build' or d['dot'] + 'build'

            open(batchfile_path, "w").write(
                AUTO_BUILD_BATCH.format(
                    build_dir=build_dir, source_dir=source_dir,
                    AUTOBUILD_IGNORE=" ".join(AUTOBUILD_IGNORE),
                )
            )

        makefile = self.new_makefile if make_mode else self.makefile
        return makefile.format(" ".join(AUTOBUILD_IGNORE))


sphinx_fontawesome_extension = Extension(
    "ext_fontawesome", "use font awesome",
    conf_py="""
# ----- sphinx-fontawesome
import sphinx_fontawesome
extensions.append('sphinx_fontawesome')
""",
    package=["sphinx-fontawesome"],
)

sphinx_commonmark_extension = Extension(
    "ext_commonmark", "use CommonMark and AutoStructify",
    conf_py="""

# ----- CommonMark
source_suffix = [source_suffix, '.md']

from recommonmark.parser import CommonMarkParser
source_parsers = {
    '.md': CommonMarkParser,
}

from recommonmark.transform import AutoStructify

github_doc_root = 'https://github.com/rtfd/recommonmark/tree/master/doc/'
def setup(app):
    app.add_config_value('recommonmark_config', {
            'url_resolver': lambda url: github_doc_root + url,
            'auto_toc_tree_section': 'Contents',
            }, True)
    app.add_transform(AutoStructify)
""",
    package=["CommonMark", "recommonmark"],
)

sphinx_sphinx_rtd_theme_extension = Extension(
    "ext_rtd_theme", "use Read the Doc theme",
    conf_py="""

# ----- Read the Docs Theme
html_theme = "sphinx_rtd_theme"
""",
    package=["sphinx-rtd-theme"],
)

nbsphinx_extension = Extension(
    "ext_nbshpinx", "provides a source parser for *.ipynb files",
    conf_py="""

# ----- Jupyter Notebook nbsphinx
extensions.append('nbsphinx')
exclude_patterns.append('**.ipynb_checkpoints')
""",
    package=["nbsphinx"],
)

sphinx_blockdiag_extension = Extension(
    "ext_blockdiag", "Sphinx extension for embedding blockdiag diagrams",
    conf_py="""

# ----- blockdiag settings
extensions.extend([
    'sphinxcontrib.blockdiag',
    'sphinxcontrib.seqdiag',
    'sphinxcontrib.actdiag',
    'sphinxcontrib.nwdiag',
    'sphinxcontrib.rackdiag',
    'sphinxcontrib.packetdiag',
])
blockdiag_html_image_format = 'SVG'
seqdiag_html_image_format = 'SVG'
actdiag_html_image_format = 'SVG'
nwdiag_html_image_format = 'SVG'
rackiag_html_image_format = 'SVG'
packetdiag_html_image_format = 'SVG'
""",
    package=[
        "sphinxcontrib-actdiag", "sphinxcontrib-blockdiag",
        "sphinxcontrib-nwdiag", "sphinxcontrib-seqdiag"
    ]
)

sphinx_autobuild_extension = AutoBuildExtension(
    "ext_autobuild", "Watch a directory and rebuild the documentation",
    makefile="""

livehtml:
\tsphinx-autobuild -b html {0} $(ALLSPHINXOPTS) $(BUILDDIR)/html
""",
    new_makefile="""

livehtml:
\tsphinx-autobuild -b html {0} $(SOURCEDIR) $(BUILDDIR)/html
""",
    package=["sphinx-autobuild"],
)

qsp_extensions = [
    sphinx_commonmark_extension,
    nbsphinx_extension,
    sphinx_blockdiag_extension,
    sphinx_fontawesome_extension,
    sphinx_sphinx_rtd_theme_extension,
    sphinx_autobuild_extension,
]

# for python2... can't use nonlocal
hook_d = {}


def qsp_ask_latest():
    """ ask use latest setting """
    global hook_d

    if hook_d:
        d = {}
        do_prompt(d, 'use_latest', 'Use latest setting? (y/n)', 'y', boolean)
        return d['use_latest']

    return False


def qsp_ask_user(d):
    """ quick start extend questions.

    :param dict d: setting dict
    :return:
    """
    for ext in qsp_extensions:
        if ext.key not in d:
            qsp_do_prompt(d, ext.key, ext.key + ":" + ext.description + ' (y/n)', 'n', boolean)


def qsp_do_prompt(d, key, text, default=None, validator=nonempty):
    default = hook_d.get(key, default)
    if isinstance(default, bool):
        default = 'y' if hook_d[key] else 'n'
    do_prompt(d, key, text, default, validator)


def _print_default_setting(d):
    for key in sorted(d.keys()):
        value = d[key]
        if value:
            print(key + ":", value)


def monkey_patch_ask_user(d):
    global hook_d

    org_do_prompt = None

    if not qsp_ask_latest():
        org_do_prompt = quickstart.do_prompt

        # monkey patch
        def _do_prompt(_d, key, text, default=None, validator=nonempty):
            default = hook_d.get(key, default)
            if isinstance(default, bool):
                default = 'y' if hook_d[key] else 'n'
            org_do_prompt(_d, key, text, default, validator)

        quickstart.do_prompt = _do_prompt
    else:
        d.update(hook_d)
        _print_default_setting(d)
        print()

    ask_user(d)
    qsp_ask_user(d)

    if org_do_prompt:
        quickstart.do_prompt = org_do_prompt


def monkey_patch_generate(d, templatedir=None):
    global hook_d
    hook_d = copy.copy(d)

    generate(d, templatedir)


def set_home_dir(_in):
    global HOME_DIR
    HOME_DIR = _in


def check_installed_modules(d=None):
    import pip

    d = d or {}
    installed_dict = {
        x.project_name: x.version
        for x in pip.get_installed_distributions()
    }
    not_installed = []

    for ext in qsp_extensions:
        if ext.key in d:
            for package in ext.package:
                if package not in installed_dict:
                    not_installed.append(package)

    return "pip install {0}".format(" ".join(not_installed)) if not_installed else None


def set_term_input(_term_input):
    quickstart.term_input = _term_input


def dump_setting(d, json_path):
    """ for unit test

    :type d: dict
    :type json_path: str
    """
    json.dump(d, open(json_path, "w"), indent=4)


def main(argv=None):
    global hook_d

    hook_d = {}
    argv = sys.argv if argv is None else argv

    # load latest setting.
    if not os.path.isdir(HOME_DIR):
        os.mkdir(HOME_DIR)

    json_path = os.path.join(HOME_DIR, LATEST_SETTING_JSON_NAME)
    if os.path.isfile(json_path):
        hook_d.update(json.load(open(json_path)))

        # for python 2: oh..
        hook_d = {str(key): value for key, value in hook_d.items()}

    # monkey patch
    quickstart.ask_user = monkey_patch_ask_user
    quickstart.generate = monkey_patch_generate

    # do sphinx.quickstart
    quickstart.main(argv)

    # save latest setting.
    save_d = {key: value for key, value in hook_d.items() if key not in EXCLUDE_VALUE}
    dump_setting(save_d, json_path)

    # write ext-extensions
    d = hook_d

    srcdir = d['sep'] and os.path.join(d['path'], 'source') or d['path']
    conf_path = os.path.join(srcdir, "conf.py")

    with open(conf_path, "a+") as fc:
        for ext in qsp_extensions:
            if d.get(ext.key) and ext.conf_py:
                fc.write(ext.extend_conf_py(d))

    if d['makefile'] is True:
        make_path = os.path.join(d['path'], 'Makefile')
        make_mode = d.get("make_mode", True)
        with open(make_path, "a+") as fm:
            makefile_key = "new_makefile" if make_mode else "makefile"
            for ext in qsp_extensions:
                if d.get(ext.key) and getattr(ext, makefile_key):
                    fm.write(ext.extend_makefile(d, make_mode))

    # check install module
    print("check modules...")
    pip_text = check_installed_modules(d)

    if pip_text:
        print()
        print("Module not found, please enter '{0}' and install module.".format(pip_text))
    else:
        print("ok")

if __name__ == '__main__':
    main(sys.argv)
