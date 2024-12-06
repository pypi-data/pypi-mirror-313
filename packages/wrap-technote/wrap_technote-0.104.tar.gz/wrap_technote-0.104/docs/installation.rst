############
Installation
############

Requirements
============

wrap_technote relies on some specific Python packages to be installed in order to
work. You will need to have an Anaconda Python Distribution installed. I recommend
using "mambaforge" for this - see instruction for installing this on DEW computers
here:

file:///P:/projects_gw/State/Groundwater_Toolbox/Python/wheels/docs/dew_ws_tools/latest_source/installing_python.html

Installing wrap_technote
========================

Once you have conda/mamba installed, you can run this in Command Prompt to install
wrap_technote and all its dependencies:

.. code-block:: none

    conda install -c dew-waterscience wrap_technote

(Substitute ``mamba`` for ``conda`` if you have mamba installed - if you don't know
what the difference is, just use the command above)

Updating the wrap_technote package
==================================

You can either install the latest version from Anaconda:

.. code-block:: none

    conda update -c dew-waterscience wrap_technote

Or you can update from PyPI:

.. code-block:: none

    pip install -U wrap_technote

