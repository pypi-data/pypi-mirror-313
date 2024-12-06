from dataclasses import dataclass, field

import argparse
import glob
from functools import reduce

import dill
import h5py
import numpy as np
from bilby.core.utils import logger

from gwpopulation.utils import xp
from gwpopulation.vt import GridVT, ResamplingVT
from .utils import (
    get_cosmology,
    get_path_or_local,
    chi_eff_from_components,
    chi_p_from_components,
)
from .analytic_spin_prior import prior_chieff_chip_isotropic

N_EVENTS = np.nan


def dummy_selection(*args, **kwargs):
    return 1


def mass_only_scalar_calibrated_grid_vt(vt_file, model):
    selection = _mass_only_calibrated_grid_vt(
        vt_file=vt_file,
        model=model,
        calibration="scalar",
    )
    return selection


def mass_only_linear_calibrated_grid_vt(vt_file, model):
    selection = _mass_only_calibrated_grid_vt(
        vt_file=vt_file,
        model=model,
        calibration="linear",
    )
    return selection


def mass_only_quadratic_calibrated_grid_vt(vt_file, model):
    selection = _mass_only_calibrated_grid_vt(
        vt_file=vt_file,
        model=model,
        calibration="quadratic",
    )
    return selection


gaussian_mass_only_scalar_calibrated_grid_vt = mass_only_scalar_calibrated_grid_vt
gaussian_mass_only_linear_calibrated_grid_vt = mass_only_linear_calibrated_grid_vt
gaussian_mass_only_quadratic_calibrated_grid_vt = mass_only_quadratic_calibrated_grid_vt
broken_mass_only_scalar_calibrated_grid_vt = mass_only_scalar_calibrated_grid_vt
broken_mass_only_linear_calibrated_grid_vt = mass_only_linear_calibrated_grid_vt
broken_mass_only_quadratic_calibrated_grid_vt = mass_only_quadratic_calibrated_grid_vt


def _mass_only_calibrated_grid_vt(vt_file, model, calibration=None):
    import h5py

    model = model
    vt_data = dict()
    with h5py.File(vt_file) as _vt_data:
        vt_data["vt"] = _vt_data["vt_early_high"][:]
        if calibration is not None:
            vt_data["vt"] *= _vt_data[f"{calibration}_calibration"][:]
        vt_data["vt"] = xp.asarray(vt_data["vt"])
        vt_data["mass_1"] = xp.asarray(_vt_data["m1"][:])
        vt_data["mass_ratio"] = xp.asarray(_vt_data["q"][:])

    selection = GridVT(model=model, data=vt_data)
    return selection


@dataclass
class VTData:
    prior: np.ndarray
    total_generated: int
    analysis_time: float
    mass_1: np.ndarray = field(default=None)
    mass_1_detector: np.ndarray = field(default=None)
    mass_ratio: np.ndarray = field(default=None)
    a_1: np.ndarray = field(default=None)
    a_2: np.ndarray = field(default=None)
    cos_tilt_1: np.ndarray = field(default=None)
    cos_tilt_2: np.ndarray = field(default=None)
    chi_eff: np.ndarray = field(default=None)
    chi_p: np.ndarray = field(default=None)
    redshift: np.ndarray = field(default=None)
    luminosity_distance: np.ndarray = field(default=None)
    mass_2: np.ndarray = field(default=None)
    mass_2_detector: np.ndarray = field(default=None)

    def append(self, other):
        self_sample_rate = self.analysis_time / self.total_generated
        other_sample_rate = other.analysis_time / other.total_generated
        self_weight = 2 * self_sample_rate / (self_sample_rate + other_sample_rate)
        other_weight = 2 * other_sample_rate / (self_sample_rate + other_sample_rate)
        for key in self.__dataclass_fields__:
            value = getattr(self, key)
            alt = getattr(other, key)
            if key == "mass_2":
                if value is None and alt is None:
                    continue
                elif value is not None and alt is not None:
                    setattr(self, key, np.concatenate([value, alt]))
                else:
                    raise ValueError("mass_2 is only defined for one VTData object")
            elif key in ["total_generated", "analysis_time"]:
                setattr(self, key, value + alt)
            elif key == "prior":
                setattr(
                    self,
                    key,
                    np.concatenate([value * self_weight, alt * other_weight]),
                )
            else:
                setattr(self, key, np.concatenate([value, alt]))

    def __add__(self, other):
        new = VTData(**self.__dict__)
        new += other
        return new

    def __iadd__(self, other):
        self.append(other)
        return self

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, key, value):
        return setattr(self, key, value)

    def items(self):
        return self.__dict__.items()

    def keys(self):
        return self.__dict__.keys()

    def get(self, key, alt):
        return self.__dict__.get(key, alt)

    def to_dict(self, keys=None):
        if keys is None:
            keys = list(self.__dict__.keys())
        data = {key: getattr(self, key) for key in keys}
        return {key: value for key, value in data.items() if value is not None}


