HTTomo (High Throughput Tomography pipeline)
*******************************************************

HTTomo is a user interface (UI) written in Python for fast big data processing using MPI protocols. 
It orchestrates I/O data operations and enables processing on a CPU and/or a GPU. HTTomo utilises other libraries, such as `TomoPy <https://tomopy.readthedocs.io>`_ and `HTTomolibgpu <https://github.com/DiamondLightSource/httomolibgpu>`_
as backends for data processing. The methods from the libraries are exposed through YAML templates to enable fast task programming.

Documentation
==============
Please check the full documentation `here <https://diamondlightsource.github.io/httomo/>`_.

Install HTTomo as a pre-built conda package
======================================================
.. code-block:: console

   $ conda create --name httomo # create a fresh conda environment
   $ conda activate httomo
   $ conda install -c conda-forge -c https://conda.anaconda.org/httomo/ httomo
   $ conda install -c https://conda.anaconda.org/httomo/ httomolibgpu # for GPU methods

Note: we recommend using `mamba <https://anaconda.org/conda-forge/mamba>`_ for a much faster dependency resolution.
After creating a fresh environment and activating it, install `mamba` with

.. code-block:: console

   $ conda install -c conda-forge mamba

And install the packages using :code:`mamba` instead (replace :code:`conda` with :code:`mamba`):

.. code-block:: console

   $ mamba install -c conda-forge -c https://conda.anaconda.org/httomo/ httomo


Install as a Python module
======================================================
.. code-block:: console
    
   $ git clone git@github.com:DiamondLightSource/HTTomo.git # clone the repo
   $ conda env create --name httomo --file conda/environment.yml # install dependencies
   $ conda activate httomo # activate environment
   $ pip install .[tomopy,httomolib,httomolibgpu] # Install the module + backend(s)

Setup HTTomo development environment:
======================================================
.. code-block:: console

   $ pip install -e .[dev] # development mode 

Running the code:
======================================================

* Install the module as described in "Install as a Python module"
* Execute the python module with :code:`python -m httomo <args>`
* For help with the command line interface, execute :code:`python -m httomo --help`

An example of running the code with test data:
==============================================

* Create an output directory :code:`mkdir output_dir/`
* Go to the home directory and run: :code:`python -m httomo run tests/test_data/tomo_standard.nxs samples/pipeline_template_examples/02_basic_cpu_pipeline_tomo_standard.yaml output_dir/`

An example of running validation on a YAML pipeline file
========================================================
* :code:`python -m httomo check samples/pipeline_template_examples/02_basic_cpu_pipeline_tomo_standard.yaml`

Release Tagging Scheme
======================

We use the `setuptools-git-versioning <https://setuptools-git-versioning.readthedocs.io/en/stable/index.html>`_
package for automatically determining the version from the latest git tag.
For this to work, release tags should start with a :code:`v` followed by the actual version,
e.g. :code:`v1.1.0a`.
We have setup a  :code:`tag_filter` in :code:`pyproject.toml` to filter tags following this pattern.
