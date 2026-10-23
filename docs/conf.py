"""Sphinx configuration for the public English documentation."""

from pathlib import Path

from genro_typst import __version__

project = "Genro Typst"
author = "Genropy Team"
copyright = "2026, Softwell S.r.l."
release = __version__
language = "en"
needs_sphinx = "7.4"
nitpicky = True
extensions = ["myst_parser", "sphinx.ext.autodoc", "sphinx.ext.viewcode"]
myst_heading_anchors = 3
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
html_theme = "sphinx_rtd_theme"
html_theme_options = {
    "navigation_depth": 4,
    "collapse_navigation": False,
    "sticky_navigation": True,
    "includehidden": True,
    "titles_only": False,
    "prev_next_buttons_location": "bottom",
    "style_external_links": True,
    "logo_only": False,
    "vcs_pageview_mode": "blob",
}
html_context = {
    "display_github": True,
    "github_user": "genro-org",
    "github_repo": "genro-typst",
    "github_version": "main",
    "conf_py_path": "/docs/",
}
html_title = f"Genro Typst {release}"
html_static_path = []
# The online build contains only static assets; the local Python API is never hosted.
html_extra_path = ["../js/dist/docs"] if (Path(__file__).parent / "../js/dist/docs").is_dir() else []
autodoc_member_order = "bysource"
autodoc_typehints = "none"
