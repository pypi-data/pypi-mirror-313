Specifying data
###############

A crucial ingredient to any population analysis is the data. There are two
main forms of data that are used in population analyses:

- posterior samples for each of the observed events. We expect that these are provided
  in the :code:`PESummary` format.`
- simulated signals for quantifying the search sensitivity (sensitivity injections).

Posterior samples
-----------------
These are specified via the :code:`--sample-regex` argument which should be a dictionary
where the keys identify subsets of the events, e.g., grouped by observing run, and the values
are glob patterns for a set of result files.

Sometimes we wish to omit specific events from the analysis. This can be done by specifying
a list of events to omit via the :code:`--ignore` option. Each entry in this list is used as
a glob pattern against the event file names.

Each :code:`PESummary` result file often contains multiple results with different analysis choices.
To specify which result to use, you can provide a list with a precedence order of
:code:`--preferred-labels`. The first matching label is used to extract the posterior samples.
If there are no matches inside the file, the first set of samples that contains the desired parameters
is used.

Finally, the run time of the analysis may scale with the number of posterior samples used for each event.
To limit the number of samples used, you can specify a maximum number of samples to use via the
:code:`--samples-per-posterior` option.

Sensitivity injections
----------------------
These must be provided in one or more :code:`hdf5` files via the :code:`--vt-file` option.
If you have multiple files, you can specify a glob pattern to match all of the files.
These files are expected to match the format of sensitivity injections produced by
the LIGO-Virgo-Kagra collaboration.