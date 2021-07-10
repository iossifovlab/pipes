.. _getting-started-label:

***************
Getting Started
***************

Installation
============

``snakeobjects`` is tested and works well on Linux and Mac; it doesn't work on
Windows. By far, the easiest method for installing ``snakeobjects`` is to use
the ``snakeobjects`` conda package available at the iossifovlab channel (SOON AT
bioconda!!). This method requires for conda or miniconda to be installed. (See
`Conda Installation
<https://docs.conda.io/projects/conda/en/latest/user-guide/install>`_).  With
conda ready, installing ``snakeobjects`` is simple::

    $ conda install -c iossifovlab -c bioconda -c conda-forge snakeobjects

Unfortunately, due to the large number of dependencies associated with
``snakemake`` this can take several minutes. After ``conda install`` finishes,
you can use the :option:`sobjects version` command to check  if the
installation was successful:

.. runblock:: console

    $ sobjects version

Hello world pipeline
====================

We will show how you can create and execute a small pipeline, and we will use
it to introduce some of the basic steps for working with ``snakeobjects``
projects and pipelines. 

Let's create a new directory to use both as a pipeline and as a project
directory.  The directory's location and name do not matter, but we will use
/tmp/helloWorld for the example below.  In this directory, you should create
three files. The first file should be called ``build_object_graph.py`` and
should contain the following two lines:

.. literalinclude:: helloWorld/build_object_graph.py

The second file should be called ``hello.snakefile`` and contain:

.. literalinclude:: helloWorld/hello.snakefile

Finally, the third file should be named ``so_project.yaml`` and should be
empty.  If you don't want to be bothered creating a directory, copying, and
pasting, you can instead download and extract (``tar xzf helloWorld.tgz``) the
files from :download:`helloWorld.tgz <./helloWorld.tgz>`.

The ``build_object_graph.py`` and the ``hello.snakefile`` files comprise our
pipeline.  The ``build_object_graph.py`` is a script that creates the object
graph for our project containing only one object with object type ``hello`` and
object id ``world``.  The ``hello.snakefile`` declares that objects of type
``hello`` have one target, ``result.txt``, and includes the rule to create such
a target.  The ``so_project.yaml`` file indicates that the directory will be
used as a ``snakeobjects`` project directory and will contain the results of
the pipeline's execution. 

With ``snakeobjects``, we execute a pipeline over a project in two steps:
:option:`sobjects prepare` and :option:`sobjects run`.  We perform both using
the ``sobjects`` command-line utility from within our project directory.

.. code-block:: bash

    $ cd /tmp/helloWorld

    $ sobjects prepare
    # WORKING ON PROJECT /tmp/helloWorld
    # WITH PIPELINE /tmp/helloWorld

    $ sobjects run -j -q
    # WORKING ON PROJECT /tmp/helloWorld
    # WITH PIPELINE /tmp/helloWorld
    UPDATING ENVIRONMENT:
    export SO_PROJECT=/tmp/helloWorld
    export SO_PIPELINE=/tmp/helloWorld
    export PATH=$SO_PIPELINE:$PATH
    RUNNING: snakemake -s /tmp/helloWorld/objects/.snakeobjects/main.snakefile -d /tmp/helloWorld/objects -j -q
    Job counts:
        count	jobs
        1	createResult
        1	so_all_targets
        1	so_hello_obj
        3

The :option:`sobjects prepare` performs a few initialization steps.
:option:`sobjects run` does the 'heavy lifting' using the ``snakemake`` to
execute the rules for creating the object targets. The execution of our
helloWorld pipeline should finish instantly, and we can find the file for the
result.txt target in the directory ``snakeobjects`` creates for our single
``hello/world`` object:

.. code-block:: bash

    $ cat /tmp/helloWorld/objects/hello/world/result.txt 
    hello world


What's next
===========

We strongly suggest that you examine our extensive :ref:`tutorial` next.
It introduces all the components necessary to design complex workflows and to
apply them to large projects.  You can find more examples in the
:ref:`examples`.  For a high-level overview of ``snakeobjects``, you should
read the ``snakeobjects`` paper [REF to come].  You can find a detailed
reference for all of the ``snakeobjects``' components in the rest of this
documentation package.

