"""Sphinx configuration for the public English documentation."""

from genro_typst import __version__

project = "Genro Typst"
author = "Softwell S.r.l."
copyright = "2026, Softwell S.r.l."
release = __version__
language = "en"
needs_sphinx = "7.4"
nitpicky = True
extensions = ["myst_parser", "sphinx.ext.autodoc", "sphinx.ext.viewcode"]
myst_heading_anchors = 3
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
html_theme = "furo"
html_title = f"Genro Typst {release}"
html_static_path = []
autodoc_member_order = "bysource"
autodoc_typehints = "none"
