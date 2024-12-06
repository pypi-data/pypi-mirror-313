"""
Functions for collecting input samples from a range of sources and computing
the fiducial prior for the appropriate parameters.

The module provides the `gwpopulation_pipe_collection` executable.

In order to use many of the other functions you will need a class that provides
various attributes specified in the `gwpopulation_pipe` parser.
"""

#!/usr/bin/env python3

import json
import os
import re

import glob
import h5py
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from bilby.core.utils import logger
from bilby_pipe.utils import convert_string_to_dict
from gwpopulation.backend import set_backend

from .data_simulation import simulate_posteriors
from .analytic_spin_prior import prior_chieff_chip_isotropic
from .parser import create_parser
from .utils import get_cosmology
from .vt_helper import dump_injection_data

matplotlib.rcParams["text.usetex"] = False


def euclidean_redshift_prior(redshift, cosmology="Planck15_LAL"):
    r"""
    Evaluate the redshift prior assuming a Euclidean universe.

    See Appendix C of `Abbott et al. <https://arxiv.org/pdf/1811.12940.pdf>`_.

    .. math::

        p(z) \propto d^2_L \frac{dd_L}{dz}

    Parameters
    ----------
    redshift: array_like
        The redshift values to evaluate the prior for.
    cosmology: str
        The name of the cosmology, default is `Planck15_LAL`

    """
    cosmo = get_cosmology(cosmology)

    luminosity_distance = cosmo.luminosity_distance(redshift)
    return luminosity_distance**2 * cosmo.dDLdz(redshift)


def euclidean_distance_prior(redshift):
    logger.warning(
        "The euclidean_distance_prior function is deprecated, "
        "use euclidean_redshift_prior instead."
    )
    return euclidean_redshift_prior(redshift)


def cosmological_redshift_prior(redshift, cosmology="Planck15_LAL"):
    r"""
    Evaluate the redshift prior assuming a cosmological universe.

    .. math::

        p(z) \propto \frac{4\pi}{1 + z}\frac{dV_C}{dz}

    Parameters
    ----------
    redshift: array_like
        The redshift values to evaluate the prior for.
    cosmology: str
        The name of the cosmology, default is `Planck15_LAL`

    """
    cosmo = get_cosmology(cosmology)

    return cosmo.differential_comoving_volume(redshift) * 4 * np.pi / (1 + redshift)


def distance_prior(redshift_prior, luminosity_distance, cosmology="Planck15_LAL"):
    r"""
    Calculate the prior on luminosity distance given a redshift prior assuming the given
    cosmology.

    .. math::

        p(d_L) = p(z)\frac{dz}{dd_L}

    Parameters
    ----------
    redshift_prior: callable
        The redshift prior function.
    luminosity_distance: array_like
        The luminosity distance values to evaluate the prior for.
    cosmology: str
        The name of the cosmology, default is `Planck15_LAL`

    """
    from wcosmo import available, z_at_value
    from wcosmo.utils import disable_units

    disable_units()
    cosmo = get_cosmology(cosmology)

    redshift = z_at_value(cosmo.luminosity_distance, luminosity_distance)
    return redshift_prior(redshift) / cosmo.dDLdz(redshift)


def aligned_spin_prior(spin):
    r"""
    The standard prior for aligned spin assuming the spin prior extends to maximal.

    .. math::

        p(\chi) = \frac{1}{2} \log(|\chi|)

    Parameters
    ----------
    spin: array_like
        The aligned spin values to evaluate the prior for.

    Returns
    -------
    prior: array_like
        The prior evaluated at the input spin.
    """
    return -np.log(np.abs(spin)) / 2


def primary_mass_to_chirp_mass_jacobian(samples):
    r"""
    Compute the Jacobian for the primary mass to chirp mass transformation.

    .. math::

        \frac{d m_c}{d m_1} = \frac{q^{3/5}}{(1 + q)^{1/5}}

    Parameters
    ----------
    samples: dict
        Samples containing `mass_1` and `mass_ratio`.

    Returns
    -------
    jacobian: array_like
        The Jacobian for the transformation.
    """
    return (1 + samples["mass_ratio"]) ** 0.2 / samples["mass_ratio"] ** 0.6


