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

import mcai_worker_sdk as mcai

sys.path.append(os.path.abspath('sphinx-ext/'))


# -- Project information -----------------------------------------------------

project = 'mcai-worker-sdk'
copyright = '2023, MCAI Contributors'
author = 'MCAI Contributors'

# The full version, including alpha/beta/rc tags
version = mcai.__version__


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
  "sphinx_rtd_theme",
  "sphinx.ext.autodoc",
  "sphinx.ext.napoleon",
  "toctree_filter",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# We check that this method exist as it is only available in media mode
if hasattr(mcai.Worker, 'process_frames'):
  tags.add("media")
else:
  exclude_patterns.append("media")
  tags.add("basic")


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
