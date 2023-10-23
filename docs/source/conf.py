# docs/source/conf.py
# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
#
# List of Options from RTD:
# https://sphinx-rtd-theme.readthedocs.io/en/stable/configuring.html
#

# ================================== Imports ==================================

import os
import sys
import pkg_resources
from pathlib import Path


# ============================== Build Environment ==============================

# Build behaviour is dependent on environment
on_rtd = os.environ.get('READTHEDOCS') == 'True'

# Configure paths
root = os.path.abspath('../../')
sys.path.append(os.path.abspath('.'))
sys.path.insert(0, root)

# on_rtd = True  # Uncomment for testing RTD builds locally


# ============================ Project information ============================

author = 'Adam Korn'
copyright = '2023, Adam Korn'
project = 'sphinx-inlinecode'
repo = project

# Package Info
# pkg = pkg_resources.require(project)[0]
# pkg_name = pkg.get_metadata('top_level.txt').strip()

# Simplify things by using the installed version
version = '0.0.1' #pkg.version
release = version

# ======================== General configuration ============================

# Doc with root toctree
master_doc = 'contents'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Source File type
source_suffix = '.rst'

# LaTeX settings
latex_elements = {  # Less yucky looking font
    'preamble': r'''
\usepackage[utf8]{inputenc}
\usepackage{charter}
\usepackage[defaultsans]{lato}
\usepackage{inconsolata}
''',
}

# Use default Pygments style if not html
if 'html' not in sys.argv:
    pygments_style = 'sphinx'

# ============================ HTML Theme Settings ============================

# The theme to use for HTML and HTML Help pages.
html_theme = 'sphinx_rtd_theme'

# Theme Options
# https://sphinx-rtd-theme.readthedocs.io/en/stable/configuring.html#theme-options
#
html_theme_options = {
    # Add the [+] signs to nav
    'collapse_navigation': False,
    # Prev/Next buttons also placed at the top
    'prev_next_buttons_location': 'both',
}

# html_logo = "_static/logo_html.png"

# Set the "Edit on GitHub" link to use the current commit
html_context = {
    'display_github': True,
    'github_user': 'TDKorn',
    'github_repo': repo,
}

if not on_rtd:
    site_url = "https://tdkorn.github.io/sphinx-inlinecode/"

html_baseurl = "https://sphinx-inlinecode.readthedocs.io/en/latest/"

sitemap_url_scheme = "{link}"
# ============================ Extensions ====================================

# Add any Sphinx extension module names here, as strings
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.viewcode',
    'sphinx_readme',
    'sphinx_sitemap',
    'sphinx_github_style',
    'sphinx_inlinecode'
]

# ====================== Extra Settings for Extensions ========================

# ~~~~ InterSphinx ~~~~
# Add references to Python, Requests docs
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'requests': ('https://requests.readthedocs.io/en/latest/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
    'bs4': ('https://www.crummy.com/software/BeautifulSoup/bs4/doc/', None)
}

# ~~~~ AutoSectionLabel ~~~~
# Make sure the target is unique
autosectionlabel_prefix_document = True

# ~~~~ Autodoc ~~~~
# Order based on source
autodoc_member_order = 'bysource'
#
# Remove typehints from method signatures and put in description instead
autodoc_typehints = 'description'
#
# Only add typehints for documented parameters (and all return types)
#  ->  Prevents parameters being documented twice for both the class and __init__
autodoc_typehints_description_target = 'documented_params'
#
# Shorten type hints
python_use_unqualified_type_names = True

# ~~~~ Sphinx GitHub Style ~~~~
#
top_level = "sphinx_inlinecode"

# Text to use for the linkcode link
linkcode_link_text = "View on GitHub"

readme_blob = linkcode_blob = "main"

# ~~~~~ Sphinx README ~~~~~~~

readme_src_files = "index.rst"

readme_docs_url_type = "html"


def skip(app, what, name, obj, would_skip, options):
    """Include __init__ as a documented method

    For classes:

        >>> if not obj.__qualname__.startswith("ClassName"):
        >>>     return False
    """
    if name in ('__init__',):
        return False
    return would_skip


def rename_index(app, exception):
    readme = Path(f"{root}/README.rst")
    index = Path(f"{root}/index.rst")

    if index.exists():
        readme.write_text(index.read_text(encoding="utf-8"), encoding="utf-8")
        index.unlink()


def setup(app):
    app.connect('autodoc-skip-member', skip)
    app.connect('build-finished', rename_index, priority=10000)
    app.add_css_file("custom.css")