def load_injection_data(vt_file, ifar_threshold=1, snr_threshold=11):
    """
    Load the injection file in the O3 injection file format.

    For mixture files and multiple observing run files we only
    have the full `sampling_pdf`.

    We use a different parameterization than the default so we require a few
    changes.

    - we parameterize the model in terms of primary mass and mass ratio and
      the injections are generated in primary and secondary mass. The Jacobian
      is `primary mass`.
    - we parameterize spins in spherical coordinates, neglecting azimuthal
      parameters. The injections are parameterized in terms of cartesian
      spins. The Jacobian is `1 / (2 pi magnitude ** 2)`.

    For O3 injections we threshold on FAR.
    For O1/O2 injections we threshold on SNR as there is no FAR
    provided by the search pipelines.

    Parameters
    ----------
    vt_file: str
        The path to the hdf5 file containing the injections.
    ifar_threshold: float
        The threshold on inverse false alarm rate in years. Default=1.
    snr_threshold: float
        The SNR threshold when there is no FAR. Default=11.

    Returns
    -------
    gwpop_data: dict
        Data required for evaluating the selection function.

    """
    logger.info(f"Loading VT data from {vt_file}.")
    if vt_file.endswith(".pkl"):
        with open(vt_file, "rb") as ff:
            data = dill.load(ff)
        for key, value in data.items():
            if isinstance(value, np.ndarray):
                data[key] = xp.asarray(value)
        return VTData(**data)

    with h5py.File(vt_file, "r") as ff:
        if "injections" in ff:
            data = ff["injections"]
            total_generated = int(data.attrs["total_generated"][()])
            analysis_time = data.attrs["analysis_time_s"][()] / 365.25 / 24 / 60 / 60
        elif "events" in ff:
            keys_of_interest = {
                "mass1_source",
                "mass2_source",
                "mass_1_source",
                "mass_2_source",
                "spin1x",
                "spin1y",
                "spin1z",
                "spin2x",
                "spin2y",
                "spin2z",
                "redshift",
                "z",
                "sampling_pdf",
                "lnpdraw_mass1_source_mass2_source_redshift_spin1x_spin1y_spin1z_spin2x_spin2y_spin2z",
                "lnpdraw_mass1_source",
                "lnpdraw_mass2_source_GIVEN_mass1_source",
                "lnpdraw_z",
                "lnpdraw_spin1_magnitude",
                "lnpdraw_spin2_magnitude",
                "lnpdraw_spin1_polar_angle",
                "lnpdraw_spin2_polar_angle",
                "v1_1ifo",
                "weights",
                "weights_1ifo",
                "name",
                "observed_phase_maximized_snr_net",
                "observed_snr_net",
                "optimal_snr_net",
                "semianalytic_observed_phase_maximized_snr_net",
            }
            keys = list(keys_of_interest.intersection(ff["events"].dtype.names))
            for substr in ["far", "ifar"]:
                keys += [
                    key
                    for key in ff["events"].dtype.names
                    if any(
                        [
                            key.startswith(f"{substr}_"),
                            key.endswith(f"_{substr}"),
                            f"_{substr}_" in key,
                        ]
                    )
                ]

            data = {key: np.array(ff["events"][key][()]) for key in keys}
            total_generated = int(ff.attrs["total_generated"][()])
            # the name applied to the analysis time changes between files, so we
            # loop over all plausible values and break once we find one
            for key in [
                "total_analysis_time",
                "analysis_time",
                "total_analysis_time_1ifo",
            ]:
                if key in ff.attrs:
                    analysis_time = ff.attrs[key][()] / 365.25 / 24 / 60 / 60
                    break
            else:
                raise AttributeError(
                    "Provided injection file does not provide analysis time"
                )
            if analysis_time == 0:
                analysis_time = 1 / 12
        else:
            raise KeyError(f"Unable to identify injections from {ff.keys()}")

        if "mass1_source" in data:
            mass_1_key = "mass1_source"
            mass_2_key = "mass2_source"
        else:
            mass_1_key = "mass_1_source"
            mass_2_key = "mass_2_source"
        if "redshift" in data:
            redshift_key = "redshift"
        else:
            redshift_key = "z"
        found_shape = data[mass_1_key][()].shape
        found = get_found_injections(data, found_shape, ifar_threshold, snr_threshold)
        n_found = sum(found)
        if n_found == 0:
            raise ValueError("No sensitivity injections pass threshold.")
        gwpop_data = dict(
            mass_1=xp.asarray(data[mass_1_key][()][found]),
            mass_ratio=xp.asarray(
                data[mass_2_key][()][found] / data[mass_1_key][()][found]
            ),
            redshift=xp.asarray(data[redshift_key][()][found]),
            total_generated=total_generated,
            analysis_time=analysis_time,
        )
        for ii in [1, 2]:
            gwpop_data[f"a_{ii}"] = (
                xp.asarray(
                    data.get(f"spin{ii}x", np.zeros(n_found))[()][found] ** 2
                    + data.get(f"spin{ii}y", np.zeros(n_found))[()][found] ** 2
                    + data[f"spin{ii}z"][()][found] ** 2
                )
                ** 0.5
            )
            gwpop_data[f"cos_tilt_{ii}"] = (
                xp.asarray(data[f"spin{ii}z"][()][found]) / gwpop_data[f"a_{ii}"]
            )
        if (
            "sampling_pdf" in data
        ):  # O1+O2+O3 mixture and endO3 injections (https://dcc.ligo.org/LIGO-T2100377, https://dcc.ligo.org/LIGO-T2100113)
            gwpop_data["prior"] = (
                xp.asarray(data["sampling_pdf"][()][found])
                * xp.asarray(data[mass_1_key][()][found])
                * (2 * np.pi * gwpop_data["a_1"] ** 2)
                * (2 * np.pi * gwpop_data["a_2"] ** 2)
            )
        elif (
            "lnpdraw_mass1_source_mass2_source_redshift_spin1x_spin1y_spin1z_spin2x_spin2y_spin2z"
            in data
        ):  # O1+O2+O3+O4a mixture (https://dcc.ligo.org/LIGO-T2400110)
            gwpop_data["prior"] = xp.exp(
                xp.asarray(
                    data[
                        "lnpdraw_mass1_source_mass2_source_redshift_spin1x_spin1y_spin1z_spin2x_spin2y_spin2z"
                    ][()][found]
                )
                + xp.log(xp.asarray(data[mass_1_key][()][found]))
                + xp.log(2 * np.pi * gwpop_data["a_1"] ** 2)
                + xp.log(2 * np.pi * gwpop_data["a_2"] ** 2)
            )
        else:  # O4a sensitivity injections (https://dcc.ligo.org/LIGO-T2400073)
            gwpop_data["prior"] = xp.exp(
                xp.sum(
                    [
                        xp.asarray(data[f"lnpdraw_{key}"][()][found])
                        for key in [
                            "mass1_source",
                            "mass2_source_GIVEN_mass1_source",
                            "z",
                            "spin1_magnitude",
                            "spin2_magnitude",
                            "spin1_polar_angle",
                            "spin2_polar_angle",
                        ]
                    ],
                    axis=0,
                )
            )
            gwpop_data["prior"] /= xp.sin(xp.arccos(gwpop_data["cos_tilt_1"]))
            gwpop_data["prior"] /= xp.sin(xp.arccos(gwpop_data["cos_tilt_2"]))
            gwpop_data["prior"] *= gwpop_data["mass_1"]

        weights = 1
        if "v1_1ifo" in vt_file:
            weights *= xp.asarray(data["weights_1ifo"][()][found])
        elif "weights" in data:
            weights *= xp.asarray(data["weights"][()][found])
        gwpop_data["prior"] /= weights
    return VTData(**gwpop_data)


