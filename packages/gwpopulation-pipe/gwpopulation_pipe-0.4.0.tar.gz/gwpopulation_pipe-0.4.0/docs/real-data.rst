Analyzing public parameter estimation samples up to GWTC-3
##########################################################

The primary use case for :code:`gwpopulation_pipe` is analyzing the gravitational-wave transient catalog (GWTC).

This will generate results equivalent to a subset of the result in the LIGO-Virgo-Kagra astrophysical distributions paper accompanying GWTC-3.

.. warning::
   This example was written using :code:`gwpopulation_pipe==0.3.2` and may not work with the latest version of the code.

First, we need to obtain various pieces of data.

Downloading single-event fiducial posterior samples
===================================================

The samples from each version of GWTC are available individually.
The following samples will download the data and unpack them into individual directories.
They can also be manually downloaded for `GWTC-1 <https://dcc.ligo.org/LIGO-P1800370/public>`_,
`GWTC-2 <https://dcc.ligo.org/LIGO-P2000217/public>`_ and `GWTC-3 <zenodo.org/record/5546663>`_.

.. literalinclude:: ../example/fetch-all-samples.sh
   :language: bash

.. warning::
   This will download > 20 GB of data.

Download sensitivity data products
==================================

The sensitivity of the gravitational-wave detector network is assessed using simulated signals that are injected into
the data stream and recovered with the same search pipelines that identify real gravitational-wave signals.
Since for this example we're just looking at binary black hole systems we will only download the data relevant to those systems.

.. code-block:: console

   $ wget -nc https://zenodo.org/record/5636816/files/o1%2Bo2%2Bo3_bbhpop_real%2Bsemianalytic-LIGO-T2100377-v2.hdf5

Additional sensitivity products for other classes of system can also be
`downloaded <https://zenodo.org/record/5636816>`_ from the same location.

Setup the configuration file
============================

Now we can write our configuration file :code:`gwtc3-bbh.ini` for :code:`gwpopulation_pipe`.

.. raw:: html

   <details>
   <summary><a>Configuration file</a></summary>

.. literalinclude:: ../example/gwtc3-bbh.ini
  :language: ini

.. raw:: html

   </details>

This references a prior file which should contain the following

.. raw:: html

   <details>
   <summary><a>Prior file</a></summary>

.. literalinclude:: ../example/gwtc3-bbh.prior
  :language: python

.. raw:: html

   </details>

Arbitrary models can be passed as python paths, e.g.,
:code:`my_population_inference_package.my_population_inference_model`.
The only limitation is that this function must follow the standard format for input arguments an return values, e.g.,

.. code-block:: python

   def my_population_inference_model(dataset, parameter_1, parameter_2, parameter_3):
       return (dataset["mass_1"] / parameter_1) ** parameter_2 + parameter_3

Using custom population models may make some of the output filenames a little clunky.

Run :code:`gwpopulation_pipe`
=============================

Running the following will set up everything needed to perform the analysis.

.. code-block:: console

   $ gwpopulation_pipe gwtc3-bbh.ini

   12:49 bilby_pipe INFO    : dag file written to GWTC-3/submit/o1o2o3.dag
   12:49 bilby_pipe INFO    : shell script written to GWTC-3/submit/o1o2o3.sh
   12:49 bilby_pipe INFO    : Now run condor_submit_dag GWTC-3/submit/o1o2o3.dag

The three lines of output will direct you to the :code:`submit` directory that contains a :code:`bash` script with all
of the required commands and also files required to submit to a cluster running the :code:`HTCondor` schedule manager.
If you are running the jobs locally you can just call

.. code-block:: console

   $ bash GWTC-3/submit/o1o2o3.sh

to run all of the required stages in serial.

If these jobs run to completion you should see a set of results in the :code:`result` and :code:`summary` directories.