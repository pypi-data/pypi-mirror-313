# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import importlib
import inspect
import operator
import pathlib

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "XManager Slurm"
copyright = "2023, Jesse Farebrother"
author = "Jesse Farebrother"
repository = "https://github.com/jessefarebro/xm-slurm"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.linkcode",
    "sphinx.ext.autodoc.typehints",
    "sphinx.ext.napoleon",
]
autodoc_typehints = "both"

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


def linkcode_resolve(domain: str, info):
    assert domain == "py", "expected only Python objects"

    mod = importlib.import_module(info["module"])
    try:
        obj = operator.attrgetter(info["fullname"])(mod)
    except AttributeError:
        return None

    try:
        file = inspect.getsourcefile(obj)
        lines = inspect.getsourcelines(obj)
    except TypeError:
        # e.g. object is a typing.Union
        return None
    assert file is not None

    file = pathlib.Path(file).relative_to(pathlib.Path(__file__).parent.parent)
    start, end = lines[1], lines[1] + len(lines[0]) - 1

    return f"{repository}/tree/main/{file}#L{start}-L{end}"


def skip_submodules(app, what, name, obj, skip, options):
    if what == "module":
        skip = True
    if name.startswith("xm_slurm.packaging"):
        skip = True
    _, _, attr = name.rpartition(".")
    if attr.startswith("__") and attr.endswith("__"):
        skip = True
    return skip


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_theme_options = {
    "sidebar_hide_name": True,
}
html_static_path = ["_static"]
html_show_sphinx = False
