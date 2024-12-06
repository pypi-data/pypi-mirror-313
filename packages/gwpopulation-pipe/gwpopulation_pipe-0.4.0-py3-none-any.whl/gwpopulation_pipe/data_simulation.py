"""
Functions for generating simulated event posteriors.
The simulated posteriors will not accurately represent real observational uncertainties.

The module provides the `gwpopulation_pipe_simulate_posteriors` executable.

In order to use the primary function you will need a class that provides
various attributes specified in the `gwpopulation_pipe` parser.
"""

import os
import sys

import numpy as np
import pandas as pd
from bilby.core.prior import TruncatedGaussian
from bilby.core.utils import logger
from bilby.gw.cosmology import get_cosmology
from bilby.gw.prior import UniformSourceFrame
from gwpopulation.backend import set_backend
from gwpopulation.conversions import convert_to_beta_parameters
from gwpopulation.utils import to_numpy, xp

from .data_analysis import load_model, load_vt
from .main import MASS_MODELS
from .main import create_parser as create_main_parser

BOUNDS = dict(
    mass_1=(2, 100),
    mass_ratio=(0, 1),
    a_1=(0, 1),
    a_2=(0, 1),
    cos_tilt_1=(-1, 1),
    cos_tilt_2=(-1, 1),
    redshift=(0, 2.3),
)

cosmology = get_cosmology()

PRIOR_VOLUME = (
    (BOUNDS["mass_1"][1] - BOUNDS["mass_1"][0]) ** 2
    * (BOUNDS["a_1"][1] - BOUNDS["a_1"][0])
    * (BOUNDS["a_2"][1] - BOUNDS["a_2"][0])
    * (BOUNDS["cos_tilt_1"][1] - BOUNDS["cos_tilt_1"][0])
)


def create_parser():
    parser = create_main_parser()
    parser.add_argument(
        "--models",
        action="append",
        help="Model function to evaluate, default is "
        "two component mass and iid spins.",
    )
    parser.add_argument(
        "--vt-model",
        type=str,
        default="",
        help="Function to generate VT object, should be in "
        "vt_helper.py, default is mass only.",
    )
    return parser


def draw_true_values(model, vt_model=None, n_samples=40):
    """
    Draw samples from the probability density provided by the input model.

    Parameters
    ----------
    model: bilby.hyper.model.Model
        Population model to evaluate
    vt_model: gwpopulation.vt.GridVT, optional
        Model to compute selection function
    n_samples: int
        Number of samples to draw

    Returns
    -------
    total_samples: `pd.DataFrame`
        Data containing the true values.

    """
    if vt_model is None:
        vt_model = lambda x: 1
    else:
        raise NotImplementedError("Sensitive volume not implemented.")
    total_samples = pd.DataFrame()
    n_per_iteration = n_samples * 10000
    while True:
        data = _draw_from_prior(n_samples=n_per_iteration)
        prob = model.prob(data)
        prob *= vt_model(data)
        data = pd.DataFrame({key: to_numpy(data[key]) for key in data})
        data["prob"] = to_numpy(prob)
        total_samples = total_samples.append(data)
        max_prob = np.max(total_samples["prob"])
        total_samples = total_samples[total_samples["prob"] > 0]
        total_samples = total_samples[
            total_samples["prob"] > max_prob / n_per_iteration
        ]
        keep = np.array(total_samples["prob"]) >= np.random.uniform(
            0, max_prob, len(total_samples)
        )
        if sum(keep) > n_samples:
            total_samples = total_samples.iloc[keep]
            break
        logger.info(f"Drawing events is very inefficient.")
    total_samples = total_samples[:n_samples]
    del total_samples["prob"]
    return total_samples