def replace_keys(posts):
    """
    Map the keys from legacy names to the `GWPopulation` standards.

    Parameters
    ----------
    posts: dict
        Dictionary of `pd.DataFrame` objects

    Returns
    -------
    new_posts: dict
        Updated posteriors.

    """
    _mapping = dict(
        mass_1="m1_source",
        mass_2="m2_source",
        mass_ratio="q",
        a_1="a1",
        a_2="a2",
        cos_tilt_1="costilt1",
        cos_tilt_2="costilt2",
        redshift="redshift",
        chi_eff="chi_eff",
        chi_p="chi_p",
    )
    new_posts = dict()
    for name in posts:
        post = posts[name]
        new = pd.DataFrame()
        for key in _mapping:
            if _mapping[key] in post:
                new[key] = post[_mapping[key]]
            elif key in post:
                new[key] = post[key]
            else:
                new[key] = 0
        new_posts[name] = new
    return new_posts


def evaluate_prior(posts, args, dataset, meta):
    """
    Evaluate the prior distribution for the input posteriors.

    Parameters
    ----------
    posts: dict
        Dictionary of `pd.DataFrame` objects containing the posteriors.
    args:
        Input args containing the prior specification.
    dataset: str
        The dataset label to evaluate the prior for (i.e. "O4a"). Should be a key in `args.sample_regex`.
    meta: dict
        The per-event metadata, including e.g., the cosmology used for the analysis.

    Returns
    -------
    posts: dict
        The input dictionary, modified in place.
    """
    if "redshift" in args.parameters or "luminosity_distance" in args.parameters:
        if args.distance_prior[dataset].lower() == "comoving":
            logger.info(
                "Using uniform in the comoving source frame distance prior for all events."
            )
            redshift_prior = cosmological_redshift_prior
        elif args.distance_prior[dataset].lower() == "euclidean":
            logger.info("Using Euclidean distance prior for all events.")
            redshift_prior = euclidean_redshift_prior
        elif args.distance_prior[dataset].lower() == "none":
            redshift_prior = lambda x, *args, **kwargs: x**0
        else:
            raise ValueError(f"Redshift prior {args.distance_prior} not recognized")
    else:
        logger.warning(
            f"No redshift and no luminosity distance present for {name}, cannot evaluate distance prior weight"
        )

    if args.mass_prior[dataset].lower() == "flat-detector-components":
        logger.info("Assuming flat in detector frame mass prior for all events.")
        if "mass_1_detector" in args.parameters:
            logger.debug(
                f"no (1+z) factor since the priors are now in detector coordinate"
            )
    elif args.mass_prior[dataset].lower() == "flat-detector-chirp-mass-ratio":
        logger.info("Assuming chirp mass prior for all events.")
    elif args.mass_prior[dataset].lower() not in ["flat-source-components", "none"]:
        raise ValueError(f"Mass prior {args.mass_prior[dataset]} not recognized.")

    if args.spin_prior[dataset].lower() == "component":
        logger.info("Assuming uniform in component spin prior for all events.")
    elif args.spin_prior[dataset].lower() != "none":
        raise ValueError(f"Spin prior {args.spin_prior[dataset]} not recognized.")

    if "mass_ratio" in args.parameters:
        logger.info(
            "Model is defined in terms of mass ratio, adjusting prior accordingly."
        )
    if "chirp_mass" in args.parameters or "chip_mass_detector" in args.parameters:
        logger.info(
            "Model is defined in terms of chirp mass, adjusting prior accordingly."
        )

    for name in posts:
        post = posts[name]
        cosmology = meta.get(name, dict()).get("cosmology", None)
        if cosmology is None:
            cosmology = "Planck15_LAL"
        logger.info(f"Using {cosmology} cosmology for {name}")
        post["prior"] = 1
        if "redshift" in args.parameters:
            post["prior"] *= redshift_prior(post["redshift"], cosmology=cosmology)
        elif "luminosity_distance" in args.parameters:
            post["prior"] *= distance_prior(
                redshift_prior, post["luminosity_distance"], cosmology=cosmology
            )

        if "mass_1" in args.parameters:
            if args.mass_prior[dataset].lower() == "flat-detector-components":
                post["prior"] *= (1 + post["redshift"]) ** 2
            elif args.mass_prior[dataset].lower() == "flat-detector-chirp-mass-ratio":
                post["prior"] /= (
                    post["mass_1"]
                    / (1 + post["redshift"])
                    * primary_mass_to_chirp_mass_jacobian(post)
                )
            if "mass_ratio" in args.parameters:
                post["prior"] *= post["mass_1"]
        elif "mass_1_detector" in args.parameters:
            if args.mass_prior[dataset].lower() == "flat-detector-chirp-mass-ratio":
                post["prior"] /= post[
                    "mass_1_detector"
                ] * primary_mass_to_chirp_mass_jacobian(post)
            if "mass_ratio" in args.parameters:
                post["prior"] *= post["mass_1_detector"]

        if "chirp_mass" in args.parameters or "chirp_mass_detector" in args.parameters:
            post["prior"] *= primary_mass_to_chirp_mass_jacobian(post)

        if args.spin_prior[dataset].lower() == "component":
            post["prior"] /= 4

        if "chi_eff" in args.parameters:
            if "chi_p" in args.parameters:
                post["prior"] *= prior_chieff_chip_isotropic(
                    post["chi_eff"], post["chi_p"], post["mass_ratio"]
                )
            else:
                logger.warning("chi_eff prior specified without chi_p.")

        if "chi_1" in args.parameters:
            post["prior"] *= aligned_spin_prior(post["chi_1"])
        if "chi_2" in args.parameters:
            post["prior"] *= aligned_spin_prior(post["chi_2"])

    return posts


