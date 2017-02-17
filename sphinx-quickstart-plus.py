#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    SphinxQuickStartPlus - sphinx-quickstart Utility

    sphinx:
        http://www.sphinx-doc.org/en/stable/

    extend sphix-quickstart.

    - Remember latest sphinx-quickstart settings.
    - More extensions
      - commonmark and recommonmark
      - Read the Docs theme
      - sphinx_fontawesome
      - sphinxcontrib-blockdiag
      - nbsphinx
      - sphinx-autobuild

    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    :author: pashango2.
    :license: Free.
"""
import sys
import sphinx_qsp

if __name__ == '__main__':
    sphinx_qsp.main(sys.argv)
