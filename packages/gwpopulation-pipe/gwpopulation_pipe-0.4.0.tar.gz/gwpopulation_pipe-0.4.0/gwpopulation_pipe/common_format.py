import os
from argparse import ArgumentParser

import dill
import h5py
import json
import numpy as np
from scipy.integrate import cumulative_trapezoid
import pandas as pd
from bilby.core.result import read_in_result
from bilby.core.utils import logger
from gwpopulation.backend import set_backend, SUPPORTED_BACKENDS
from gwpopulation.utils import to_numpy, xp
from tqdm import tqdm
from bilby_pipe.parser import StoreBoolean, nonestr

from .data_analysis import load_model
from .data_collection import evaluate_prior
from .utils import prior_conversion
from .vt_helper import load_injection_data


def create_parser():
    import wcosmo

    parser = ArgumentParser()
    parser.add_argument("-r", "--result-file", help="Bilby result file")
    parser.add_argument(
        "-s", "--samples-file", help="File containing single event samples"
    )
    parser.add_argument(
        "--injection-file",
        type=nonestr,
        help="File containing injections",
    )
    parser.add_argument("-f", "--filename", default=None, help="Output file name")
    parser.add_argument("--max-redshift", default=2.3, type=float)
    parser.add_argument("--minimum-mass", default=2, type=float)
    parser.add_argument("--maximum-mass", default=100, type=float)
    parser.add_argument(
        "--n-events", type=int, default=None, help="Number of events to draw"
    )
    parser.add_argument(
        "--n-samples",
        type=int,
        default=5000,
        help="The number of population samples to use, default=5000",
    )
    parser.add_argument(
        "--vt-ifar-threshold",
        type=float,
        default=1,
        help="IFAR threshold for resampling injections",
    )
    parser.add_argument(
        "--vt-snr-threshold",
        type=float,
        default=11,
        help="IFAR threshold for resampling injections. "
        "This is only used for O1/O2 injections",
    )
    parser.add_argument(
        "--distance-prior",
        default="euclidean",
        help="Distance prior format, e.g., euclidean, comoving",
    )
    parser.add_argument(
        "--mass-prior",
        default="flat-detector",
        help="Mass prior, only flat-detector is implemented",
    )
    parser.add_argument(
        "--spin-prior",
        default="component",
        help="Spin prior, this should be either component or gaussian",
    )
    parser.add_argument(
        "--backend",
        default="jax",
        choices=SUPPORTED_BACKENDS,
        help="The backend to use, default is jax",
    )
    parser.add_argument(
        "--cosmo", action="store_true", help="Whether to fit cosmological parameters."
    )
    parser.add_argument(
        "--cosmology",
        type=str,
        default="Planck15_LAL",
        help=(
            "Cosmology to use for the analysis, this should be one of "
            f"{', '.join(wcosmo.available.keys())}. Some of these are fixed pre-defined "
            "cosmologies while others are parameterized cosmologies. If a parameterized "
            "cosmology is used the parameters relevant parameters should be included "
            "in the prior specification."
        ),
    )
    parser.add_argument(
        "--make-popsummary-file",
        action=StoreBoolean,
        default=True,
        help="Whether to make a summary result file in popsummary format.",
    )
    parser.add_argument(
        "--event-data-file", default=None, help="File containing event metadata"
    )
    parser.add_argument(
        "--popsummary-file",
        default=None,
        help=(
            "Popsummary output .h5/.hdf5 file name. Defaults to "
            "'{result.outdir}/{result.label}_popsummary_result.h5' where `result` is a "
            "bilby.core.result.Result object read in under `--result-file`."
        ),
    )
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    set_backend(args.backend)

    result = read_in_result(args.result_file)
    n_samples = min(args.n_samples, len(result.posterior))
    all_samples = dict()
    posterior = result.posterior.sample(n_samples, replace=False)
    posterior = do_spin_conversion(posterior)
    all_samples["posterior"] = posterior

    with open(args.samples_file, "rb") as ff:
        samples = dill.load(ff)
    if "prior" not in samples["original"]:
        data = dict(original=samples["original"])
        evaluate_prior(data, args)
        samples.update(data)
    for key in samples["original"]:
        samples["original"][key] = xp.asarray(samples["original"][key])

    if args.n_events:
        n_draws = args.n_events
        logger.info(f"Number of draws set to {n_draws}.")
    else:
        n_draws = len(samples["names"])
        logger.info(f"Number of draws equals number of events, {n_draws}.")

    logger.info("Generating observed populations.")
    args.models = result.meta_data["models"]
    model = load_model(args)
    observed_dataset = resample_events_per_population_sample(
        posterior=posterior,
        samples=samples["original"],
        model=model,
        n_draws=len(samples["names"]),
    )

    for ii, name in enumerate(samples["names"]):
        new_posterior = pd.DataFrame()
        for key in observed_dataset:
            new_posterior[f"{name}_{key}"] = to_numpy(observed_dataset[key][:, ii])
        all_samples[name] = new_posterior

    if args.injection_file is None:
        logger.info("Can't generate predicted populations without VT file.")
    else:
        logger.info("Generating predicted populations.")
        args.models = result.meta_data["vt_models"]
        vt_data = load_injection_data(
            args.injection_file,
            ifar_threshold=args.vt_ifar_threshold,
            snr_threshold=args.vt_snr_threshold,
        ).to_dict()
        model = load_model(args)
        synthetic_dataset = resample_injections_per_population_sample(
            posterior=posterior,
            data=vt_data,
            model=model,
            n_draws=n_draws,
        )

        for ii in range(n_draws):
            new_posterior = pd.DataFrame()
            for key in synthetic_dataset:
                new_posterior[f"synthetic_{key}_{ii}"] = to_numpy(
                    synthetic_dataset[key][:, ii]
                )
            all_samples[f"synthetic_{ii}"] = new_posterior

    if args.filename is None:
        filename = os.path.join(result.outdir, f"{result.label}_full_posterior.hdf5")
    else:
        filename = args.filename
    save_to_common_format(
        posterior=all_samples, events=samples["names"], filename=filename
    )

    if args.make_popsummary_file:
        args.backend = "numpy"
        set_backend(args.backend)
        if args.popsummary_file is None:
            filename = os.path.join(
                result.outdir, f"{result.label}_popsummary_result.h5"
            )
        else:
            filename = args.popsummary_file
        with open(args.event_data_file, "r") as ff:
            event_meta_data = json.load(ff)
        args.models = result.meta_data["models"]
        model = load_model(args)
        save_to_popsummary_format(
            filename=filename,
            bilby_result=result,
            event_meta_data=event_meta_data,
            reweighted_samples=all_samples,
            model=model,
            maximum_mass=args.maximum_mass,
            minimum_mass=args.minimum_mass,
            max_redshift=args.max_redshift,
        )