def load_posterior_from_meta_file(filename, labels=None):
    """
    Load a posterior from a `PESummary` meta file. The poseterior samples are expected to follow Bilby naming conventions.

    Parameters
    ----------
    filename: str
    labels: list
        The labels to search for in the file in order of precedence.

    Returns
    -------
    posterior: pd.DataFrame
    meta_data: dict
        Dictionary containing the run label that was loaded.

    """
    _mapping = dict(
        chirp_mass="chirp_mass_source",
        mass_1="mass_1_source",
        mass_2="mass_2_source",
        chirp_mass_detector="chirp_mass",
        mass_1_detector="mass_1",
        mass_2_detector="mass_2",
        mass_ratio="mass_ratio",
        redshift="redshift",
        luminosity_distance="luminosity_distance",
        a_1="a_1",
        a_2="a_2",
        cos_tilt_1="cos_tilt_1",
        cos_tilt_2="cos_tilt_2",
        chi_1="spin_1z",
        chi_2="spin_2z",
        chi_eff="chi_eff",
        chi_p="chi_p",
    )
    load_map = dict(
        json=load_meta_file_from_json,
        h5=load_meta_file_from_hdf5,
        hdf5=load_meta_file_from_hdf5,
        dat=load_samples_from_csv,
    )
    if labels is None:
        labels = ["PrecessingSpinIMRHM", "PrecessingSpin"]
    if not os.path.exists(filename):
        raise FileNotFoundError(f"{filename} does not exist")
    extension = os.path.splitext(filename)[1][1:]
    _posterior, label, waveform, cosmology = load_map[extension](
        filename=filename, labels=labels
    )
    keys = [key for key, value in _mapping.items() if value in _posterior]
    posterior = pd.DataFrame({key: _posterior[_mapping[key]] for key in keys})
    _attempt_to_fill_posterior(posterior, cosmology)
    meta_data = dict(
        label=label,
        waveform=waveform,
        cosmology=cosmology,
    )
    logger.info(f"Loaded {label} from {filename}.")
    return posterior, meta_data


def _attempt_to_fill_posterior(posterior, cosmology=None):
    """
    Attempt to add missing variables to the posterior.
    This is mostly for CI testing where the data doesn't contain all the variables.
    """
    from wcosmo import available, z_at_value
    from wcosmo.utils import disable_units

    disable_units()
    if cosmology is None:
        cosmology = "Planck15_LAL"
    logger.info(f"Assuming {cosmology} cosmology")
    cosmo = get_cosmology(cosmology)

    if "redshift" in posterior and "luminosity_distance" not in posterior:
        posterior["luminosity_distance"] = cosmo.luminosity_distance(
            posterior["redshift"]
        )
    elif "luminosity_distance" in posterior and "redshift" not in posterior:
        posterior["redshift"] = z_at_value(
            cosmo.redshift, posterior["luminosity_distance"]
        )
    elif "redshift" not in posterior:
        return

    for var in ["mass_1", "mass_2", "chirp_mass"]:
        if var in posterior and f"{var}_detector" not in posterior:
            posterior[f"{var}_detector"] = posterior[var] * (1 + posterior["redshift"])
        elif f"{var}_detector" in posterior and var not in posterior:
            posterior[var] = posterior[f"{var}_detector"] / (1 + posterior["redshift"])


