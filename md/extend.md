# Let's monky patch!


Did you want to further expand 'sphinx-quickstart-plus'?
Editing 'sphinx-quickstart-plus' source code for extension is not cool.

Let's monky patch!

Below is an example of a simple extension.

```python
from sphinx_qsp import quickstart_plus

# Setting your extension.
your_extension = quickstart_plus.Extension(
    "ext_your_ext", "your extensions description.",
    conf_py="""

# ----Your Extension
import your_extension_package
extension.append("your-extension_name")
)
""",
    package=["your_extension_packge"]
)

# Add your extension.
quickstart_plus.qsp_extensions.extend([
    your_extension
])

# Run sphinx-quickstart-plus.
quickstart_plus.main()

```

The base class of extension is the following code.

```eval_rst
.. literalinclude:: /../sphinx_qsp/quickstart_plus.py
  :language: python
  :pyobject: Extension
```

The extended class of 'sphinx-autobuild' is the following code.

```eval_rst
.. literalinclude:: /../sphinx_qsp/quickstart_plus.py
  :language: python
  :pyobject: AutoBuildExtension
```