def simulate_posterior(sample, fractional_sigma=0.1, n_samples=10000):
    """
    Simulate a posterior distribution given an input sample.

    This assumes uncorrelated uncertainties between different parameters.

    Parameters
    ----------
    sample: dict
        The true parameter values of the event to simulate a posterior for.
    fractional_sigma: float
        Fractional uncertainty on each parameter.
    n_samples: int
        The number of samples to draw.

    Returns
    -------
    posterior: `pd.DataFrame`
        The simulated posterior samples.

    """
    posterior = pd.DataFrame()
    for key in sample:
        if key in BOUNDS:
            bound = BOUNDS[key]
        else:
            bound = (-np.inf, np.inf)
        sigma = sample[key] * fractional_sigma
        new_true = TruncatedGaussian(
            mu=sample[key], sigma=sigma, minimum=bound[0], maximum=bound[1]
        ).sample()
        posterior[key] = TruncatedGaussian(
            mu=new_true, sigma=sigma, minimum=bound[0], maximum=bound[1]
        ).sample(n_samples)
    posterior = posterior[
        (BOUNDS["mass_1"][0] / posterior["mass_1"] <= posterior["mass_ratio"])
        & (posterior["mass_ratio"] <= BOUNDS["mass_ratio"][1])
    ]

    posterior["prior"] = 1 / PRIOR_VOLUME
    return posterior


def _draw_from_prior(n_samples):
    data = dict()
    for key in BOUNDS:
        data[key] = xp.random.uniform(BOUNDS[key][0], BOUNDS[key][1], n_samples)
    data["redshift"] = xp.asarray(
        UniformSourceFrame(
            minimum=BOUNDS["redshift"][0],
            maximum=BOUNDS["redshift"][1],
            name="redshift",
        ).sample(n_samples)
    )
    return data


def simulate_posterior_from_prior(n_samples=10000):
    """
    Draw samples from the posterior distribution assuming the data are
    non-informative, e.g., sample from the prior distribution.

    Parameters
    ----------
    n_samples: int
        The number of samples to simulate.

    Returns
    -------
    posterior: `pd.DataFrame`
        The simulated samples.

    """
    data = _draw_from_prior(n_samples=n_samples)
    posterior = pd.DataFrame({key: to_numpy(data[key]) for key in data})
    posterior["prior"] = (
        UniformSourceFrame(
            minimum=BOUNDS["redshift"][0],
            maximum=BOUNDS["redshift"][1],
            name="redshift",
        ).prob(posterior["redshift"])
        / PRIOR_VOLUME
    )
    return posterior


def simulate_posteriors(args):
    """
    Simulate a set of posterior samples gives the command-line arguments.

    Parameters
    ----------
    args:
        The command-line arguments.

    Returns
    -------
    posteriors: list
        The simulated posterior samples.
    """
    posteriors = list()
    if args.sample_from_prior:
        logger.info("Drawing prior samples for all simulated events.")
        for ii in range(args.n_simulations):
            posteriors.append(
                simulate_posterior_from_prior(n_samples=args.samples_per_posterior)
            )
    else:
        injection_parameters = dict(
            pd.read_json(args.injection_file).iloc[args.injection_index]
        )
        injection_parameters, _ = convert_to_beta_parameters(
            parameters=injection_parameters
        )
        args.models = list()
        args.models.append(MASS_MODELS[args.mass_models[0]])
        args.models.append(f"{args.magnitude_models[0]}_spin_magnitude")
        args.models.append(f"{args.tilt_models[0]}_spin_orientation")
        model = load_model(args=args)
        model.parameters.update(injection_parameters)
        logger.info(model.parameters)
        if not getattr(args, "vt_model", "") == "":
            vt_model = load_vt(args=args)
        else:
            vt_model = None
        true_values = draw_true_values(
            model=model, vt_model=vt_model, n_samples=args.n_simulations
        )
        logger.info("Simulating posteriors for all events.")
        for ii in range(args.n_simulations):
            posteriors.append(
                simulate_posterior(
                    dict(true_values.iloc[ii]), n_samples=args.samples_per_posterior
                )
            )
    if not os.path.exists(os.path.join(args.run_dir)):
        os.mkdir(os.path.join(args.run_dir))
    if not os.path.exists(os.path.join(args.run_dir, "data")):
        os.mkdir(os.path.join(args.run_dir, "data"))
    with open(
        os.path.join(args.run_dir, "data", f"{args.data_label}_posterior_files.txt"),
        "w",
    ) as ff:
        for ii in range(args.n_simulations):
            ff.write(f"{ii}:{ii}")
    return posteriors


def main():
    parser = create_parser()
    args, _ = parser.parse_known_args(sys.argv[1:])

    set_backend(args.backend)

    simulate_posteriors(args)
