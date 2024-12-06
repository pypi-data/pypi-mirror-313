from setuptools import setup

setup(
    name="wrap_technote",
    packages=["wrap_technote"],
    use_scm_version={"version_scheme": "post-release"},
    setup_requires=["setuptools_scm"],
    description="Code for the annual WRAP technical notes",
    long_description=open("README.md", mode="r").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/dew-waterscience/wrap_technote",
    author="DEW Water Science (Kent Inverarity)",
    author_email="kent.inverarity@sa.gov.au",
    license="All rights reserved @ DEW",
    classifiers=(
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering",
    ),
    keywords="science groundwater",
    install_requires=(
        "loguru",
        "matplotlib",
        "shapely",
        "pyshp",
        "jinja2",
        "click",
        "requests",
        "python-sa-gwdata>=0.5.4",
        "adjustText",
        "xlrd",
        "openpyxl",
        "pillow",  # conda
        "pyproj",
        "geopandas>=0.5.0",  # conda
        "scipy",
        "attrdict",
        "ausweather",
        "sageodata_db>=0.19",
        "dew_gwdata>=0.74",
    ),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "wraptn = wrap_technote.scripts.cli:wraptn",
            "wrap_run_waterlevels = wrap_technote.scripts.waterlevels:waterlevels",
            "wrap_run_salinities = wrap_technote.scripts.salinities:salinities",
            "wrap_run_rainfall = wrap_technote.scripts.rainfall:rainfall",
            "wrap_run_summaries = wrap_technote.scripts.summaries:summaries",
        ]
    },
)
