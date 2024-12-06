"""
Post-processing plotting functions. This makes spectra plots as well as plots
comparing fiducial and population-informed posteriors.

The module provides the `gwpopulation_pipe_plot` executable.
"""

#!/usr/bin/env python3
import os

import dill
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from bilby.core.result import plot_multiple, read_in_result
from bilby.core.utils import logger
from bilby.hyper.model import Model
from bilby_pipe.parser import StoreBoolean
from gwpopulation.backend import set_backend
from gwpopulation.conversions import convert_to_beta_parameters
from gwpopulation.models.mass import (
    BrokenPowerLawPeakSmoothedMassDistribution,
    BrokenPowerLawSmoothedMassDistribution,
    MultiPeakSmoothedMassDistribution,
    SinglePeakSmoothedMassDistribution,
    power_law_primary_mass_ratio,
)
from gwpopulation.models.redshift import MadauDickinsonRedshift, PowerLawRedshift
from gwpopulation.models.spin import (
    independent_spin_magnitude_beta,
    independent_spin_orientation_gaussian_isotropic,
)
from gwpopulation.utils import to_numpy, xp
from tqdm import tqdm

from .parser import create_parser as create_main_parser
from .data_analysis import _load_model

_new_matplotlib_settings = {
    "text.usetex": True,
    "font.serif": "Computer Modern Roman",
    "font.family": "Serif",
}

_old_matplotlib_settings = {
    key: matplotlib.rcParams[key] for key in _new_matplotlib_settings
}


def _set_matplotlib():
    for key in _new_matplotlib_settings:
        matplotlib.rcParams[key] = _new_matplotlib_settings[key]


def _unset_matplotlib():
    for key in _old_matplotlib_settings:
        matplotlib.rcParams[key] = _old_matplotlib_settings[key]


def _load_samples(filename):
    with open(filename, "rb") as ff:
        return dill.load(ff)


def _dump_samples(filename, data):
    with open(filename, "wb") as ff:
        dill.dump(data, file=ff)


def create_parser():
    parser = create_main_parser()
    parser.add_argument("--result-file", nargs="*")
    parser.add_argument("--labels", nargs="*", default=None)
    spectra = ["mass", "orientation", "magnitude", "redshift", "chi_eff_chi_p"]
    for key in spectra:
        parser.add_argument(
            f"--{key}",
            dest=key,
            action=StoreBoolean,
            default=True,
            help=f"Make a {key} spectrum plot?",
        )
    for key in ["mass", "magnitude", "tilt", "redshift", "chi_eff_chi_p"]:
        parser.add_argument(f"--{key}-model", default=None)
    parser.add_argument(
        "--corner",
        dest="corner",
        action=StoreBoolean,
        default=False,
        help="Make corner plots?",
    )
    parser.add_argument(
        "--lower-limit",
        type=float,
        default=2.5,
        help="Lower limit for confidence band.",
    )
    parser.add_argument(
        "--upper-limit",
        type=float,
        default=97.5,
        help="Upper limit for confidence band.",
    )
    parser.add_argument(
        "--samples",
        type=str,
        default=None,
        help="HDF5 file containing original and reampled posteriors.",
    )
    return parser


MAX_SAMPLES = 10000


def corner_plots(result, *args, **kwargs):
    """
    Make corner plots broken into distinct single-event parameters
    based on known hyperparemeter names, e.g., all parameters describing the
    mass spectrum.

    Parameters
    ----------
    result: `bilby.core.result.Result`
        The `Bilby` result object containing the posterior.
    args: unused
    kwargs: unused

    """
    mass_parameters = [
        "alpha",
        "mmax",
        "mmin",
        "mpp",
        "sigpp",
        "lam",
        "delta_m",
        "beta",
        "alpha_1",
        "alpha_2",
        "break_fraction",
    ]
    spin_magnitude_parameters = [
        "alpha_chi",
        "beta_chi",
        "mu_chi",
        "sigma_chi",
        "mu_chi_1",
        "mu_chi_2",
        "sigma_chi_1",
        "sigma_chi_2",
        "amax",
        "amax_1",
        "amax_2",
        "mu_chi_eff",
        "sigma_chi_eff",
        "mu_chi_p",
        "sigma_chi_p",
    ]
    spin_orientation_parameters = ["xi_spin", "sigma_1", "sigma_2", "sigma_spin"]
    chi_eff_chi_p_parameters = [
        "mu_chi_eff",
        "sigma_chi_eff",
        "mu_chi_p",
        "sigma_chi_p",
        "spin_covariance",
    ]
    redshift_parameters = ["lambda_z"]

    if len(result) > 1:
        for kind, pars in zip(
            ["mass", "spin_magnitude", "spin_orientation", "redshift", "chi_eff_chi_p"],
            [
                mass_parameters,
                spin_magnitude_parameters,
                spin_orientation_parameters,
                redshift_parameters,
                chi_eff_chi_p_parameters,
            ],
        ):
            plot_pars = [
                par
                for par in pars
                if all([par in res.search_parameter_keys for res in result])
            ]
            if len(plot_pars) == 0:
                continue
            logger.info(f"Making {kind} corner plot with: " + ", ".join(plot_pars))
            plot_multiple(
                results=result,
                parameters=plot_pars,
                quantiles=None,
                filename=f"{result[0].outdir}/combined_{kind}_corner.png",
            )
    else:
        result = result[0]
        for kind, pars in zip(
            ["mass", "spin_magnitude", "spin_orientation", "redshift", "chi_eff_chi_p"],
            [
                mass_parameters,
                spin_magnitude_parameters,
                spin_orientation_parameters,
                redshift_parameters,
                chi_eff_chi_p_parameters,
            ],
        ):
            plot_pars = [par for par in result.search_parameter_keys if par in pars]
            if len(plot_pars) == 0:
                continue
            logger.info(f"Making {kind} corner plot with: " + ", ".join(plot_pars))
            result.plot_corner(
                parameters=plot_pars,
                quantiles=None,
                filename=f"{result.outdir}/{result.label}_{kind}_corner.png",
            )


