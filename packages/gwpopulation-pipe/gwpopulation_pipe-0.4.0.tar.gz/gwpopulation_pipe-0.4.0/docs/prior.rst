Analyzing simulated non-informative posteriors
==============================================

A powerful test of population inference is to use non-information posteriors (i.e., prior samples) as the input.
If the analysis is unbiased, we should recover the prior distribution on our hyperparameters.

We can perform such an analysis with the following bash script.

.. literalinclude:: ../example/prior_sample.sh
  :language: bash

.. note::
  In this example, we use the :code:`pymultinest` sampler rather than the default :code:`dynesty`.
  This does not install automatically with :code:`gwpopulation_pipe`, however it can be simply installed with

  .. code-block:: bash

     $ conda install -c conda-forge pymultinest

  :code:`pymultinest` can't be simply installed using :code:`pypi` as it relies on the :code:`fortran` package :code:`MultiNest`.

This will create a directory :code:`prior` with two subdirectories :code:`data` and :code:`result`.
The :code:`data` directory contains the simulated posterior and violin plots of the input parameters.
The :code:`result` directory contains the output of the sampler and various plots produced in post-processing.