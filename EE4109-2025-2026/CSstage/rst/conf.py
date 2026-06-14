# -*- coding: utf-8 -*-

import sys
import os
import time
import sphinx_bootstrap_theme

extensions = [
    'sphinx.ext.mathjax',
    'sphinx.ext.doctest',
]
math_number_all = True
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = u'SLiCAP'
copyright = u'2009-2019, Anton Montagne'
author = u'Anton Montagne'
language = None
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
pygments_style = 'sphinx'
todo_include_todos = False
html_theme = 'bootstrap'
html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()
html_title = u'SLiCAP output'
html_favicon = '_static/amp.ico'
html_static_path = ['_static']
html_last_updated_fmt = time.strftime("%d/%m/%Y")
html_domain_indices = False
html_use_index = True
html_show_sourcelink = False
html_show_sphinx = True
html_show_copyright = True
intersphinx_mapping = {'https://docs.python.org/': None}
html_logo = "amp.png"
html_theme_options = {
    'navbar_title': "SLiCAP",
    'navbar_links': [
        ("Home", "http://www.analog-electronics.eu/slicap/slicap.html", True),
        ("Help", "http://www.analog-electronics.eu/slicap-documentation/slicap-documentation.html", True),
    ],
    'navbar_sidebarrel': False,
    'navbar_pagenav': True,
    'globaltoc_depth': -1,
    'globaltoc_includehidden': "true",
    'navbar_class': "navbar navbar-inverse",
    'navbar_fixed_top': "true",
    'source_link_position': "nav",
    'bootswatch_theme': "cerulean",
    'bootstrap_version': "3",
}