def mass_spectrum_plot(results, args, rate=False, observed=False, save=True):
    """
    Make the posterior mass spectrum plot given either one or multiple result
    objects.

    Parameters
    ----------
    results: [list, `bilby.core.result.Result`]
        `Bilby` result(s) to make the spectra from.
    args: ArgumentParser
        The arguments describing the model.
    rate: bool
        Whether to scale the spectra by the inferred rate.
    observed: bool
        Whether to correct for selection effects. Not currently implemented.
    save: bool
        Whether to save the result to file.

    Returns
    -------
    [dict, `matplotlib.pyplot.Figure`]
        If `save` the data behind the plot is returned as a dictionary.
        Else, the figure handle is returned.

    """
    mass_1 = xp.linspace(2, 100, 1000)
    mass_ratio = xp.linspace(0.1, 1, 500)
    mass_1_grid, mass_ratio_grid = xp.meshgrid(mass_1, mass_ratio)
    if not isinstance(results, list):
        result = [results]

    if observed:
        # vt_evaluator = load_vt(None)
        # vt_evaluator
        # TODO: make this usable...
        raise NotImplementedError(
            "Observation weighted spectrum plots not yet supported."
        )

    fig, axs = plt.subplots(2, 1, figsize=(12, 8))

    peak_1 = 0
    peak_2 = 0

    for result in results:
        filename = f"{result.outdir}/{result.label}_mass_data.h5"
        if os.path.isfile(filename):
            _data = _load_samples(filename)
            lines = _data["lines"]
            ppd = _data["ppd"]
            injected = _data.get("injected", None)
        else:
            data = dict(
                mass_1=mass_1_grid,
                mass_ratio=mass_ratio_grid,
                mass_2=mass_1_grid * mass_ratio_grid,
            )
            lines = dict(mass_1=list(), mass_ratio=list())
            ppd = xp.zeros_like(data["mass_1"])

            if len(result.posterior) > MAX_SAMPLES:
                samples = result.posterior.sample(MAX_SAMPLES)
            else:
                samples = result.posterior

            if model := result.meta_data["models"].get("mass", None):
                model = Model([_load_model(model, args)])
            elif args.mass_model is not None:
                model = Model([_load_model(args.mass_model, args)])
            elif "mpp_1" in samples.keys():
                model = Model([MultiPeakSmoothedMassDistribution()])
                if "delta_m" not in samples:
                    samples["delta_m"] = 0
            elif "alpha_2" in samples.keys():
                if "mpp" in samples.keys():
                    model = Model([BrokenPowerLawPeakSmoothedMassDistribution()])
                else:
                    model = Model([BrokenPowerLawSmoothedMassDistribution()])
                if "delta_m" not in samples:
                    samples["delta_m"] = 0
            elif "mpp" in samples.keys():
                model = Model([SinglePeakSmoothedMassDistribution()])
                if "delta_m" not in samples:
                    samples["delta_m"] = 0
            elif "alpha" in samples.keys():
                model = Model([power_law_primary_mass_ratio])

            for ii in tqdm(range(len(samples))):
                parameters = dict(samples.iloc[ii])
                model.parameters.update(parameters)
                prob = model.prob(data)
                if rate:
                    if "rate" not in parameters:
                        rate = False
                    else:
                        prob *= parameters["rate"]
                ppd += prob

                mass_1_prob = xp.trapz(prob, mass_ratio, axis=0)
                mass_ratio_prob = xp.trapz(prob, mass_1, axis=-1)

                lines["mass_1"].append(mass_1_prob)
                lines["mass_ratio"].append(mass_ratio_prob)
            for key in lines:
                lines[key] = np.vstack([to_numpy(line) for line in lines[key]])

            ppd /= len(samples)
            ppd = to_numpy(ppd)

            if result.injection_parameters is not None and not rate:
                model.parameters.update(result.injection_parameters)
                injected = to_numpy(model.prob(data))
            else:
                injected = None

            positions = dict(mass_1=to_numpy(mass_1), mass_ratio=to_numpy(mass_ratio))
            _dump_samples(
                filename,
                data=dict(lines=lines, ppd=ppd, positions=positions, injected=injected),
            )

        mass_1 = to_numpy(mass_1)
        mass_ratio = to_numpy(mass_ratio)

        mass_1_ppd = np.trapz(ppd, mass_ratio, axis=0)
        mass_ratio_ppd = np.trapz(ppd, mass_1, axis=-1)

        label = " ".join(result.label.split("_")).title()

        axs[0].semilogy(mass_1, mass_1_ppd, label=label)
        axs[0].fill_between(
            mass_1,
            np.percentile(lines["mass_1"], args.lower_limit, axis=0),
            np.percentile(lines["mass_1"], args.upper_limit, axis=0),
            alpha=0.5,
        )
        _peak_1 = max(np.percentile(lines["mass_1"], args.upper_limit, axis=0))
        peak_1 = max(peak_1, _peak_1)
        axs[1].semilogy(mass_ratio, mass_ratio_ppd)
        axs[1].fill_between(
            mass_ratio,
            np.percentile(lines["mass_ratio"], args.lower_limit, axis=0),
            np.percentile(lines["mass_ratio"], args.upper_limit, axis=0),
            alpha=0.5,
        )
        _peak_2 = max(np.percentile(lines["mass_ratio"], args.upper_limit, axis=0))
        peak_2 = max(peak_2, _peak_2)

        if injected is not None:
            injected_mass_1 = np.trapz(injected, mass_ratio, axis=0)
            injected_mass_ratio = np.trapz(injected, mass_1, axis=-1)
            axs[0].plot(
                mass_1, injected_mass_1, color="k", label="True", linestyle="--"
            )
            axs[1].plot(mass_ratio, injected_mass_ratio, color="k", linestyle="--")

    axs[0].set_xlim(2, 100)
    axs[0].set_ylim(peak_1 / 100000, peak_1 * 1.1)
    axs[0].set_xlabel("$m_{1}$ [$M_{\\odot}$]")
    axs[0].legend(bbox_to_anchor=(0.5, 1.15), loc="upper center")
    if rate:
        ylabel = "$\\frac{d\\mathcal{R}}{dm_{1}}$ [Gpc$^{-3}$yr$^{-1}M_{\\odot}^{-1}$]"
    else:
        ylabel = "$p(m_{1})$ [$M_{\\odot}^{-1}$]"
    axs[0].set_ylabel(ylabel)

    axs[1].set_xlim(0.1, 1)
    axs[1].set_ylim(peak_2 / 10000, peak_2 * 1.1)
    axs[1].set_xlabel("$q$")
    if rate:
        ylabel = "$\\frac{d\\mathcal{R}}{dq}$ [Gpc$^{-3}$yr$^{-1}$]"
    else:
        ylabel = "$p(q)$"
    axs[1].set_ylabel(ylabel)

    if len(results) == 1:
        file_name = f"{result.outdir}/{result.label}_mass_spectrum.pdf"
    else:
        file_name = f"{result.outdir}/combined_mass_spectrum.pdf"
    plt.tight_layout()
    if save:
        plt.savefig(file_name, format="pdf", dpi=600, bbox_inches="tight")
        plt.close()
        return ppd
    else:
        return fig


