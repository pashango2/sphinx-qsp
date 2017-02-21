# Extensions


## Code added to conf.py
### ext_commonmark

```python
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

```

### ext_nbshpinx

```python
# ----- Jupyter Notebook nbsphinx
extensions.append('nbsphinx')
exclude_patterns.append('**.ipynb_checkpoints')
```

### ext_blockdiag
```python
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
```

### ext_fontawesome
```python
# ----- sphinx-fontawesome
import sphinx_fontawesome
extensions.append('sphinx_fontawesome')
```

### ext_rtd_theme
```python
# ----- Read the Docs Theme
html_theme = "sphinx_rtd_theme"
```
### ext_autobuild

'auto_build' does not override 'conf.py', but rewrites the Makefile.
Type the following command to start auto build.

```
$ make livehtml
```

On Windows, `auto_build.bat` is generated, please execute it.

```
$ auto_build.bat
```
