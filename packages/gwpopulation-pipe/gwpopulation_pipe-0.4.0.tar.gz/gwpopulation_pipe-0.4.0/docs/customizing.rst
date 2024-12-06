Using custom models
###################

The recommended way to use a custom model is to create a package that contains the model and install it in the current environment.
There are instructions for creating a GWPopulation-compatible package `here <https://github.com/ColmTalbot/gwpopulation-additional-models>`_.
However, by the nature of population modelling, it is not always possible to have a pre-defined model for the population of
interest installed in the current environment.
For example, in order to use the OSG currently requires using an :code:`igwn-conda` environment, which has a significant lead time.
In this case, it is possible to read a custom model from a local file with :code:`gwpopulation_pipe`.
If using the :code:`HTCondor` file transfer mechanism, this is done by providing a python file that contains the model
using the :code:`--source-files` argument. If the file transfer mechanism is not being used, the file should be copied to the
working directory.

The file should contain a function in the format expected for :code:`Bilby` hyperparameter analyses.
There are a few requirements for the custom model:

- The first argument should be a dictionary of arrays whose keys are the names of the parameters.
- The additional arguments should explicitly name the parameters.
- The function should return the model probability density of the parameters.
- If the function explicitly uses :code:`numpy`-like functions, it should import :code:`xp` *inside* the function.
  If the import is outside the function, it may not adapt to calls to :code:`gwpopulation.set_backend`.
- Models can also be defined as a class, in which case, the :code:`__call__` method does not need to explicitly
  list the parameters, but the class should have a :code:`variable_names` attribute / property.

.. code-block:: python

    def my_custom_model(dataset, variable_1, ...):
        from gwpopulation.utils import xp
        prob = xp.sqrt(some_other_function(dataset["mass_1"], variable_1))
        return prob


    class MyCustomModel:
        variable_names = ["variable_1", ...]

        def __call__(self, dataset, **kwargs):
            from gwpopulation.utils import xp
            prob = xp.sqrt(some_other_function(dataset["mass_1"], kwargs["variable_1"]))
            return prob

    def some_other_function(mass, variable_1):
        return mass ** variable_1
