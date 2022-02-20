import os
import sys
sys.path.insert(0, os.path.abspath('..'))

project = 'akeno'
copyright = '2022, Okimii'
author = 'Okimii'

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx.ext.extlinks",
]
default_dark_mode = True

templates_path = ['_templates']

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


html_theme = 'furo'

html_static_path = ['_static']
