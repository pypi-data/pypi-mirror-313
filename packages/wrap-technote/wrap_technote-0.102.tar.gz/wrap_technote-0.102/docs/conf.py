project_name = "wrap_technote"


from pkg_resources import get_distribution

release = get_distribution(project_name).version
version = ".".join(release.split(".")[:2])

project = f"{project_name} documentation v{version}"
copyright = "2019-2022 DEW"
author = "Kent Inverarity"


extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.mathjax",
    "sphinx.ext.ifconfig",
    "sphinx.ext.viewcode",
    "sphinx.ext.githubpages",
    "sphinx.ext.napoleon",
    "nbsphinx",
]

templates_path = ["_templates"]

source_suffix = ".rst"
master_doc = "index"
language = "en"

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
pygments_style = None

html_theme = "sphinx_rtd_theme"

html_theme_options = {}

html_context = {
    "github_user": "dew-waterscience",
    "github_repo": project_name,
    "github_version": "main",
    "doc_path": "docs",
}

html_static_path = ["_static"]

html_css_files = [
    "css/custom.css",
]


html_sidebars = {
    # "**": ["search-field", "sidebar-nav-bs", "sidebar-ethical-ads"]
    # "**": ["search-field", "sidebar-nav-bs",]
    "**": [
        "search-field",
        "navbar-nav",
        "parent_links",
    ]
}


intersphinx_mapping = {
    "python": ("http://docs.python.org/", None),
    "pandas": ("https://pandas.pydata.org/pandas-docs/stable/", None),
    "sa_gwdata": ("https://python-sa-gwdata.readthedocs.io/en/latest/", None),
    # "sageodata_db": (
    #     "http://github.io/dew-waterscience/sageodata_db",
    #     "sageodata_db.objects.inv",
    # ),
    # "dew_gwdata": (
    #     "http://github.io/dew-waterscience/dew_gwdata",
    #     "dew_gwdata.objects.inv",
    # ),
    # "wrap_technote": (
    #     "http://github.io/dew-waterscience/wrap_technote",
    #     "wrap_technote.objects.inv",
    # ),
    # "waterkennect": (
    #     "http://github.io/dew-waterscience/waterkennect",
    #     "waterkennect.objects.inv",
    # ),
}
intersphinx_cache_limit = 1

# -- Options for todo extension ----------------------------------------------

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True


def setup(app):
    app.add_css_file("custom.css")


with open("../requirements.txt") as f:
    for line in f:
        if line.strip().startswith("sageodata_db"):
            sageodata_db_version = line.strip().split(">=")[1]
        if line.strip().startswith("dew_gwdata"):
            dew_gwdata_version = line.strip().split(">=")[1]


rst_epilog = "\n".join(
    [
        f".. |{tag_name}| replace:: {tag}"
        for tag_name, tag in [
            ("sageodata_db_version", sageodata_db_version),
            ("dew_gwdata_version", dew_gwdata_version),
        ]
    ]
)