def get_found_injections(data, shape, ifar_threshold=1, snr_threshold=11):
    found = np.zeros(shape, dtype=bool)
    has_ifar = any(["ifar" in key.lower() for key in data.keys()])

    far_keys = list(
        filter(
            lambda key: (
                key.lower().startswith("far_")
                or key.lower().endswith("_far")
                or "_far_" in key.lower()
            ),
            data,
        )
    )

    if not has_ifar and len(far_keys) > 0:
        for far_key in far_keys:
            data[far_key.replace("far", "ifar")] = 1 / data[far_key][()]
        has_ifar = True
    if ifar_threshold is None:
        ifar_threshold = 1e300
    if has_ifar:
        for key in data:
            if "ifar" in key.lower():
                found |= data[key][()] > ifar_threshold
            if "name" in data.keys():
                gwtc1 = (data["name"][()] == b"o1") | (data["name"][()] == b"o2")
                found |= gwtc1 & (data["optimal_snr_net"][()] > snr_threshold)
        if "semianalytic_observed_phase_maximized_snr_net" in data.keys():
            found |= (
                data["semianalytic_observed_phase_maximized_snr_net"][()]
                > snr_threshold
            )
        return found
    elif snr_threshold is not None:
        if "observed_phase_maximized_snr_net" in data.keys():
            found |= data["observed_phase_maximized_snr_net"][()] > snr_threshold
        elif "observed_snr_net" in data.keys():
            found |= data["observed_snr_net"][()] > snr_threshold
        return found
    else:
        raise ValueError("Cannot find keys to filter sensitivity injections.")