def load_meta_file_from_hdf5(filename, labels):
    """
    Load the posterior from a `hdf5` `PESummary` file.
    See `load_posterior_from_meta_file`.
    """
    new_style = True
    with h5py.File(filename, "r") as data:
        if "posterior_samples" in data.keys():
            new_style = False
            data = data["posterior_samples"]
        label = None
        for _label in labels:
            if _label in data.keys():
                label = _label
                break
        if label is None:
            for key in data.keys():
                if "posterior_samples" in data[key]:
                    label = key
                    break
        if label is None:
            raise ValueError(f"Could not find posterior samples in {filename}")
        try:
            cosmology = data[label]["meta_data"]["meta_data"]["cosmology"][0].decode()
        except (AttributeError, IndexError, KeyError):
            cosmology = None
        if new_style:
            posterior = pd.DataFrame(data[label]["posterior_samples"][:])
        elif hasattr(data[label], "keys"):
            posterior = pd.DataFrame(
                data[label]["samples"][:],
                columns=[key.decode() for key in data[label]["parameter_names"][:]],
            )
        else:
            posterior = pd.DataFrame(data[label][:])
        if "approximant" in data[label]:
            waveform = data[label]["approximant"][0].decode()
        else:
            waveform = ""
        return posterior, label, waveform, cosmology


def load_meta_file_from_json(filename, labels):
    """
    Load the posterior from a `json` `PESummary` file.
    See `load_posterior_from_meta_file`.
    """
    with open(filename, "r") as ff:
        data = json.load(ff)
    samples = data["posterior_samples"]
    del data
    label = list(samples.keys())[0]
    for _label in labels:
        if _label in samples:
            label = _label
            break
    try:
        cosmology = data[label]["meta_data"]["meta_data"]["cosmology"]
    except (AttributeError, IndexError, KeyError):
        cosmology = None
    posterior = pd.DataFrame(
        samples[label]["samples"], columns=samples[label]["parameter_names"]
    )
    return posterior, label, None, cosmology


def load_samples_from_csv(filename, *args, **kwargs):
    """
    Load posterior samples from a csd file.
    This is just a wrapper to `pd.read_csv` assuming tab separation.

    Parameters
    ----------
    filename: str
    args: unused
    kwargs: unused

    Returns
    -------
    posterior: `pd.DataFrame`
    meta_data: None
    cosmology: None
    """
    posterior = pd.read_csv(filename, sep="\t")
    return posterior, None, None, None


def _load_batch_of_meta_files(regex, label, labels=None, keys=None, ignore=None):
    if ignore is None:
        ignore = list()
    if keys is None:
        keys = [
            "mass_1",
            "mass_ratio",
            "a_1",
            "a_2",
            "cos_tilt_1",
            "cos_tilt_2",
            "chi_1",
            "chi_2",
            "redshift",
            "chi_eff",
            "chi_p",
        ]
    posteriors = dict()
    meta_data = dict()
    all_files = glob.glob(regex)
    all_files.sort()
    logger.info(f"Found {len(all_files)} {label} events in standard format.")
    for posterior_file in all_files:
        drop = False
        for label in ignore:
            if label in posterior_file:
                drop = True
                break
        if drop:
            logger.info(f"Ignoring {posterior_file}.")
            continue
        try:
            new_posterior, data = load_posterior_from_meta_file(
                posterior_file, labels=labels
            )
        except (TypeError, ValueError) as e:
            logger.info(f"Failed to load {posterior_file} with {type(e)}: {e}.")
            continue
        if all([key in new_posterior for key in keys]):
            meta_data[posterior_file] = data
            new_posterior = new_posterior[keys]
            if "mass_ratio" in new_posterior:
                new_posterior["mass_ratio"] = np.minimum(
                    new_posterior["mass_ratio"],
                    1 / new_posterior["mass_ratio"],
                )
            posteriors[posterior_file] = new_posterior
        else:
            logger.info(f"Posterior has keys {new_posterior.keys()}.")
    return posteriors, meta_data


