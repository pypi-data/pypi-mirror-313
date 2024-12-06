import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from bilby.hyper.model import Model
from gwpopulation.conversions import convert_to_beta_parameters
from gwpopulation.utils import to_numpy, xp
from gwpopulation.models.mass import (
    double_power_law_primary_power_law_mass_ratio,
    two_component_primary_mass_ratio,
)
from gwpopulation.models.spin import (
    independent_spin_magnitude_beta,
    independent_spin_orientation_gaussian_isotropic,
)
from tqdm import tqdm

MAX_SAMPLES = 10000

__single_plots__ = [
    "mass_spectrum_plot",
    "spin_magnitude_spectrum_plot",
    "spin_orientation_spectrum_plot",
]
__comparison_plots__ = [
    "mass_spectrum_plot",
    "spin_magnitude_spectrum_plot",
    "spin_orientation_spectrum_plot",
]


def mass_spectrum_plot(parameters, samples, labels=None, limits=None, rate=False):
    if limits is None:
        limits = [5, 95]

    if labels is not None and len(labels) > 1:
        all_samples = [
            pd.DataFrame(samps, columns=params)
            for samps, params in zip(samples, parameters)
        ]
    else:
        all_samples = [pd.DataFrame(samples, columns=parameters)]
        labels = [labels]
    mass_1 = xp.linspace(2, 100, 1000)
    mass_ratio = xp.linspace(0.1, 1, 500)
    mass_1_grid, mass_ratio_grid = xp.meshgrid(mass_1, mass_ratio)

    fig, axs = plt.subplots(2, 1, figsize=(12, 8))

    peak_1 = 0
    peak_2 = 0

    for jj, samples in enumerate(all_samples):
        data = dict(mass_1=mass_1_grid, mass_ratio=mass_ratio_grid)
        lines = dict(mass_1=list(), mass_ratio=list())
        ppd = xp.zeros_like(data["mass_1"])

        if len(samples) > MAX_SAMPLES:
            samples = samples.sample(MAX_SAMPLES)
        else:
            samples = samples

        for func in [
            two_component_primary_mass_ratio,
            double_power_law_primary_power_law_mass_ratio,
        ]:
            model = Model([func])
            try:
                model.parameters.update(dict(samples.iloc[0]))
                model.prob(dict(mass_1=xp.asarray([30]), mass_ratio=xp.asarray([0.9])))
                break
            except:
                pass

        for ii in tqdm(range(len(samples))):
            parameters = dict(samples.iloc[ii])
            model.parameters.update(parameters)
            prob = model.prob(data)
            if rate:
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

        mass_1 = to_numpy(mass_1)
        mass_ratio = to_numpy(mass_ratio)

        mass_1_ppd = np.trapz(ppd, mass_ratio, axis=0)
        mass_ratio_ppd = np.trapz(ppd, mass_1, axis=-1)

        label = labels[jj]
        if label is not None:
            label = label.replace("_", " ")

        axs[0].semilogy(mass_1, mass_1_ppd, label=label)
        axs[0].fill_between(
            mass_1,
            np.percentile(lines["mass_1"], limits[0], axis=0),
            np.percentile(lines["mass_1"], limits[1], axis=0),
            alpha=0.5,
        )
        _peak_1 = max(np.percentile(lines["mass_1"], limits[1], axis=0))
        peak_1 = max(peak_1, _peak_1)
        axs[1].semilogy(mass_ratio, mass_ratio_ppd)
        axs[1].fill_between(
            mass_ratio,
            np.percentile(lines["mass_ratio"], limits[0], axis=0),
            np.percentile(lines["mass_ratio"], limits[1], axis=0),
            alpha=0.5,
        )
        _peak_2 = max(np.percentile(lines["mass_ratio"], limits[1], axis=0))
        peak_2 = max(peak_2, _peak_2)

    axs[0].set_xlim(2, 60)
    axs[0].set_ylim(peak_1 / 1000, peak_1 * 1.1)
    axs[0].set_xlabel("$m_{1}$ [$M_{\\odot}$]")
    if rate:
        ylabel = "$\\frac{dN}{dm_{1}}$"
    else:
        ylabel = "$p(m_{1})$ [$M_{\\odot}^{-1}$]"
    axs[0].set_ylabel(ylabel)
    if len(labels) > 1:
        axs[0].legend(loc="best")

    axs[1].set_xlim(0.1, 1)
    axs[1].set_ylim(peak_2 / 10000, peak_2 * 1.1)
    axs[1].set_xlabel("$q$")
    if rate:
        ylabel = "$\\frac{dN}{dq}$"
    else:
        ylabel = "$p(q)$"
    axs[1].set_ylabel(ylabel)

    plt.tight_layout()
    return fig


