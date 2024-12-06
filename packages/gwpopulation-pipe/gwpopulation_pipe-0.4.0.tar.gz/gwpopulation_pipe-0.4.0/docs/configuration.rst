Using gwpopulation_pipe
#######################

The format of :code:`gwpopulation_pipe` is based on the :code:`bilby_pipe` package.
The most important executables are:

- :code:`gwpopulation_pipe` - the main executable that builds a :code:`bash` script for local use
  and :code:`HTCondor` for submission to a computing cluster. If you're interested in :code:`SLURM`
  support please let us know.
- :code:`gwpopulation_pipe_collection` - reads in posterior samples for individual
  events and combines them into a single file containing the requested parameters and files containing
  data products used to estimate the search sensitivity, which are also downsampled.
- :code:`gwpopulation_pipe_analysis` - reads in the output of :code:`gwpopulation_pipe_collection`
  and performs the population analysis using :code:`Bilby` and/or :code:`numpyro`.
- :code:`gwpopulation_pipe_plot` - makes plots of the results of the population analysis.
- :code:`gwpopulation_pipe_to_common_format` - converts the result files to the common format for
  LVK population analyses.

:code:`gwpopulation_pipe` help
------------------------------

Other documentation pages describe how to specify some of these arguments in more detail, but
here is a brief overview of the command line arguments for :code:`gwpopulation_pipe`.

For reference, here is the full output of

.. code-block:: console

   $ gwpopulation_pipe --help

.. highlight:: none

.. argparse::
   :ref: gwpopulation_pipe.main.create_parser
   :prog: gwpopulation_pipe
   :noepilog:
