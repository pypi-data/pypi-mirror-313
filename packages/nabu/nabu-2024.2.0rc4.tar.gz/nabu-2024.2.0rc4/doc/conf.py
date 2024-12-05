# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

sys.path.insert(0, os.path.abspath("../"))


# -- Project information -----------------------------------------------------

project = "Nabu"
copyright = "2019-2024, ESRF"
author = "Pierre Paleo"

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "myst_parser",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.napoleon",
    "sphinx.ext.autodoc",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode",
    "nbsphinx",
    #    'sphinx.ext.autosummary',
    #    'sphinx.ext.doctest',
    #    'sphinx.ext.inheritance_diagram',
]
# myst_commonmark_only = True
# for myst
suppress_warnings = [
    "myst.header",  # non-consecutive headers levels
    "autosectionlabel.*",  # duplicate section names
]
myst_heading_anchors = 3
myst_enable_extensions = [
    #    "amsmath",
    # #   "colon_fence",
    # #   "deflist",
    "dollarmath",
    #    "html_admonition",
    #    "html_image",
    #    "linkify",
    # #   "replacements",
    # #   "smartquotes",
    # #   "substitution"
]
#
# autosummary_generate = True
autodoc_member_order = "bysource"

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#

# from corlab_theme import get_theme_dir
# html_theme = 'corlab_theme'

from cloud_sptheme import get_theme_dir

html_theme = "cloud"

html_theme_path = [get_theme_dir()]

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
# These paths are either relative to html_static_path
# or fully qualified paths (eg. https://...)
html_css_files = [
    "theme_overrides.css",
]

html_theme_options = {
    #    'navigation_depth': -1,
    "max_width": "75%",
    "minimal_width": "720px",
}


# For mathjax
mathjax_path = "javascript/MathJax-3.0.5/es5/tex-mml-chtml.js"


"""
# For recommonmark
from recommonmark.transform import AutoStructify
github_doc_root = 'https://github.com/rtfd/recommonmark/tree/master/doc/'
def setup(app):
    app.add_config_value('recommonmark_config', {
            'url_resolver': lambda url: github_doc_root + url,
            'auto_toc_tree_section': 'Contents',
            'enable_math': True,
            'enable_inline_math': True,
            }, True)
    app.add_transform(AutoStructify)
"""

# Document __init__
autoclass_content = "both"

from nabu import __version__

version = __version__
release = version

master_doc = "index"

#
# nbsphinx
#

nbsphinx_allow_errors = True
