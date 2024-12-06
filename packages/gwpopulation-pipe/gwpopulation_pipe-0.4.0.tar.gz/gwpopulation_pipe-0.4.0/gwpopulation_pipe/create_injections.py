from argparse import ArgumentParser

import pandas as pd
from bilby.core.prior import PriorDict
from bilby.core.utils import logger

from .utils import prior_conversion


def create_parser():
    parser = ArgumentParser(prog="GWPopulation pipe create injections")
    parser.add_argument("--prior-file", type=str, help="The prior file to sample from.")
    parser.add_argument("--n-simulation", type=int, help="The number of injections")
    parser.add_argument("--injection-file", type=str, help="The output file.")
    return parser


def create_injections(prior_file, n_simulation):
    priors = PriorDict(prior_file)
    priors.conversion_function = prior_conversion
    logger.info(f"Drawing {n_simulation} samples from {prior_file}.")
    samples = pd.DataFrame(priors.sample(n_simulation))
    return samples


def main():
    parser = create_parser()
    args = parser.parse_args()
    samples = create_injections(
        prior_file=args.prior_file, n_simulation=args.n_simulation
    )
    samples.to_json(args.injection_file)
    logger.info(f"Saving samples to {args.injection_file}.")
