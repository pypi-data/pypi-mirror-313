# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

from __future__ import annotations

# Warning: do not change the path here. To use autodoc, you need to install the
# package first.

# -- Path setup --------------------------------------------------------------

import os
import sys
sys.path.insert(0, os.path.abspath("../.."))
print(sys.path)

# -- Project information -----------------------------------------------------

project = "WallGo"
copyright = "2024, Andreas Ekstedt, Oliver Gould, Joonas Hirvonen, \
Benoit Laurent, Lauri Niemi, Philipp Schicho, and Jorinde van de Vis"
author = "Andreas Ekstedt, Oliver Gould, Joonas Hirvonen, \
Benoit Laurent, Lauri Niemi, Philipp Schicho, and Jorinde van de Vis"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named "sphinx.ext.*") or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    # "sphinx_automodapi.automodapi",
    # "sphinx_automodapi.smart_resolver",
    # 'sphinx_autodoc_typehints', # types (less noise in class signature)
    'sphinxcontrib.bibtex',
    "sphinx.ext.napoleon", # for numpy style docs
    "sphinx.ext.doctest", # test code snippets in docs
    "sphinx.ext.coverage", # collect doc coverage stats
    "sphinx.ext.mathjax", # support for mathjax
    "sphinx.ext.ifconfig", # if statements for including content
    "sphinx.ext.viewcode", # add links to highlighted source code
    "myst_parser",  # for markdown
]

# Some tricks here from StackOverflow question 2701998
# numpydoc_show_class_members = False # automodapi
autosummary_generate = True
autoclass_content = "both"  # 'both', 'init' or 'class'
html_show_sourcelink = False  # Remove 'view source code' from top of page (for html, not python)
autodoc_inherit_docstrings = True  # If no docstring, inherit from base class
# set_type_checking_flag = True  # Enable 'expensive' imports for sphinx_autodoc_typehints
autodoc_typehints = "description" # Sphinx-native method. Not as good as sphinx_autodoc_typehints
add_module_names = False # Remove namespaces from class/method signatures

# Options for sphinxcontrib.bibtex
bibtex_bibfiles = ['refs.bib']

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# Include both markdown and rst files
source_suffix = [".rst", ".md"]

# The master toctree document.
master_doc = "index"

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = "Python"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "default"

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

html_theme_options = {
    'logo_only': True,
    # 'display_version': True,
    'titles_only': True,
    'style_nav_header_background': '#efefef'
}

html_logo = 'figures/wallgo.svg'
html_favicon = 'figures/favicon.ico'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path: ["_static"]


# -- Extension configuration -------------------------------------------------
