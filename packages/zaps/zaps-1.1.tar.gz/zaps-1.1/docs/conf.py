# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Zaps'
copyright = '2024, Amr Muhammad YT/@AmMoPy'
author = 'Amr Muhammad YT/@AmMoPy'
release = '1.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

import os
import sys
sys.path.insert(0, os.path.abspath("..")) # ".." parent of config.py (when build and source are the same), "../.." parent of the parent

extensions = [
	"sphinx.ext.autodoc", # pull docstring from code
    "sphinx.ext.napoleon", # preprocess docstrings to correct `rst` before autodoc processes them
    "sphinx.ext.viewcode", # add `source` button to view source code
    # "sphinx.ext.intersphinx", # fetch external modules from the internet
    # 'sphinx.ext.autosummary',
]

autodoc_default_options = {
    "members":True,
    "inherited-members": False,
    "show-inheritance": False,
    "member-order": "bysource"
}

autodoc_typehints = "none"
# autoclass_content = "class"

# autosummary_generate = True

napoleon_numpy_docstring = True
napoleon_google_docstring = False
napoleon_use_admonition_for_notes = True # Notes placed inside box
napoleon_use_param = False # allow multiple params in on single description
napoleon_use_ivar = True # attributes shown as varaibles also separate method from text
napoleon_use_rtype = False # combine type of return in single line
# napoleon_include_private_with_doc = True

# intersphinx_mapping = {
#     "sklearn": ("https://scikit-learn.org/stable/", None)
# }

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
# html_static_path = ['_static']