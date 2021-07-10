
snakeobjects
============

.. image:: https://readthedocs.org/projects/snakeobjects/badge/?version=latest :target: https://snakeobjects.readthedocs.io/en/latest/?badge=latest :alt: Documentation Status


Overview
--------

**snakeobjects** is a workflow management framework based on ``snakemake`` that
uses an object-oriented abstraction of workflows. ``snakeobjects`` workflows
are easier to develop, to maintain and to adopt compared to the equivallent
workflows written in ``stanakemake``, but inherit all the powerful features of
``snakemake``. These include the portability, efficient resource usage, the
large expressive power due to the tight python integration, and the large
community of the ``snakemake`` users.

.. toctree::
    :maxdepth: 1

    gettingStarted
    tutorial
    examples
    documentation
    specialTopics
    terms
    sobjects
    snakemakeExt
    pythonUtils

.. rstTests (This is a comment)

Documentation
-------------

https://www.iossifovlab.com/snakeobjects

Source
------

https://github.com/iossifovlab/snakeobjects

Setting up the development environment
--------------------------------------

.. code-block:: bash

    git clone git@github.com:iossifovlab/snakeobjects.git
    cd snakeobjects
    conda env create environment.yml
    conda activate snakeobjectsDev
    pip install -e .

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