def do_spin_conversion(posterior):
    """Utility function to convert between beta distribution parameterizations."""
    original_keys = list(posterior.keys())
    posterior = prior_conversion(posterior)
    for key in ["amax", "amax_1", "amax_2"]:
        if key not in original_keys and key in posterior:
            del posterior[key]
    return posterior


def save_to_common_format(posterior, events, filename):
    """
    Save the data to the common hdf5 format.

    Parameters
    ----------
    posterior: [np.ndarray, pd.DataFrame]
        The posterior to be saved.
    events: list
        The names of each of the events in the dataset.
    filename: str
        the output filename

    """
    for key in posterior:
        if isinstance(posterior[key], pd.DataFrame):
            posterior[key] = data_frame_to_sarray(posterior[key])
    events = [event.encode() for event in events]
    logger.info(f"Writing data to {filename}")
    with h5py.File(filename, "w") as ff:
        for key in posterior:
            ff[f"samples/{key}"] = posterior[key]
        ff["events"] = events


def read_common_format(filename, data_format="numpy"):
    """
    Read a posterior file in the common format

    Parameters
    ----------
    filename: str
        The path to the file to read.
    data_format: str
        The format to return the data in, can be either `numpy` or `pandas`.

    Returns
    -------
    output: [np.ndarray, pd.DataFrame]
        The posterior in the requested format.
    events: list
        The event names.
    """
    with h5py.File(filename, "r") as ff:
        data = {key: ff["samples"][key][:] for key in ff["samples"]}
        events = [event.decode() for event in ff["events"]]
    if data_format == "numpy":
        return data, events
    elif data_format == "pandas":
        output = dict()
        for key in data:
            data_frame = pd.DataFrame()
            for name in data[key].dtype.names:
                data_frame[name] = data[key][name]
            output[key] = data_frame
        return output, events
    else:
        raise ValueError(f"Data format {data_format} not implemented.")