def chi_eff_chi_p_plot(results, args, rate=False, observed=False, save=True):
    """
    Make the posterior chi_eff chi_p plot given either one or multiple result
    objects.

    Parameters
    ----------
    results: [list, `bilby.core.result.Result`]
        `Bilby` result(s) to make the spectra from.
    args: ArgumentParser
        The arguments describing the model.
    rate: bool
        Whether to scale the spectra by the inferred rate.
    observed: bool
        Whether to correct for selection effects. Not currently implemented.
    save: bool
        Whether to save the result to file.

    Returns
    -------
    [dict, `matplotlib.pyplot.Figure`]
        If `save` the data behind the plot is returned as a dictionary.
        Else, the figure handle is returned.

    """

    chi_eff = xp.linspace(-1, 1, 1000)
    chi_p = xp.linspace(0, 1, 500)
    chi_eff_grid, chi_p_grid = xp.meshgrid(chi_eff, chi_p)
    if not isinstance(results, list):
        result = [results]

    if observed:
        # vt_evaluator = load_vt(None)
        # vt_evaluator
        # TODO: make this usable...
        raise NotImplementedError(
            "Observation weighted spectrum plots not yet supported."
        )

    fig, axs = plt.subplots(2, 1, figsize=(12, 8))

    for result in results:
        filename = f"{result.outdir}/{result.label}_spin_data.h5"
        if os.path.isfile(filename):
            _data = _load_samples(filename)
            lines = _data["lines"]
            ppd = _data["ppd"]
            injected = _data.get("injected", None)
        else:
            data = dict(
                chi_eff=chi_eff_grid,
                chi_p=chi_p_grid,
            )
            lines = dict(chi_eff=list(), chi_p=list())
            ppd = xp.zeros_like(data["chi_eff"])

            if len(result.posterior) > MAX_SAMPLES:
                samples = result.posterior.sample(MAX_SAMPLES)
            else:
                samples = result.posterior

            try:
                try:
                    model = result.meta_data["models"]["spin"]
                except KeyError:
                    model = result.meta_data["models"]["effective_spin"]
            except KeyError:
                raise KeyError("No chi_eff chi_p spin model found in result.")
            model = Model([_load_model(model, args)])

            for ii in tqdm(range(len(samples))):
                parameters = dict(samples.iloc[ii])
                model.parameters.update(parameters)
                prob = model.prob(data)
                if rate:
                    if "rate" not in parameters:
                        rate = False
                    else:
                        prob *= parameters["rate"]
                ppd += prob

                chi_eff_prob = xp.trapz(prob, chi_p, axis=0)
                chi_p_prob = xp.trapz(prob, chi_eff, axis=-1)

                lines["chi_eff"].append(chi_eff_prob)
                lines["chi_p"].append(chi_p_prob)
            for key in lines:
                lines[key] = np.vstack([to_numpy(line) for line in lines[key]])

            ppd /= len(samples)
            ppd = to_numpy(ppd)

            if result.injection_parameters is not None and not rate:
                model.parameters.update(result.injection_parameters)
                injected = to_numpy(model.prob(data))
            else:
                injected = None

            _dump_samples(filename, data=dict(lines=lines, ppd=ppd, injected=injected))

        chi_eff = to_numpy(chi_eff)
        chi_p = to_numpy(chi_p)

        chi_eff_ppd = np.trapz(ppd, chi_p, axis=0)
        chi_p_ppd = np.trapz(ppd, chi_eff, axis=1)

        label = " ".join(result.label.split("_")).title()

        axs[0].plot(chi_eff, chi_eff_ppd, label=label)
        axs[0].fill_between(
            chi_eff,
            np.percentile(lines["chi_eff"], args.lower_limit, axis=0),
            np.percentile(lines["chi_eff"], args.upper_limit, axis=0),
            alpha=0.5,
        )

        axs[1].plot(chi_p, chi_p_ppd)
        axs[1].fill_between(
            chi_p,
            np.percentile(lines["chi_p"], args.lower_limit, axis=0),
            np.percentile(lines["chi_p"], args.upper_limit, axis=0),
            alpha=0.5,
        )

        if injected is not None:
            injected_chi_p = np.trapz(injected, chi_p, axis=0)
            injected_chi_eff = np.trapz(injected, chi_eff, axis=-1)
            axs[0].plot(
                chi_eff, injected_chi_eff, color="k", label="True", linestyle="--"
            )
            axs[1].plot(chi_p, injected_chi_p, color="k", linestyle="--")

    axs[0].set_xlim(-1, 1)
    axs[0].set_ylim(0)
    axs[0].set_xlabel("$\\chi_{eff}$")
    axs[0].legend(loc="upper center")
    if rate:
        ylabel = "$\\frac{d\\mathcal{R}}{d\\chi_{eff}}$ [Gpc$^{-3}$yr$^{-1}$]"
    else:
        ylabel = "$p(\\chi_{eff})$]"
    axs[0].set_ylabel(ylabel)

    axs[1].set_xlim(0.0, 1)
    axs[1].set_ylim(0)
    axs[1].set_xlabel("$\\chi_p$")
    if rate:
        ylabel = "$\\frac{d\\mathcal{R}}{d\\chi_p}$ [Gpc$^{-3}$yr$^{-1}$]"
    else:
        ylabel = "$p(\\chi_p)$"
    axs[1].set_ylabel(ylabel)

    if len(results) == 1:
        file_name = f"{result.outdir}/{result.label}_spin_spectrum.pdf"
    else:
        file_name = f"{result.outdir}/combined_spin_spectrum.pdf"
    plt.tight_layout()
    if save:
        plt.savefig(file_name, format="pdf", dpi=600, bbox_inches="tight")
        plt.close()
        return ppd
    else:
        return fig


