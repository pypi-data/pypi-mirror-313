# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'showtens'
copyright = '2024, Vassilis Papadopoulos'
author = 'Vassilis Papadopoulos'
release = '0.3'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode'
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
html_theme = 'pydata_sphinx_theme'
# html_theme_options = {
#     "light_css_variables": {
#         "color-brand-primary": "#2962ff",    # Strong blue for main brand
#         "color-brand-content": "#1976d2",    # Slightly darker blue for content
#         "color-highlight-on-target": "#e3f2fd",  # Very light blue for highlights
#     },
#     "dark_css_variables": {
#         "color-brand-primary": "#90caf9",    # Light blue for main brand in dark mode
#         "color-brand-content": "#64b5f6",    # Slightly darker blue for content
#         "color-highlight-on-target": "#0d47a1",  # Dark blue for highlights
#     },
# }
html_static_path = ['_static']
html_css_files = ['custom.css']


import os
import sys
sys.path.insert(0, os.path.abspath('../../src/showtens'))