def resample_events_per_population_sample(posterior, samples, model, n_draws):
    """
    Resample the input posteriors with a fiducial prior to the population
    informed distribution. This returns a single sample for each event for
    each passed hyperparameter sample.

    See, e.g., section IIIC of `Moore and Gerosa <https://arxiv.org/abs/2108.02462>`_
    for a description of the method.

    Parameters
    ----------
    posterior: pd.DataFrame
        Hyper-parameter samples to use for the reweighting.
    samples: dict
        Posterior samples with the fiducial prior.
    model: bilby.hyper.model.Model
        Object that implements a `prob` method that will calculate the population
        probability.
    n_draws: int
        The number of samples to draw. This should generally be the number of events.
        This will return one sample per input event.

    Returns
    -------
    observed_dataset: dict
        The observed dataset of the events with the population informed prior.
    """
    from .utils import maybe_jit

    @maybe_jit
    def extract_choices(parameters, seed=None):
        model.parameters.update(parameters)
        if hasattr(model, "cosmology_names"):
            data, jacobian = model.detector_frame_to_source_frame(samples, **parameters)
        else:
            data = samples
            jacobian = 1
        weights = model.prob(data) / data["prior"] / jacobian
        weights = (weights.T / xp.sum(weights, axis=-1)).T
        if "jax" in xp.__name__:
            seeds = random.split(random.PRNGKey(seed), len(weights))
            choices = [
                random.choice(seeds[ii], len(weights[ii]), p=weights[ii])
                for ii in range(n_draws)
            ]
        else:
            choices = [
                random.choice(
                    len(weights[ii]),
                    p=weights[ii],
                    size=1,
                ).squeeze()
                for ii in range(n_draws)
            ]
        return xp.asarray(choices)

    points = posterior.to_dict(orient="records")
    if "jax" in xp.__name__:
        from jax import random

        seeds = np.random.choice(100000, len(posterior))
    else:
        random = xp.random
        seeds = [None] * len(posterior)
    inputs = list(zip(points, seeds))
    all_choices = xp.asarray(
        [extract_choices(point, seed) for point, seed in tqdm(inputs)]
    )

    @maybe_jit
    def resample(samples, choices):
        return xp.asarray([samples[ii, choice] for ii, choice in enumerate(choices)])

    observed_dataset = dict()
    for key in samples:
        observed_dataset[key] = to_numpy(
            xp.asarray([resample(samples[key], choices) for choices in all_choices])
        )
    return observed_dataset


def resample_injections_per_population_sample(posterior, data, model, n_draws):
    """
    Resample the input data with a fiducial prior to the population
    informed distribution. This returns a fixed number of samples for
    each passed hyperparameter sample.

    This is designed to be used with found injections.

    See, e.g., section IIIC of `Moore and Gerosa <https://arxiv.org/abs/2108.02462>`_
    for a description of the method.

    Parameters
    ----------
    posterior: pd.DataFrame
        Hyper-parameter samples to use for the reweighting.
    data: dict
        Input data samples to be reweighted.
    model: bilby.hyper.model.Model
        Object that implements a `prob` method that will calculate the population
        probability.
    n_draws: int
        The number of samples to draw. This should generally be the number of events.
        This will return one sample per input event.

    Returns
    -------
    observed_dataset: dict
        The observed dataset of the input data with the population informed prior.
    """
    from .utils import maybe_jit

    @maybe_jit
    def extract_choices(parameters, seed):
        model.parameters.update(parameters)
        if hasattr(model, "cosmology_names"):
            samples, jacobian = model.detector_frame_to_source_frame(data, **parameters)
        else:
            samples = data
            jacobian = 1
        weights = model.prob(samples) / samples["prior"] / jacobian
        weights /= xp.sum(weights)
        if "jax" in xp.__name__:
            choices = choice(
                PRNGKey(seed),
                len(weights),
                p=weights,
                shape=(n_draws,),
                replace=False,
            )
        else:
            weights = to_numpy(weights)
            choices = choice(len(weights), p=weights, size=n_draws, replace=False)
        return choices

    if "jax" in xp.__name__:
        from jax.random import PRNGKey, choice

        seeds = np.random.choice(100000, len(posterior))
    else:
        # FIXME: cupy.random.choice doesn't support p != None and replace=False
        # cupy==13.0.0 (240202)
        from numpy.random import choice

        seeds = [None] * len(posterior)
    points = posterior.to_dict(orient="records")
    inputs = list(zip(points, seeds))
    all_choices = to_numpy(
        xp.asarray([extract_choices(point, seed) for point, seed in tqdm(inputs)])
    )

    @maybe_jit
    def resample(data, choices):
        """
        For some reason even this simple function significantly benefits from jit
        """
        return data[choices]

    synthetic_dataset = dict()
    for key in data:
        if not isinstance(data[key], xp.ndarray):
            continue
        synthetic_dataset[key] = xp.asarray(
            [resample(data[key], choices) for choices in all_choices]
        )
    return synthetic_dataset