def spin_magnitude_spectrum_plot(results, args, rate=False, save=True):
    """
    Make the posterior spin magnitude plot given either one or multiple result
    objects.

    Parameters
    ----------
    results: [list, `bilby.core.result.Result`]
        `Bilby` result(s) to make the spectra from.
    args: ArgumentParser
        The arguments describing the model.
    rate: bool
        Whether to scale the spectra by the inferred rate.
    save: bool
        Whether to save the result to file.

    Returns
    -------
    [dict, `matplotlib.pyplot.Figure`]
        If `save` the data behind the plot is returned as a dictionary.
        Else, the figure handle is returned.

    """
    mags = xp.linspace(0, 1, 1000)
    a_1, a_2 = xp.meshgrid(mags, mags)

    fig, axs = plt.subplots(1, 2, figsize=(12, 4))

    for result in results:
        filename = f"{result.outdir}/{result.label}_magnitude_data.h5"
        if os.path.isfile(filename):
            _data = _load_samples(filename)
            lines = _data["lines"]
            ppd = _data["ppd"]
            injected = _data.get("injected", None)
        else:
            if model := result.meta_data["models"].get("magnitude", None):
                model = Model([_load_model(model, args)])
            elif args.magnitude_model is not None:
                model = Model([_load_model(args.magnitude_model, args=args)])
            else:
                model = Model([independent_spin_magnitude_beta])
                for key in ["amax", "mu_chi", "sigma_chi", "alpha_chi", "beta_chi"]:
                    if key in result.posterior and f"{key}_1" not in result.posterior:
                        result.posterior[f"{key}_1"] = result.posterior[key]
                        result.posterior[f"{key}_2"] = result.posterior[key]
                        del result.posterior[key]
                result.posterior = convert_to_beta_parameters(result.posterior)[0]

            data = dict(a_1=a_1, a_2=a_2)
            lines = dict(a_1=list(), a_2=list())
            ppd = xp.zeros_like(data["a_1"])

            if len(result.posterior) > MAX_SAMPLES:
                samples = result.posterior.sample(MAX_SAMPLES)
            else:
                samples = result.posterior

            for ii in tqdm(range(len(samples))):
                parameters = dict(samples.iloc[ii])
                model.parameters.update(parameters)
                prob = model.prob(data)
                if rate:
                    if "rate" not in parameters:
                        rate = False
                    else:
                        prob *= parameters["rate"]
                ppd += prob

                a_1_prob = xp.trapz(prob, mags, axis=0)
                a_2_prob = xp.trapz(prob, mags, axis=-1)

                lines["a_1"].append(a_1_prob)
                lines["a_2"].append(a_2_prob)
            for key in lines:
                lines[key] = np.vstack([to_numpy(line) for line in lines[key]])

            ppd /= len(samples)
            ppd = to_numpy(ppd)

            if result.injection_parameters is not None and not rate:
                parameters = result.injection_parameters.copy()
                for key in ["amax", "mu_chi", "sigma_chi", "alpha_chi", "beta_chi"]:
                    if key in parameters and f"{key}_1" not in parameters:
                        parameters[f"{key}_1"] = parameters[key]
                        parameters[f"{key}_2"] = parameters[key]
                        del parameters[key]
                parameters = convert_to_beta_parameters(parameters)[0]
                model.parameters.update(parameters)
                injected = to_numpy(model.prob(data))
            else:
                injected = None

            positions = dict(a_1=to_numpy(mags), a_2=to_numpy(mags))
            _dump_samples(
                filename, data=dict(lines=lines, ppd=ppd, positions=positions)
            )

        mags = to_numpy(mags)

        a_1_ppd = np.trapz(ppd, mags, axis=0)
        a_2_ppd = np.trapz(ppd, mags, axis=1)

        label = " ".join(result.label.split("_")).title()

        axs[0].plot(mags, a_1_ppd, label=label)
        axs[0].fill_between(
            mags,
            np.percentile(lines["a_1"], args.lower_limit, axis=0),
            np.percentile(lines["a_1"], args.upper_limit, axis=0),
            alpha=0.5,
        )
        axs[1].plot(mags, a_2_ppd)
        axs[1].fill_between(
            mags,
            np.percentile(lines["a_2"], args.lower_limit, axis=0),
            np.percentile(lines["a_2"], args.upper_limit, axis=0),
            alpha=0.5,
        )

        if injected is not None and not rate:
            a_1_injected = np.trapz(injected, mags, axis=0)
            a_2_injected = np.trapz(injected, mags, axis=1)
            axs[0].plot(mags, a_1_injected, color="k", label="True", linestyle="--")
            axs[1].plot(mags, a_2_injected, color="k", linestyle="--")

    for ii in [1, 2]:
        axs[ii - 1].set_xlim(0, 1)
        axs[ii - 1].set_ylim(0)
        axs[ii - 1].set_xlabel(f"$a_{ii}$")
        if rate:
            ylabel = f"$\\frac{{dN}}{{da_{ii}}}$"
        else:
            ylabel = f"$p(a_{ii})$"
        axs[ii - 1].set_ylabel(ylabel)
    axs[0].legend(bbox_to_anchor=(0.5, 1.15), loc="upper center")

    if len(results) == 1:
        file_name = f"{result.outdir}/{result.label}_magnitude_spectrum.pdf"
    else:
        file_name = f"{result.outdir}/comparison_magnitude_spectrum.pdf"
    if save:
        plt.savefig(file_name, format="pdf", dpi=600, bbox_inches="tight")
        plt.close()
        return ppd
    else:
        return fig