def load_all_events(args, save_meta_data=True, ignore=None):
    """
    Load posteriors for some/all events.

    Parameters
    ----------
    args: argparse.Namespace
        Namespace containing the needed arguments, these are:
        - `sample_regex`: A dictionary of regex strings to search for the posterior files.
        - `preferred_labels`: A list of preferred labels to search for in the posterior files.
        - `parameters`: A list of parameters to extract from the posteriors.
        - `mass_prior`: The mass prior used in initial sampling.
        - `distance_prior`: The distance prior used in initial sampling.
        - `spin_prior`: The spin prior used in initial sampling.
        - `max_redshift`: The maximum redshift allowed in the sample.
    save_meta_data: bool
        Whether to write meta data about the loaded results to plain-text files.
    ignore: list
        List of strings to ignore in the file names to filter unwanted events.

    Returns
    -------
    posteriors: dict
        Dictionary of `pd.DataFrame` posteriors.
    """
    posteriors = dict()
    meta_data = dict()
    logger.info("Loading posteriors...")
    for label, regex in args.sample_regex.items():
        posts, meta = _load_batch_of_meta_files(
            regex=regex,
            label=label,
            labels=args.preferred_labels,
            keys=args.parameters,
            ignore=ignore,
        )
        posts = evaluate_prior(posts, args=args, dataset=label, meta=meta)
        posteriors.update(posts)
        meta_data.update(meta)
    if save_meta_data:
        with open(os.path.join(args.run_dir, "data", "event_data.json"), "w") as ff:
            json.dump(meta_data, ff)
    for key in args.parameters:
        for name in posteriors:
            if key not in posteriors[name]:
                raise KeyError(f"{key} not found for {name}")
    logger.info(f"Loaded {len(posteriors)} posteriors.")
    return posteriors


def plot_summary(posteriors: list, events: list, args):
    """
    Plot a summary of the posteriors for each parameter.

    Parameters
    ----------
    posteriors: list
        List of `pd.DataFrame` posteriors.
    events: list
        Names for each event.
    args
    """
    posteriors = posteriors[::-1]
    events = events[::-1]
    plot_dir = os.path.join(args.run_dir, "data")
    plot_parameters = args.parameters + ["prior"]
    n_cols = len(plot_parameters)
    fig, axes = plt.subplots(
        ncols=n_cols, figsize=(5 * n_cols, len(posteriors)), sharey=True
    )
    for parameter, axis in zip(plot_parameters, axes):
        data = [post[parameter] for post in posteriors]
        plt.sca(axis)
        plt.violinplot(data, vert=False)
        plt.xlabel(parameter.replace("_", " "))
        plt.xlim(np.min(data), np.max(data))
        if parameter == "prior":
            plt.xscale("log")
    plt.ylim(0.5, len(events) + 0.5)
    plt.yticks(np.arange(1, len(events) + 1), events, rotation=90)
    plt.tight_layout()
    plt.savefig(f"{plot_dir}/events.png")
    plt.close(fig)


def gather_posteriors(args, save_meta_data=True):
    """
    Load in posteriors from files according to the command-line arguments.

    Parameters
    ----------
    args: argparse.Namespace
        Command-line arguments
    save_meta_data: bool
        Whether to write meta data about the loaded results to plain-text files.

    Returns
    -------
    posts: list
        List of `pd.DataFrame` posteriors.
    events: list
        Event labels
    """
    posteriors = load_all_events(
        args, save_meta_data=save_meta_data, ignore=args.ignore
    )
    posts = list()
    events = list()
    filenames = list()
    for filename in posteriors.keys():
        event = re.findall(r"(GW\d{6}_\d{6}|S\d{6}[a-z]*|GW\d{6})", filename)[-1]
        if event in events:
            logger.warning(f"Duplicate event {event} found, ignoring {filename}.")
            continue
        posts.append(posteriors[filename])
        events.append(event)
        filenames.append(filename)
    if save_meta_data:
        logger.info(f"Outdir is {args.run_dir}")
        with open(
            f"{args.run_dir}/data/{args.data_label}_posterior_files.txt", "w"
        ) as ff:
            for event, filename in zip(events, filenames):
                ff.write(f"{event}: {filename}\n")
    n_samples = args.samples_per_posterior
    for post in posts:
        n_samples = min(len(post), n_samples)
    logger.info(f"Downsampling to {n_samples} samples per posterior")
    downsampled_posts = [
        post.sample(n_samples, random_state=args.collection_seed) for post in posts
    ]
    return downsampled_posts, events