def data_frame_to_sarray(data_frame):
    """
    Convert a pandas DataFrame object to a numpy structured array.
    This is functionally equivalent to but more efficient than
    `np.array(df.to_array())`.

    lifted from https://stackoverflow.com/questions/30773073/save-pandas-dataframe-using-h5py-for-interoperabilty-with-other-hdf5-readers

    Parameters
    -----------
    data_frame: pd.DataFrame
        the data frame to convert

    Returns
    -------
    output: np.ndarray
        a numpy structured array representation of df
    """

    types = [
        (data_frame.columns[index], data_frame[key].dtype.type)
        for (index, key) in enumerate(data_frame.columns)
    ]
    dtype = np.dtype(types)
    output = np.zeros(data_frame.values.shape[0], dtype)
    for (index, key) in enumerate(output.dtype.names):
        output[key] = data_frame.values[:, index]
    return output


def save_to_popsummary_format(
    filename,
    bilby_result,
    event_meta_data,
    reweighted_samples,
    model,
    maximum_mass,
    minimum_mass,
    max_redshift,
):
    """
    Saves all data products to a single hdf5 file in popsummary format.
    See https://git.ligo.org/christian.adamcewicz/popsummary and, specifically,
    https://git.ligo.org/christian.adamcewicz/popsummary/-/blob/main/examples/tutorial.ipynb
    for more information on reading and writing to popsummary format.

    Parameters
    -----------
    filename: str
        filename for the popsummary result (must be .h5/.hdf5)
    bilby_result: bilby.core.result.Result
        result object in bilby format
    event_meta_data: dict
        dictionary containing `approximant` and `label` for each event
    reweighted_samples: dict
        dictionary containing reweighted posteriors and injections
    model: bilby.hyper.model.Model
        population model for computing fair population draws
    maximum_mass: float
        maximum mass to sample from for fair population draws
    minimum_mass: float
        minimum mass to sample from for fair population draws
    max_redshift: float
        maximum redshift to sample from for fair population draws
    """
    from popsummary.popresult import PopulationResult

    logger.info("Saving to popsummary file:\n" f"   {filename}")
    result = PopulationResult(fname=filename)

    meta_data = dict()
    meta_data["hyperparameters"] = list(bilby_result.posterior.keys())
    meta_data["hyperparameter_latex_labels"] = []
    for key in meta_data["hyperparameters"]:
        if (
            key in bilby_result.priors.keys()
            and bilby_result.priors[key].latex_label is not None
        ):
            meta_data["hyperparameter_latex_labels"].append(
                bilby_result.priors[key].latex_label
            )
        elif key in COMMON_KEYS:
            meta_data["hyperparameter_latex_labels"].append(COMMON_KEYS[key])
        else:
            meta_data["hyperparameter_latex_labels"].append(key)
    meta_data["model_names"] = list(bilby_result.meta_data["models"].values())
    meta_data["model_names"].extend(
        [f"vt:{vt_model}" for vt_model in bilby_result.meta_data["vt_models"].values()]
    )
    meta_data["events"] = bilby_result.meta_data["event_ids"]
    meta_data["event_waveforms"] = []
    meta_data["event_sample_IDs"] = []
    for event in meta_data["events"]:
        key = list(event_meta_data.keys())[
            np.flatnonzero(np.char.find(list(event_meta_data.keys()), event) != -1)[0]
        ]
        meta_data["event_waveforms"].append(event_meta_data[key]["waveform"])
        meta_data["event_sample_IDs"].append(event_meta_data[key]["label"])
    meta_data["event_parameters"] = bilby_result.meta_data["parameters"]
    for key in meta_data.keys():
        result.set_metadata(key, meta_data[key], overwrite=True)

    hyperparameter_samples = np.array(
        [bilby_result.posterior[param] for param in meta_data["hyperparameters"]]
    ).T
    result.set_hyperparameter_samples(hyperparameter_samples, overwrite=True)

    for key in ["mass", "magnitude", "orientation", "redshift", "chi_eff_chi_p"]:
        try:
            with open(
                os.path.join(
                    bilby_result.outdir, f"{bilby_result.label}_{key}_data.h5"
                ),
                "rb",
            ) as ff:
                rates_data = dill.load(ff)
            for param in rates_data["lines"].keys():
                result.set_rates_on_grids(
                    param,
                    grid_params=param,
                    positions=rates_data["positions"][param],
                    rates=rates_data["lines"][param],
                    overwrite=True,
                )
        except FileNotFoundError:
            logger.info(
                f"Could not load gridded {key} rates. "
                f"This data will be absent from the popsummary output."
            )

    fair_population_draws = rejection_sample_population(
        model,
        meta_data["event_parameters"],
        bilby_result.posterior,
        maximum_mass,
        minimum_mass,
        max_redshift,
    )
    result.set_fair_population_draws(fair_population_draws, overwrite=True)

    reweighted_event_samples = []
    for event in meta_data["events"]:
        _reweighted_event_samples = np.array(
            [
                reweighted_samples[event][f"{event}_{param}"]
                for param in meta_data["event_parameters"]
            ]
        ).T
        reweighted_event_samples.append(_reweighted_event_samples[None, :, :])
    result.set_reweighted_event_samples(
        np.array(reweighted_event_samples), overwrite=True
    )

    reweighted_injections = []
    for key in reweighted_samples.keys():
        if "synthetic" in key:
            catalog = key.replace("synthetic_", "")
            _reweighted_injections = np.array(
                [
                    reweighted_samples[key][f"synthetic_{param}_{catalog}"]
                    for param in meta_data["event_parameters"]
                ]
            ).T
            reweighted_injections.append(_reweighted_injections)
    reweighted_injections = np.array(reweighted_injections)
    if reweighted_injections.ndim == 3:
        result.set_reweighted_injections(
            np.array(reweighted_injections)[None, :, :, :], overwrite=True
        )


