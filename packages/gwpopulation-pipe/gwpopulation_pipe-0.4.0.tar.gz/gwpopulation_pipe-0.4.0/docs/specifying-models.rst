Specifying models
=================

In the configuration file, the models to be analyzed are specified using a :code:`JSON` string.
This string should be formatted as a dictionary where the keys describe the model or parameters the model
impacts and the values specify the models.
The specific choice of the model is only relevant for creating plots with :code:`gwpopulation_pipe_plot`
which recognizes :code:`{mass,magnitude,orientation,redshift}`.
The model specification can take one of the following formats:

- A string specifying the :code:`Python` import path for the model, e.g., `gwpopulation.models.spin.iid_spin`.
- A path to a :code:`JSON` file containing the model specification in a format that can be read using
  :code:`bilby.core.utils.io.decode_bilby_json`.
- One of a small number of hardcoded models. Note that this option will be removed and are only included for
  backwards compatibility.

For example :code:`{"spin": "gwpopulation.models.spin.iid_spin", "redshift": "redshift_model.json"}`.