def apply_injection_prior(data, parameters):
    """
    We assume the injection prior is uniform in the detector frame primary
    mass and mass ratio.
    """
    from .data_collection import primary_mass_to_chirp_mass_jacobian, aligned_spin_prior

    if "mass_2" in parameters:
        data["mass_2"] = data["mass_1"] * data["mass_ratio"]
        data["prior"] /= data["mass_1"]
    if "chirp_mass" in parameters:
        jacobian = primary_mass_to_chirp_mass_jacobian(data)
        data["chirp_mass"] = data["mass_1"] / jacobian
        data["prior"] *= jacobian
    if "chi_eff" in parameters:
        data["chi_eff"] = chi_eff_from_components(
            a_1=data["a_1"],
            cos_tilt_1=data["cos_tilt_1"],
            a_2=data["a_2"],
            cos_tilt_2=data["cos_tilt_2"],
            mass_ratio=data["mass_ratio"],
        )
        if "chi_p" in parameters:
            data["chi_p"] = chi_p_from_components(
                a_1=data["a_1"],
                cos_tilt_1=data["cos_tilt_1"],
                a_2=data["a_2"],
                cos_tilt_2=data["cos_tilt_2"],
                mass_ratio=data["mass_ratio"],
            )
            amax = 1
            logger.info(
                f"Applying isotropic prior to chi_eff and chi_p, assuming injections with amax={amax}."
            )
            p_chi_iso = prior_chieff_chip_isotropic(
                data["chi_eff"], data["chi_p"], data["mass_ratio"], amax=amax
            )
            p_magnitude_costilt_iso = (1 / 2) ** 2 * (1 / amax) ** 2
            data["prior"] *= p_chi_iso / p_magnitude_costilt_iso
    if "chi_1" in parameters:
        data["chi_1"] = data["a_1"] * data["cos_tilt_1"]
        data["prior"] *= 2 * aligned_spin_prior(data["chi_1"])
    if "chi_2" in parameters:
        data["chi_2"] = data["a_2"] * data["cos_tilt_2"]
        data["prior"] *= 2 * aligned_spin_prior(data["chi_2"])
    if "mass_1_detector" in parameters:
        data["mass_1_detector"] = data["mass_1"] * (1 + data["redshift"])
        data["prior"] /= 1 + data["redshift"]
    if "mass_2_detector" in parameters:
        data["mass_2_detector"] = data["mass_1_detector"] * data["mass_ratio"]
        data["prior"] /= data["mass_1_detector"]
    if "chirp_mass_detector" in parameters:
        jacobian = primary_mass_to_chirp_mass_jacobian(data)
        try:
            data["chirp_mass_detector"] = data["mass_1_detector"] / jacobian
            data["prior"] *= jacobian
        except (KeyError, AttributeError, TypeError):
            data["chirp_mass_detector"] = (
                data["mass_1"] * (1 + data["redshift"]) / jacobian
            )
            data["prior"] *= jacobian / (1 + data["redshift"])
    if "luminosity_distance" in parameters:
        cosmo = get_cosmology("Planck15_LAL")

        data["luminosity_distance"] = cosmo.luminosity_distance(data["redshift"])
        data["prior"] /= cosmo.dDLdz(data["redshift"])


