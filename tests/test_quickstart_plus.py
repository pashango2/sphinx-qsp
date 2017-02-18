# -*- coding: utf-8 -*-
"""
    test_quickstart_plus
"""
import sys
import os
from six import PY2, text_type, StringIO
from six.moves import input

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from sphinx_qsp import quickstart_plus as qsp
from sphinx import quickstart as qs


def test_quickstart(tmpdir):
    answers = {
        'Root path': str(tmpdir.realpath()),
        'Separate source and build': 'y',
        'Name prefix for templates': '.',
        'Project name': u'STASI™'.encode('utf-8'),
        'Author name': u'Wolfgang Schäuble & G\'Beckstein'.encode('utf-8'),
        'Project version': '2.0',
        'Project release': '2.0.1',
        'Project language': 'de',
        'Source file suffix': '.txt',
        'Name of your master document': 'contents',
        'autodoc': 'y',
        'doctest': 'yes',
        'intersphinx': 'no',
        'todo': 'y',
        'coverage': 'no',
        'imgmath': 'N',
        'mathjax': 'no',
        'ifconfig': 'no',
        'viewcode': 'no',
        'githubpages': 'no',
        'ext_rtd_theme': 'y',
        'ext_fontawesome': 'y',
        'Create Makefile': 'no',
        'Create Windows command file': 'no',
        'Do you want to use the epub builder': 'yes',
    }

    tmpdir.mkdir(".sphinxpsp")

    qsp.set_home_dir(str(tmpdir.realpath()))

    prompt = mock_input(answers)
    qsp.set_term_input(prompt)

    save_d = {}

    def dump_setting(d, _):
        save_d["save"] = d

    qsp.dump_setting = dump_setting
    qsp.main([])

    conffile = tmpdir / 'conf.py'

    print(conffile)

    print(save_d)





def mock_input(answers, needanswer=False):
    called = set()

    def input_(prompt):
        called.add(prompt)
        if PY2:
            prompt = str(prompt)  # Python2.x raw_input emulation
            # `raw_input` encode `prompt` by default encoding to print.
        else:
            prompt = text_type(prompt)  # Python3.x input emulation
            # `input` decode prompt by default encoding before print.
        for question in answers:
            if prompt.startswith(qs.PROMPT_PREFIX + question):
                return answers[question]
        if needanswer:
            raise AssertionError('answer for %r missing' % prompt)
        return ''

    return input_
