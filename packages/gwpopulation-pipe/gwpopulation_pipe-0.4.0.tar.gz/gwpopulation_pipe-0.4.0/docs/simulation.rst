Analyzing simulated posteriors
==============================

A standard test of population inference is to analyze a simulated population to verify that we can recover the true population.
The optimal way to do this is to run full parameter estimation on signals injected into real interferometer noise.
However, to reduce the computational cost, :code:`gwpopulation_pipe` implements a simple method for generating Gaussian
posteriors based on a specified population model.

We can perform such an analysis with the following bash script.

.. literalinclude:: ../example/simulations.sh
  :language: bash

.. note::
  In this example, we use the :code:`pymultinest` sampler rather than the default :code:`dynesty`.
  This does not install automatically with :code:`gwpopulation_pipe`, however it can be simply installed with

  .. code-block:: bash

     $ conda install -c conda-forge pymultinest

  :code:`pymultinest` can't be simply installed using :code:`pypi` as it relies on the :code:`fortran` package :code:`MultiNest`.

The file :code:`samples.json` contains the true values of the hyperparameters to simulate the universe for.
This should be in a format that can be read in with :code:`pandas.read_json`.

.. literalinclude:: ../example/samples.json
  :language: json

This will create a directory :code:`simulation` with two subdirectories :code:`data` and :code:`result`.
The :code:`data` directory contains the simulated posterior and violin plots of the input parameters.
The :code:`result` directory contains the output of the sampler and various plots produced in post-processing.