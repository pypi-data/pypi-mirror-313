# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

from importlib.metadata import version as get_version

project = 'WuttaWeb'
copyright = '2024, Lance Edgar'
author = 'Lance Edgar'
release = get_version('WuttaWeb')

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
    'sphinx.ext.todo',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

intersphinx_mapping = {
    'colander': ('https://docs.pylonsproject.org/projects/colander/en/latest/', None),
    'deform': ('https://docs.pylonsproject.org/projects/deform/en/latest/', None),
    'pyramid': ('https://docs.pylonsproject.org/projects/pyramid/en/latest/', None),
    'python': ('https://docs.python.org/3/', None),
    'rattail-manual': ('https://rattailproject.org/docs/rattail-manual/', None),
    'webhelpers2': ('https://webhelpers2.readthedocs.io/en/latest/', None),
    'wuttjamaican': ('https://rattailproject.org/docs/wuttjamaican/', None),
    'wutta-continuum': ('https://rattailproject.org/docs/wutta-continuum/', None),
}


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']