def resolve_arguments(args):
    """
    - Make sure there are no incompatible arguments.
    - Resolve any deprecated arguments with their corresponding updates if possible.
    - Disable prior terms for parameters that aren't being fit.
    """
    if args.mass_prior.lower() == "flat-detector":
        logger.warning(
            "The 'flat-detector' mass prior specification is deprecated, "
            "use 'flat-detector-components' instead."
        )
        args.mass_prior = "flat-detector-components"
    elif args.mass_prior.lower() == "chirp-mass":
        logger.warning(
            "The 'chirp-mass' mass prior specification is deprecated, "
            "use 'flat-detector-chirp-mass-ratio' instead."
        )
        args.mass_prior = "flat-detector-chirp-mass-ratio"

    mass_parameters = {
        "mass_1",
        "mass_1_detector",
        "mass_2",
        "mass_2_detector",
        "chirp_mass",
        "chirp_mass_detector",
        "mass_ratio",
    }
    fitted_masses = mass_parameters.intersection(args.parameters)
    if len(fitted_masses) > 2:
        logger.warning(
            "More than two mass parameters specified, this may lead to issues with the prior."
        )
    elif len(fitted_masses) == 1:
        logger.warning(
            "Only one mass parameter specified, this may lead to issues with the prior."
        )
    elif len(fitted_masses) == 0:
        args.mass_prior = "None"

    if (
        "redshift" not in args.parameters
        and "luminosity_distance" not in args.parameters
    ):
        args.distance_prior = "None"

    spin_parameters = {
        "a_1",
        "a_2",
        "cos_tilt_1",
        "cos_tilt_2",
        "chi_1",
        "chi_2",
        "chi_eff",
        "chi_p",
    }
    fitted_spins = spin_parameters.intersection(args.parameters)
    if len(fitted_spins) == 0:
        args.spin_prior = "None"
    args.sample_regex = convert_arg_to_dict(args.sample_regex)
    prior_dict = {
        key: vars(args)[key] for key in ["mass_prior", "spin_prior", "distance_prior"]
    }
    for param in prior_dict:
        if "{" not in prior_dict[param]:
            prior_dict[param] = {
                dataset: prior_dict[param] for dataset in args.sample_regex
            }
        else:
            prior_dict[param] = convert_arg_to_dict(prior_dict[param])
    vars(args).update(prior_dict)


def convert_arg_to_dict(arg):
    """
    Convert a string argument to a dictionary. Not in-place.
    gwpopulation_pipe strips quotes from the regex string, so we need to add them back in,
    this assumes that there are no internal braces and spaces after all ':' and ','
    delimiting entries.

    Parameters
    ----------
    arg: str
        Arg that should be converted to a dictionary.

    Returns
    -------
    arg_dict: dict
        Dictionary representation of the input string.
    """
    try:
        regex_str = arg
        if '"' not in regex_str:

            regex_str = (
                regex_str.replace("{", '{"')
                .replace(":", '":"')
                .replace(", ", '", "')
                .replace("}", '"}')
                .replace(" ", "")
            )
        arg_dict = json.loads(regex_str)
    except json.decoder.JSONDecodeError:
        arg_dict = convert_string_to_dict(arg)
    return arg_dict


def main():
    parser = create_parser()
    args = parser.parse_args()
    resolve_arguments(args)

    set_backend("numpy")

    os.makedirs(f"{args.run_dir}/data", exist_ok=True)
    if args.injection_file is not None or args.sample_from_prior:
        posts = simulate_posteriors(args=args)
        events = [str(ii) for ii in range(len(posts))]
    else:
        posts, events = gather_posteriors(args=args)
    logger.info(f"Using {len(posts)} events, final event list is: {', '.join(events)}.")
    posterior_file = f"{args.data_label}.pkl"
    logger.info(f"Saving posteriors to {posterior_file}")
    filename = os.path.join(args.run_dir, "data", posterior_file)
    pd.to_pickle(posts, filename)
    if args.plot:
        plot_summary(posts, events, args)
    if args.vt_file is not None:
        dump_injection_data(args)