def dump_injection_data(args, save_filename=None):
    """
    Dump the injection data to a pickle file to :code:`{args.run_dir}/data/injections.pkl` for easier file transfer.

    This also makes sure the required parameters are present in the data and updates the prior accordingly.

    Parameters
    ----------
    args:
        Command-line arguments
    save_filename:
        The filename to save the data to. If None, it will save the data to args.run_dir/data/injections.pkl.
    """
    if "*" in args.vt_file:
        data = reduce(
            lambda x, y: x + y,
            [
                load_injection_data(
                    vt_file=get_path_or_local(vt_file),
                    ifar_threshold=args.vt_ifar_threshold,
                    snr_threshold=args.vt_snr_threshold,
                )
                for vt_file in glob.glob(args.vt_file)
            ],
        )
    else:
        data = load_injection_data(
            vt_file=get_path_or_local(args.vt_file),
            ifar_threshold=args.vt_ifar_threshold,
            snr_threshold=args.vt_snr_threshold,
        )
    apply_injection_prior(data, args.parameters)
    if save_filename is None:
        fname = f"{args.run_dir}/data/injections.pkl"
    else:
        fname = save_filename
    data_dict = data.to_dict()
    keys = args.parameters.copy() + ["prior", "total_generated", "analysis_time"]
    data_dict = {key: value for key, value in data_dict.items() if key in keys}
    with open(fname, "wb") as ff:
        dill.dump(data_dict, ff)
    logger.info(f"Written injection data to {fname}")


def injection_resampling_vt(vt_file, model, ifar_threshold=1, snr_threshold=11):

    if "*" in vt_file:
        vt_files = glob.glob(vt_file)
        data = sum(
            [
                load_injection_data(
                    vt_file=get_path_or_local(filename),
                    ifar_threshold=ifar_threshold,
                    snr_threshold=snr_threshold,
                )
                for filename in vt_files
            ]
        )
    else:
        data = load_injection_data(
            vt_file=get_path_or_local(vt_file),
            ifar_threshold=ifar_threshold,
            snr_threshold=snr_threshold,
        )

    return ResamplingVT(model=model, data=data.to_dict(), n_events=N_EVENTS)


def injection_resampling_vt_no_redshift(
    vt_file, model, ifar_threshold=1, snr_threshold=11
):

    data = load_injection_data(
        vt_file=vt_file, ifar_threshold=ifar_threshold, snr_threshold=snr_threshold
    )
    data["prior"] = data["mass_1"] ** (-2.35 + 1) * data["mass_ratio"] ** 2

    return ResamplingVT(model=model, data=data.to_dict(), n_events=N_EVENTS)


def create_injection_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "vt_file",
        type=str,
        help="File to load VT data from or a glob string matching multiple files to combine.",
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
        help="SNR threshold for resampling injections. "
        "This is only used for O1/O2 injections",
    )
    parser.add_argument(
        "--vt-function",
        type=str,
        default="injection_resampling_vt",
        help="Function to generate selection function from.",
    )

    parser.add_argument(
        "--parameters",
        "-p",
        action="append",
        help=(
            "Parameters that are fit with the model. "
            "These are the parameters that will be extracted from the injections "
            "and should follow Bilby naming conventions with the exception that all masses "
            "are assumed to be in the source frame. Here is a list of parameters for which "
            "prior factors will be properly accounted. "
            "mass_1: source frame primary mass, mass_2: source frame secondary mass, "
            "chirp_mass: source frame chirp mass, mass_ratio: mass ratio, redshift: redshift, "
            "a_1: primary spin magnitude, a_2: secondary spin magnitude, cos_tilt_1: "
            "cosine primary spin tilt, cos_tilt_2: cosine secondary spin tilt, "
            "chi_1: aligned primary spin, chi_2: aligned secondary spin."
            "Any other parameters will be assumed to have a flat prior."
            "These parameters are also used to set the fiducial prior values. "
            "No redundancy checks are performed so users should be careful to not "
            "include unused parameters as that may have unintended consequences."
        ),
    )

    parser.add_argument(
        "--save_as",
        "-s",
        type=str,
        default="injections.pkl",
        help="name of pickle file to save the injections",
    )

    return parser


def read_injections():
    parser = create_injection_parser()
    args = parser.parse_args()
    save_file = args.save_as
    save_file = save_file.split(".pkl")[0] + ".pkl"
    dump_injection_data(args, save_file)