def spin_magnitude_spectrum_plot(
    parameters, samples, labels=None, limits=None, rate=False
):
    if limits is None:
        limits = [5, 95]

    if labels is not None and len(labels) > 1:
        all_samples = [
            pd.DataFrame(samps, columns=params)
            for samps, params in zip(samples, parameters)
        ]
    else:
        all_samples = [pd.DataFrame(samples, columns=parameters)]
        labels = [labels]
    mags = xp.linspace(0, 1, 1000)
    a_1, a_2 = xp.meshgrid(mags, mags)
    model = Model([independent_spin_magnitude_beta])

    fig, axs = plt.subplots(1, 2, figsize=(12, 4))

    for jj, samples in enumerate(all_samples):
        for key in ["amax", "mu_chi", "sigma_chi"]:
            if f"{key}_1" not in samples:
                samples[f"{key}_1"] = samples[key]
                samples[f"{key}_2"] = samples[key]
                del samples[key]

        data = dict(a_1=a_1, a_2=a_2)
        lines = dict(a_1=list(), a_2=list())
        ppd = xp.zeros_like(data["a_1"])

        samples = convert_to_beta_parameters(samples)[0]

        if len(samples) > MAX_SAMPLES:
            samples = samples.sample(MAX_SAMPLES)
        else:
            samples = samples

        for ii in tqdm(range(len(samples))):
            parameters = dict(samples.iloc[ii])
            model.parameters.update(parameters)
            prob = model.prob(data)
            if rate:
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

        mags = to_numpy(mags)

        a_1_ppd = np.trapz(ppd, mags, axis=0)
        a_2_ppd = np.trapz(ppd, mags, axis=1)

        label = labels[jj]
        if label is not None:
            label = label.replace("_", " ")

        axs[0].plot(mags, a_1_ppd, label=label)
        axs[0].fill_between(
            mags,
            np.percentile(lines["a_1"], limits[0], axis=0),
            np.percentile(lines["a_1"], limits[1], axis=0),
            alpha=0.5,
        )
        axs[1].plot(mags, a_2_ppd)
        axs[1].fill_between(
            mags,
            np.percentile(lines["a_2"], limits[0], axis=0),
            np.percentile(lines["a_2"], limits[1], axis=0),
            alpha=0.5,
        )

    for ii in [1, 2]:
        axs[ii - 1].set_xlim(0, 1)
        axs[ii - 1].set_ylim(0)
        axs[ii - 1].set_xlabel(f"$a_{ii}$")
        if rate:
            ylabel = f"$\\frac{{dN}}{{da_{ii}}}$"
        else:
            ylabel = f"$p(a_{ii})$"
        axs[ii - 1].set_ylabel(ylabel)
    if len(labels) > 1:
        axs[0].legend(loc="best")

    plt.tight_layout()
    return fig


def spin_orientation_spectrum_plot(
    parameters, samples, labels=None, limits=None, rate=False
):
    if limits is None:
        limits = [5, 95]

    if labels is not None and len(labels) > 1:
        all_samples = [
            pd.DataFrame(samps, columns=params)
            for samps, params in zip(samples, parameters)
        ]
    else:
        all_samples = [pd.DataFrame(samples, columns=parameters)]
        labels = [labels]
    cos_tilts = xp.linspace(-1, 1, 1000)
    cos_tilt_1, cos_tilt_2 = xp.meshgrid(cos_tilts, cos_tilts)

    model = Model([independent_spin_orientation_gaussian_isotropic])

    fig, axs = plt.subplots(1, 2, figsize=(12, 4))

    for jj, samples in enumerate(all_samples):
        if "sigma_1" not in samples:
            samples["sigma_1"] = samples["sigma_spin"]
            samples["sigma_2"] = samples["sigma_spin"]

        data = dict(cos_tilt_1=cos_tilt_1, cos_tilt_2=cos_tilt_2)
        lines = dict(cos_tilt_1=list(), cos_tilt_2=list())
        ppd = xp.zeros_like(data["cos_tilt_1"])

        if len(samples) > MAX_SAMPLES:
            samples = samples.sample(MAX_SAMPLES)
        else:
            samples = samples

        for ii in tqdm(range(len(samples))):
            parameters = dict(samples.iloc[ii])
            model.parameters.update(parameters)
            prob = model.prob(data)
            if rate:
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

        cos_tilts = to_numpy(cos_tilts)

        cos_tilt_1_ppd = np.trapz(ppd, cos_tilts, axis=0)
        cos_tilt_2_ppd = np.trapz(ppd, cos_tilts, axis=1)

        label = labels[jj]
        if label is not None:
            label = label.replace("_", " ")

        axs[0].plot(cos_tilts, cos_tilt_1_ppd, label=label)
        axs[0].fill_between(
            cos_tilts,
            np.percentile(lines["cos_tilt_1"], limits[0], axis=0),
            np.percentile(lines["cos_tilt_1"], limits[1], axis=0),
            alpha=0.5,
        )
        axs[1].plot(cos_tilts, cos_tilt_2_ppd)
        axs[1].fill_between(
            cos_tilts,
            np.percentile(lines["cos_tilt_2"], limits[0], axis=0),
            np.percentile(lines["cos_tilt_2"], limits[1], axis=0),
            alpha=0.5,
        )

    if rate:
        ylabel = "$\\frac{{dN}}{{d\\cos t_{}}}$"
    else:
        ylabel = "$p(\\cos t_{})$"
    for ii in [1, 2]:
        axs[ii - 1].set_xlim(0, 1)
        axs[ii - 1].set_ylim(0)
        axs[ii - 1].set_xlabel(f"$\\cos t_{ii}$")
        axs[ii - 1].set_ylabel(ylabel.format(str(ii)))
    if len(labels) > 1:
        axs[0].legend(loc="best")

    plt.tight_layout()
    return fig
