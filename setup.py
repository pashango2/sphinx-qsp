# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

import os
import sys
from distutils import log
from distutils.cmd import Command

import sphinx_qsp

long_desc = '''

'''

if sys.version_info < (2, 7) or (3, 0) <= sys.version_info < (3, 4):
    print('ERROR: sphinx-quickstart-plus requires at least Python 2.7 or 3.4 to run.')
    sys.exit(1)

requires = [
    'sphinx',
]

extras_require = {
    # Environment Marker works for wheel 0.24 or later
    ':sys_platform=="win32"': [
        'colorama>=0.3.5',
    ],
    'websupport': [
        'sqlalchemy>=0.9',
        'whoosh>=2.0',
    ],
    'test': [
        'nose',
        'mock',  # it would be better for 'test:python_version in 2.7'
        'simplejson',  # better: 'test:platform_python_implementation=="PyPy"'
        'html5lib',
    ],
}

# for sdist installation with pip-1.5.6
if sys.platform == 'win32':
    requires.append('colorama>=0.3.5')

try:
    with open('README.txt') as f:
        readme = f.read()
except IOError:
    readme = ''

setup(
    name='sphinx-quickstart-plus',
    version=sphinx_qsp.__version__,
    url='https://github.com/pashango2/sphinx-qsp',
    # download_url='https://pypi.python.org/pypi/Sphinx',
    license='Free',
    author='Toshiyuki Ishii',
    author_email='pashango2@gmail.com',
    description='sphinx-quickstart Utility',
    long_description=readme,
    zip_safe=False,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: Freeware',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Framework :: Sphinx',
        'Framework :: Sphinx :: Extension',
        'Framework :: Sphinx :: Theme',
        'Topic :: Documentation',
        'Topic :: Documentation :: Sphinx',
        'Topic :: Text Processing',
        'Topic :: Utilities',
    ],
    platforms='any',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'sphinx-quickstart-plus = sphinx_qsp.quickstart_plus:main',
        ],
    },
    install_requires=requires,
    extras_require=extras_require,
    # cmdclass={},
)
