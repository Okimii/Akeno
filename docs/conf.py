import os
import sys

sys.path.insert(0, os.path.abspath(".."))

project = "akeno"
copyright = "2022, Okimii"
author = "Okimii"

extensions = ["sphinx.ext.autodoc", "sphinx.ext.intersphinx", "sphinx.ext.napoleon", "sphinx.ext.extlinks"]
default_dark_mode = True

templates_path = ["_templates"]

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


html_theme = "furo"

html_theme_options = {
    "light_css_variables": {"color-brand-primary": "#7C4DFF", "color-brand-content": "#7C4DFF"},
    "dark_css_variables": {"color-brand-primary": "#7C4DFF", "color-brand-content": "#7C4DFF"},
}

html_static_path = ["_static"]

pygments_style = "sphinx"
pygments_dark_style = "monokai"