def rejection_sample_population(
    model,
    params,
    posterior,
    maximum_mass,
    minimum_mass,
    max_redshift,
    draws_per_hypersample=1,
    batch_size=int(1e4),
    maxit=int(1e2),
):
    """
    Rejection sampling for `fair_population_draws` in popsummary output.

    Parameters
    -----------
    model: bilby.hyper.model.Model
        population model to draw from
    params: list
        names of the event-level parameters being modelled
    posterior: pandas.DataFrame
        data frame of hypersamples
    maximum_mass: float
        maximum mass to sample from
    minimum_mass: float
        minimum mass to sample from
    max_redshift: float
        maximum redshift to sample from
    draws_per_hypersample: int
        number of samples to draw per hypersample
    batch_size: int
        batch size to draw potential samples with
    maxit: int
        maximum number of iterations to attempt drawing `batch_size` samples
        in order to achieve `draws_per_hypersample` cumulative accepted samples

    Returns
    -----------
    population_draws: np.array
        array of samples from the population model with shape
        (draws_per_hypersample, number_of_hypersamples, number_of_event_dimensions)
    """
    param_lims = dict(
        mass_1=[minimum_mass, maximum_mass],
        mass_2=[minimum_mass, maximum_mass],
        mass_ratio=[minimum_mass / maximum_mass, 1],
        redshift=[1e-6, max_redshift],
        a_1=[0, 1],
        a_2=[0, 1],
        cos_tilt_1=[-1, 1],
        cos_tilt_2=[-1, 1],
        chi_1=[-1, 1],
        chi_2=[-1, 1],
        chi_eff=[-1, 1],
        chi_p=[0, 1],
    )

    def get_samples(n):
        return {
            param: np.random.uniform(param_lims[param][0], param_lims[param][1], n)
            for param in params
        }

    def accept(hypersample, samples, n):
        model.parameters.update(hypersample)
        probs = model.prob(samples)
        return np.random.uniform(0, max(probs), n) < probs

    logger.info("Rejection sampling population draws...")
    population_draws = {param: [] for param in params}
    for i in tqdm(range(len(posterior))):
        hypersample = posterior.iloc[i]
        accepted_draws = {param: np.array([]) for param in params}
        for ii in range(maxit):
            proposed_draws = get_samples(batch_size)
            accepted = accept(hypersample, proposed_draws, batch_size)
            for param in params:
                accepted_draws[param] = np.append(
                    accepted_draws[param], proposed_draws[param][accepted]
                )
            if len(accepted_draws[params[0]]) >= draws_per_hypersample:
                break
        if len(accepted_draws[params[0]]) < draws_per_hypersample:
            logger.info(
                f"Failed to accept {draws_per_hypersample} (accepted "
                f"{len(accepted_draws[params[0]])}) from {maxit*batch_size} "
                f"proposals with hyperparameters:\n   {hypersample}"
            )
        for param in params:
            population_draws[param].append(
                accepted_draws[param][:draws_per_hypersample]
            )

    return np.array([population_draws[param] for param in params]).T


COMMON_KEYS = dict(
    log_likelihood="$\ln \mathcal{L}$",
    log_prior="$\ln \pi$",
    rate="$\mathcal{R}$",
    log_10_rate="$\log_{10} \mathcal{R}$",
)
