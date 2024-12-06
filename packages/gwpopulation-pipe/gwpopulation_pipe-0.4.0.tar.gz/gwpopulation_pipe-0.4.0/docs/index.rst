:code:`gwpopulation_pipe` provides a standardized interface to gravitational-wave popualtion inference
######################################################################################################

This is intended to be used with the command-line interface and limited support will be provided for directly calling the API.

.. automodule:: gwpopulation_pipe
    :members:

Installation
------------

The easiest way to install :code:`gwpopulation_pipe` is via :code:`pypi`

.. code-block:: console

  $ pip install gwpopulation_pipe

Examples
--------

Here are a few examples of how to use the command line interface.

.. toctree::
   :maxdepth: 1

   real-data
   simulation
   prior
   configuration
   customizing
   specifying-data
   specifying-models

.. currentmodule:: gwpopulation_pipe

API:
----

.. autosummary::
   :toctree: api
   :template: custom-module-template.rst
   :caption: API:
   :recursive:

    common_format
    data_analysis
    data_collection
    data_simulation
    main
    parser
    post_plots
    utils
    vt_helper

Citing
------

If this software is useful for your research, please cite


.. raw:: html

   <details>
   <summary><a>Bilby</a></summary>

.. code-block:: bibtex

    @ARTICLE{2019ApJS..241...27A,
           author = {{Ashton}, Gregory and {H{\"u}bner}, Moritz and {Lasky}, Paul D. and {Talbot}, Colm and {Ackley}, Kendall and {Biscoveanu}, Sylvia and {Chu}, Qi and {Divakarla}, Atul and {Easter}, Paul J. and {Goncharov}, Boris and {Hernandez Vivanco}, Francisco and {Harms}, Jan and {Lower}, Marcus E. and {Meadors}, Grant D. and {Melchor}, Denyz and {Payne}, Ethan and {Pitkin}, Matthew D. and {Powell}, Jade and {Sarin}, Nikhil and {Smith}, Rory J.~E. and {Thrane}, Eric},
            title = "{BILBY: A User-friendly Bayesian Inference Library for Gravitational-wave Astronomy}",
          journal = {\apjs},
         keywords = {gravitational waves, methods: data analysis, methods: statistical, stars: black holes, stars: neutron, Astrophysics - Instrumentation and Methods for Astrophysics, Astrophysics - High Energy Astrophysical Phenomena, General Relativity and Quantum Cosmology},
             year = 2019,
            month = apr,
           volume = {241},
           number = {2},
              eid = {27},
            pages = {27},
              doi = {10.3847/1538-4365/ab06fc},
    archivePrefix = {arXiv},
           eprint = {1811.02042},
     primaryClass = {astro-ph.IM},
           adsurl = {https://ui.adsabs.harvard.edu/abs/2019ApJS..241...27A},
          adsnote = {Provided by the SAO/NASA Astrophysics Data System}
    }

.. raw:: html

   </details>

   <details>
   <summary><a>GWPopulation</a></summary>

.. code-block::

    @ARTICLE{2019PhRvD.100d3030T,
           author = {{Talbot}, Colm and {Smith}, Rory and {Thrane}, Eric and {Poole}, Gregory B.},
            title = "{Parallelized inference for gravitational-wave astronomy}",
          journal = {\prd},
         keywords = {Astrophysics - Instrumentation and Methods for Astrophysics, Astrophysics - High Energy Astrophysical Phenomena, General Relativity and Quantum Cosmology},
             year = 2019,
            month = aug,
           volume = {100},
           number = {4},
              eid = {043030},
            pages = {043030},
              doi = {10.1103/PhysRevD.100.043030},
    archivePrefix = {arXiv},
           eprint = {1904.02863},
     primaryClass = {astro-ph.IM},
           adsurl = {https://ui.adsabs.harvard.edu/abs/2019PhRvD.100d3030T},
          adsnote = {Provided by the SAO/NASA Astrophysics Data System}
    }

.. raw:: html

   </details>

   <details>
   <summary><a>GWPopulation Pipe</a></summary>

.. code-block:: bibtex

    @ARTICLE{
        gwpop_pipe,
        title={GWPopulation pipe},
        DOI={10.5281/zenodo.5654673},
        publisher={Zenodo},
        author={Talbot, Colm},
        year={2021},
        month={Nov},
        url={https://git.ligo.org/RatesAndPopulations/gwpopulation_pipe}
    }

.. raw:: html

   </details>


Along with whatever paper introduced the data, models, or sampler used.