def spin_orientation_spectrum_plot(results, args, rate=False, save=True):
    """
    Make the posterior spin orientation plot given either one or multiple result
    objects.

    Parameters
    ----------
    results: [list, `bilby.core.result.Result`]
        `Bilby` result(s) to make the spectra from.
    args: ArgumentParser
        The arguments describing the model.
    rate: bool
        Whether to scale the spectra by the inferred rate.
    save: bool
        Whether to save the result to file.

    Returns
    -------
    [dict, `matplotlib.pyplot.Figure`]
        If `save` the data behind the plot is returned as a dictionary.
        Else, the figure handle is returned.

    """
    cos_tilts = xp.linspace(-1, 1, 1000)
    cos_tilt_1, cos_tilt_2 = xp.meshgrid(cos_tilts, cos_tilts)

    fig, axs = plt.subplots(1, 2, figsize=(12, 4))

    for result in results:
        filename = f"{result.outdir}/{result.label}_orientation_data.h5"
        if os.path.isfile(filename):
            _data = _load_samples(filename)
            lines = _data["lines"]
            ppd = _data["ppd"]
            injected = _data.get("injected", None)
        else:
            if model := result.meta_data["models"].get("tilt", None):
                model = Model([_load_model(model, args)])
            elif args.tilt_model is not None:
                model = Model([_load_model(args.tilt_model, args=args)])
            else:
                model = Model([independent_spin_orientation_gaussian_isotropic])
                if "sigma_1" not in result.posterior:
                    result.posterior["sigma_1"] = result.posterior["sigma_spin"]
                    result.posterior["sigma_2"] = result.posterior["sigma_spin"]

            data = dict(cos_tilt_1=cos_tilt_1, cos_tilt_2=cos_tilt_2)
            lines = dict(cos_tilt_1=list(), cos_tilt_2=list())
            ppd = xp.zeros_like(data["cos_tilt_1"])

            if len(result.posterior) > MAX_SAMPLES:
                samples = result.posterior.sample(MAX_SAMPLES)
            else:
                samples = result.posterior

            for ii in tqdm(range(len(samples))):
                parameters = dict(samples.iloc[ii])
                model.parameters.update(parameters)
                prob = model.prob(data)
                if rate:
                    if "rate" not in parameters:
                        rate = False
                    else:
                        prob *= parameters["rate"]
                ppd += prob

                cos_tilt_1_prob = xp.trapz(prob, cos_tilts, axis=0)
                cos_tilt_2_prob = xp.trapz(prob, cos_tilts, axis=1)

                lines["cos_tilt_1"].append(cos_tilt_1_prob)
                lines["cos_tilt_2"].append(cos_tilt_2_prob)
            for key in lines:
                lines[key] = np.vstack([to_numpy(line) for line in lines[key]])

            ppd /= len(samples)
            ppd = to_numpy(ppd)

            if result.injection_parameters is not None and not rate:
                parameters = result.injection_parameters
                if "sigma_1" not in parameters:
                    parameters["sigma_1"] = parameters["sigma_spin"]
                    parameters["sigma_2"] = parameters["sigma_spin"]
                model.parameters.update(parameters)
                injected = to_numpy(model.prob(data))
            else:
                injected = None

            positions = dict(
                cos_tilt_1=to_numpy(cos_tilts), cos_tilt_2=to_numpy(cos_tilts)
            )
            _dump_samples(
                filename, data=dict(lines=lines, ppd=ppd, positions=positions)
            )

        cos_tilts = to_numpy(cos_tilts)

        cos_tilt_1_ppd = np.trapz(ppd, cos_tilts, axis=0)
        cos_tilt_2_ppd = np.trapz(ppd, cos_tilts, axis=1)

        label = " ".join(result.label.split("_")).title()

        axs[0].plot(cos_tilts, cos_tilt_1_ppd, label=label)
        axs[0].fill_between(
            cos_tilts,
            np.percentile(lines["cos_tilt_1"], args.lower_limit, axis=0),
            np.percentile(lines["cos_tilt_1"], args.upper_limit, axis=0),
            alpha=0.5,
        )
        axs[1].plot(cos_tilts, cos_tilt_2_ppd)
        axs[1].fill_between(
            cos_tilts,
            np.percentile(lines["cos_tilt_2"], args.lower_limit, axis=0),
            np.percentile(lines["cos_tilt_2"], args.upper_limit, axis=0),
            alpha=0.5,
        )

        if injected is not None and not rate:
            t_1_injected = np.trapz(injected, cos_tilts, axis=0)
            t_2_injected = np.trapz(injected, cos_tilts, axis=1)
            axs[0].plot(
                cos_tilts, t_1_injected, color="k", label="True", linestyle="--"
            )
            axs[1].plot(cos_tilts, t_2_injected, color="k", linestyle="--")

    if rate:
        ylabel = "$\\frac{{d\\mathcal{{R}}}}{{d\\cos t_{}}}$ [Gpc$^{{-3}}$yr$^{{-1}}$]"
    else:
        ylabel = "$p(\\cos t_{})$"
    for ii in [1, 2]:
        axs[ii - 1].set_xlim(-1, 1)
        axs[ii - 1].set_ylim(0)
        axs[ii - 1].set_xlabel(f"$\\cos t_{ii}$")
        axs[ii - 1].set_ylabel(ylabel.format(str(ii)))
    axs[0].legend(bbox_to_anchor=(0.5, 1.15), loc="upper center")

    if len(results) == 1:
        file_name = f"{result.outdir}/{result.label}_orientation_spectrum.pdf"
    else:
        file_name = f"{result.outdir}/comparison_orientation_spectrum.pdf"
    if save:
        plt.savefig(file_name, format="pdf", dpi=600, bbox_inches="tight")
        plt.close()
        return ppd
    else:
        return fig


