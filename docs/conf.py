# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "py-ab-experiment"
copyright = "2024, gus-fr"
author = "[gus-fr](https://github.com/gus-fr)"
release = "0.2.0"

# -- extensions --

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "recommonmark",
    "sphinx.ext.viewcode",
    "autoapi.extension",
]
templates_path = ["_templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
# html_static_path = ["_static"]

# AutoApi settings


autoapi_type = "python"
autoapi_dirs = ["../src"]
autoapi_member_order = "groupwise"
autoapi_keep_files = False  # set to True to see temp files
autoapi_add_toctree_entry = True

autodoc_typehints = "signature"


def skip_sly(app, what, name, obj, skip, options):
    if name.startswith("pyab_experiment.sly") and what != "package":
        skip = True
    elif name.startswith("pyab_experiment.language") and what != "package":
        #    if what == "class" and "util" in name:
        skip = True
    return skip


def setup(sphinx):
    sphinx.connect("autoapi-skip-member", skip_sly)
