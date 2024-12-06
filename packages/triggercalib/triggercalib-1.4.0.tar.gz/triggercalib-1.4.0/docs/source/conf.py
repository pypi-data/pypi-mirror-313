#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

from datetime import date
import os
import sys

from sphinxawesome_theme.postprocess import Icons
html_permalinks_icon = Icons.permalinks_icon

# Add the package directory to the Python path
sys.path.insert(0, os.path.abspath('../..'))
sys.path.insert(0, os.path.abspath('../../src'))

# -- Project information -----------------------------------------------------

project = "TriggerCalib"
copyright = (
    f'2024-{date.today().strftime("%Y")}, LHCb Collaboration'
    if date.today().strftime("%Y") != "2024"
    else f"2024, LHCb Collaboration"
)
author = "Jamie Gooding"


release = os.getenv('CI_COMMIT_TAG', 'dev')
if "master" in release:
    release = "master"
version = release


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinxawesome_theme",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.mathjax",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.autosummary",  # For generating summaries
    "sphinx.ext.inheritance_diagram",  # For class inheritance diagrams
]

mathjax_path = (
    "https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML"
)

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"
numfig = True

# Autosectionlabel
autosectionlabel_prefix_document = True

# Autosummary settings
autosummary_generate = True  # Generate stub pages for autosummary directives
autosummary_imported_members = True  # Include imported members

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = True
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_ivar = True
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_type_aliases = None

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
pygments_style = "sphinx"
html_theme = "sphinxawesome_theme"
html_logo = "_static/logo.jpeg"
html_favicon = "_static/logo-smaller.jpeg"
# html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

html_context = {
    # Show the "Edit on GitLab" link instead of "View Source"
    "display_gitlab": True,
    "gitlab_host": "gitlab.cern.ch",
    "gitlab_user": "lhcb-rta",
    "gitlab_repo": "triggercalib",
    "gitlab_version": f"{version}/source/",
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
html_css_files = [
    "custom.css",
]

# Add version warning banner for old versions
def setup(app):
    if version != 'dev':
        app.add_config_value('version_warning', True, 'html')