def redshift_spectrum_plot(results, args, rate=True, save=True):
    """
    Make the posterior redshift plot given either one or multiple result
    objects.

    Parameters
    ----------
    results: [list, `bilby.core.result.Result`]
        `Bilby` result(s) to make the spectra from.
    args: ArgumentParser
        The arguments describing the model.
    rate: bool
        Whether to scale the spectra by the inferred rate.
    save: bool
        Whether to save the result to file.

    Returns
    -------
    [dict, `matplotlib.pyplot.Figure`]
        If `save` the data behind the plot is returned as a dictionary.
        Else, the figure handle is returned.

    """
    fig, ax = plt.subplots(1, 1, figsize=(6, 4))

    for result in results:
        if model := result.meta_data["models"].get("redshift", None):
            model = _load_model(model, args)
        elif args.redshift_model is not None:
            model = _load_model(args.redshift_model, args=args)
        elif "lamb" in result.posterior:
            model = PowerLawRedshift(z_max=2.3)
        elif "gamma" in result.posterior:
            model = MadauDickinsonRedshift(z_max=args.upper_limit)
        else:
            raise KeyError("Cannot find redshift parameters.")

        redshifts = model.zs
        _np_redshifts = to_numpy(redshifts)

        filename = f"{result.outdir}/{result.label}_redshift_data.h5"
        if os.path.exists(filename):
            _data = _load_samples(filename)
            lines = _data["lines"]
            ppd = _data["ppd"]
        else:
            ppd = xp.zeros_like(redshifts)
            lines = dict(redshift=list())

            if len(result.posterior) > MAX_SAMPLES:
                samples = result.posterior.sample(MAX_SAMPLES)
            else:
                samples = result.posterior

            for ii in tqdm(range(len(samples))):
                parameters = dict(samples.iloc[ii])
                prob = model.psi_of_z(
                    redshift=redshifts,
                    **{key: parameters[key] for key in model.variable_names},
                )
                if rate:
                    if "surveyed_hypervolume" not in parameters:
                        rate = False
                    else:
                        prob *= parameters["rate"]
                ppd += prob

                lines["redshift"].append(to_numpy(prob))

            ppd /= len(samples)
            ppd = to_numpy(ppd)
            positions = dict(redshift=_np_redshifts)
            _dump_samples(
                filename, data=dict(lines=lines, ppd=ppd, positions=positions)
            )

        label = " ".join(result.label.split("_")).title()

        ax.plot(_np_redshifts, ppd, label=label)
        ax.fill_between(
            _np_redshifts,
            np.percentile(lines["redshift"], args.lower_limit, axis=0),
            np.percentile(lines["redshift"], args.upper_limit, axis=0),
            alpha=0.5,
        )

    if rate:
        ylabel = "$\\mathcal{R}(z)$ [Gpc$^{-3}$yr$^{-1}$]"
    else:
        ylabel = "$\\frac{R(z)}{R(z=0)}$"
    ax.set_xlim(0, 2.3)
    ax.set_yscale("log")
    ax.set_xlabel("$z$")
    ax.set_ylabel(ylabel)
    ax.legend(bbox_to_anchor=(0.5, 1.15), loc="upper center")

    if len(results) == 1:
        file_name = f"{result.outdir}/{result.label}_redshift_spectrum.pdf"
    else:
        file_name = f"{result.outdir}/comparison_redshift_spectrum.pdf"
    if save:
        plt.savefig(file_name, format="pdf", dpi=600, bbox_inches="tight")
        plt.close()
        return ppd
    else:
        return fig


def reweighted_comparison(data, outdir="outdir"):
    """
    Plot a comparison of fiducial and population-informed single-event posteriors.

    The makes an interactive `html` figure with `plotly`.

    Parameters
    ----------
    data: dict
        Dictionary containing `original` and `reweighted` posteriors.
    outdir: str
        The output directory to save the file to.

    """
    import plotly.graph_objects as go
    from plotly.offline import plot
    from plotly.subplots import make_subplots

    parameter_names = list(data["original"].keys())
    plotting_parameters = list()
    for key in ["original", "reweighted"]:
        if "mass_1" in parameter_names:
            plotting_parameters.append("mass_1")
            if "mass_ratio" in parameter_names and "mass_2" not in parameter_names:
                data[key]["mass_2"] = data[key]["mass_1"] * data[key]["mass_ratio"]
            elif "mass_ratio" not in parameter_names and "mass_2" in parameter_names:
                data[key]["mass_ratio"] = data[key]["mass_2"] / data[key]["mass_1"]
        if all(
            [
                _key in data[key]
                for _key in ["a_1", "a_2", "cos_tilt_1", "cos_tilt_2", "mass_ratio"]
            ]
        ):
            data[key]["chi_eff"] = (
                data[key]["a_1"] * data[key]["cos_tilt_1"]
                + data[key]["mass_ratio"] * data[key]["a_2"] * data[key]["cos_tilt_2"]
            ) / (1 + data[key]["mass_ratio"])
            in_plane_1 = data[key]["a_1"] * (1 - data[key]["cos_tilt_1"] ** 2) ** 0.5
            in_plane_2 = data[key]["a_2"] * (1 - data[key]["cos_tilt_2"] ** 2) ** 0.5
            data[key]["chi_p"] = np.maximum(
                in_plane_1,
                data[key]["mass_ratio"]
                * (3 + 4 * data[key]["mass_ratio"])
                / (4 + 3 * data[key]["mass_ratio"])
                * in_plane_2,
            )
    if "chi_eff" in data["original"]:
        plotting_parameters.append("chi_eff")
        plotting_parameters.append("chi_p")
    plotting_parameters.append("mass_ratio")
    plotting_parameters.append("mass_2")
    if "names" not in data:
        names = [str(ii) for ii in range(data["original"][parameter_names[0]].shape[0])]
    else:
        names = data["names"]

    fig = make_subplots(
        rows=len(parameter_names),
        cols=1,
        row_heights=[1 / len(parameter_names)] * len(parameter_names),
    )

    fig.update_layout(
        template="plotly_white",
        font=dict(family="Computer Modern"),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
    )

    kinds = list()
    parameters = list()
    legends = list()

    for jj, parameter in enumerate(plotting_parameters):
        for ii, event in enumerate(names):
            fig.add_trace(
                go.Histogram(
                    x=to_numpy(data["original"][parameter][ii])[:1000],
                    histnorm="probability density",
                    marker_color="Blue",
                    legendgroup=event,
                    showlegend=False,
                    name=event,
                    hovertext=event,
                ),
                row=jj + 1,
                col=1,
            )
            kinds.append("original")
            parameters.append(parameter)
            if jj == 0:
                legends.append(True)
            else:
                legends.append(False)
            fig.add_trace(
                go.Histogram(
                    x=to_numpy(data["reweighted"][parameter][ii])[:1000],
                    histnorm="probability density",
                    marker_color="Red",
                    legendgroup=event,
                    showlegend=True and jj == 0,
                    name=event,
                    hovertext=event,
                ),
                row=jj + 1,
                col=1,
            )
            kinds.append("resampled")
            parameters.append(parameter)
            if jj == 0:
                legends.append(True)
            else:
                legends.append(False)
        fig.update_xaxes(title_text=" ".join(parameter.split("_")), row=jj + 1, col=1)

    fig.update_layout(barmode="overlay")
    fig.update_traces(opacity=0.3)

    updatemenus = [
        go.layout.Updatemenu(
            type="buttons",
            direction="right",
            active=0,
            x=0.57,
            y=1.2,
            buttons=list(
                [
                    dict(
                        label="All",
                        method="update",
                        args=[
                            {
                                "visible": [True] * len(kinds),
                                "showlegend": [
                                    kind == "original" and legend
                                    for kind, legend in zip(kinds, legends)
                                ],
                            }
                        ],
                    ),
                    dict(
                        label="Original",
                        method="update",
                        args=[
                            {
                                "visible": [kind == "original" for kind in kinds],
                                "showlegend": [
                                    kind == "original" and legend
                                    for kind, legend in zip(kinds, legends)
                                ],
                            }
                        ],
                    ),
                    dict(
                        label="Resampled",
                        method="update",
                        args=[
                            {
                                "visible": [kind == "resampled" for kind in kinds],
                                "showlegend": [
                                    kind == "original" and legend
                                    for kind, legend in zip(kinds, legends)
                                ],
                            }
                        ],
                    ),
                ]
            ),
        )
    ]
    fig.update_layout(updatemenus=updatemenus)
    fig.update_layout(height=250 * len(plotting_parameters), width=1000)
    filename = f"{outdir}/{data['label']}_samples.html"
    plot(fig, filename=filename, include_mathjax="cdn", auto_open=False)


PLOT_MAP = dict(
    mass=mass_spectrum_plot,
    magnitude=spin_magnitude_spectrum_plot,
    orientation=spin_orientation_spectrum_plot,
    redshift=redshift_spectrum_plot,
    corner=corner_plots,
    chi_eff_chi_p=chi_eff_chi_p_plot,
)


def _safe_plot(result, args, key):
    _set_matplotlib()
    try:
        PLOT_MAP[key](result, args, rate=True)
    except Exception as e:
        if "TeX" in e.args[0]:
            logger.warning(
                f"Failed to create plot for {key} due to missing TeX. " "Disabling TeX."
            )
            _unset_matplotlib()
            PLOT_MAP[key](result, args, rate=True)
        else:
            logger.warning(f"Failed to create {key} plot with message {e}")
    _unset_matplotlib()


def main():
    parser = create_parser()
    args, _ = parser.parse_known_args()
    set_backend(args.backend)
    results = [read_in_result(res) for res in args.result_file]
    if args.labels is not None:
        for label, result in zip(args.labels, results):
            result.label = label
    if args.run_dir is not None:
        for result in results:
            result.outdir = os.path.join(args.run_dir, "result")
    for key in [
        "mass",
        "magnitude",
        "orientation",
        "redshift",
        "corner",
        "chi_eff_chi_p",
    ]:
        if getattr(args, key):
            logger.info(f"Making {key} plot")
            _safe_plot(results, args, key)
    if args.samples is not None and os.path.exists(args.samples):
        samples = _load_samples(args.samples)
        reweighted_comparison(data=samples, outdir=os.path.join(args.run_dir, "result"))
    elif args.samples is not None:
        logger.info(
            f"Cannot find samples file {args.samples}. \
            Skipping reweighted comparison plot."
        )


if __name__ == "__main__":
    main()
