import os

from gwpopulation.conversions import convert_to_beta_parameters
from gwpopulation.hyperpe import HyperparameterLikelihood, xp
from gwpopulation.models.spin import (
    iid_spin,
    iid_spin_magnitude_beta,
    independent_spin_magnitude_beta,
)


def get_cosmology(name):
    from wcosmo.astropy import FlatLambdaCDM, available

    if name.lower() == "planck15_lal":
        return FlatLambdaCDM(H0=67.90, Om0=0.3065, name="Planck15_LAL")
    elif name in available.keys():
        return available[name]
    else:
        raise ValueError(f"Unknown cosmology {name}")


def prior_conversion(parameters):
    """Wrapper around conversion for prior constraints"""
    for key in ["amax", "amax_1", "amax_2"]:
        if key not in parameters:
            parameters[key] = 1
    parameters, _ = convert_to_beta_parameters(parameters)
    return parameters


def get_path_or_local(path: str) -> str:
    """
    Check if a path exists, if not check if the basename exists, if not raise an error.

    Parameters
    ----------
    path: str
        The path to check.

    Returns
    -------
    path: str
        The path to use.

    Raises
    ------
    ValueError
        If neither the path nor the basename exist.
    """
    if os.path.exists(path):
        return path
    elif os.path.exists(os.path.basename(path)):
        return os.path.basename(path)
    else:
        raise ValueError(f"Cannot find {path} or {os.path.basename(path)}")


def chi_eff_from_components(a_1, cos_tilt_1, a_2, cos_tilt_2, mass_ratio):
    """
    Compute the effective spin parameter from the component spins.

    Parameters
    ----------
    a_1: array-like
        The magnitude of the primary spin.
    cos_tilt_1: array-like
        The cosine of the tilt of the primary spin.
    a_2: array-like
        The magnitude of the secondary spin.
    cos_tilt_2: array-like
        The cosine of the tilt of the secondary spin.
    mass_ratio: array-like
        The mass ratio of the binary.

    Returns
    -------
    chi_eff: array-like
        The effective spin parameter.
    """
    return (a_1 * cos_tilt_1 + mass_ratio * a_2 * cos_tilt_2) / (1 + mass_ratio)


def chi_p_from_components(a_1, cos_tilt_1, a_2, cos_tilt_2, mass_ratio):
    """
    Compute the precession spin parameter from the component spins.

    Parameters
    ----------
    a_1: array-like
        The magnitude of the primary spin.
    cos_tilt_1: array-like
        The cosine of the tilt of the primary spin.
    a_2: array-like
        The magnitude of the secondary spin.
    cos_tilt_2: array-like
        The cosine of the tilt of the secondary spin.
    mass_ratio: array-like
        The mass ratio of the binary.

    Returns
    -------
    chi_p: array-like
        The precession spin parameter.
    """
    sin_tilt_1 = xp.sqrt(1 - cos_tilt_1**2)
    sin_tilt_2 = xp.sqrt(1 - cos_tilt_2**2)
    return xp.maximum(
        a_1 * sin_tilt_1,
        (3 + 4 * mass_ratio) / (4 + 3 * mass_ratio) * mass_ratio * a_2 * sin_tilt_2,
    )


KNOWN_ARGUMENTS = {
    iid_spin: ["mu_chi", "sigma_chi", "xi_spin", "sigma_spin"],
    iid_spin_magnitude_beta: ["mu_chi", "sigma_chi"],
    independent_spin_magnitude_beta: [
        "mu_chi_1",
        "mu_chi_2",
        "sigma_chi_1",
        "sigma_chi_2",
    ],
}


class MinimumEffectiveSamplesLikelihood(HyperparameterLikelihood):
    def _compute_per_event_ln_bayes_factors(self, return_uncertainty=True):
        """
        Compute the per event ln Bayes factors and associated variance.

        This method imposes a condition that the number of effective
        samples per Monte Carlo integral must be at least as much
        as the total number of events. Otherwise the lnBF is set to
        - infinity.

        Returns
        -------
        ln_per_event_bfs: array-like
            The ln BF per event subject to having a sufficient number
            of independent samples.
        variance: array-like
            The variances (uncertainties) in the ln BF per event. Only
            returned if `return_uncertainty` is True. This output will
            generally not be used for convergence criteria, as this function
            already enforces a threshold on effective number of samples.
        """
        (
            per_event_bfs,
            n_effectives,
            variance,
        ) = self.per_event_bayes_factors_and_n_effective_and_variances()
        per_event_bfs *= n_effectives > self.n_posteriors
        if return_uncertainty:
            return xp.log(per_event_bfs), variance
        else:
            return xp.log(per_event_bfs)

    def per_event_bayes_factors_and_n_effective_and_variances(self):
        """
        Called by `_compute_per_event_ln_bayes_factors` to compute the
        per event BFs, effective number of samples for each event's computed
        BF, and the associated uncertainty (variance) in the *ln* BF. Computes
        same qunatities as superclass function `_compute_per_event_ln_bayes_factors`
        but additionally provides the effective sample size.

        Returns
        -------
        per_event_bfs: array-like
            The BF per event, computed by reweighting single-event likelihood
            samples into the `hyper_prior` model.
        n_effectives: array-like
            The effective sample size for each Monte Carlo sum computation of the BFs.
            The BF is computed for each event, so this array has length n_events.
        variance: array-like
            The variances (uncertainties) in the ln BF per event.
        """
        weights = self.hyper_prior.prob(self.data) / self.sampling_prior
        per_event_bfs = xp.sum(weights, axis=-1)
        n_effectives = xp.nan_to_num(per_event_bfs**2 / xp.sum(weights**2, axis=-1))
        per_event_bfs /= self.samples_per_posterior
        square_expectation = xp.mean(weights**2, axis=-1)
        variance = (square_expectation - per_event_bfs**2) / (
            self.samples_per_posterior * per_event_bfs**2
        )
        return per_event_bfs, n_effectives, variance

    def per_event_bayes_factors_and_n_effective(self):
        (
            per_event_bfs,
            n_effectives,
            _,
        ) = self.per_event_bayes_factors_and_n_effective_and_variances()
        return per_event_bfs, n_effectives


def maybe_jit(func):
    from gwpopulation.backend import __backend__

    if __backend__ == "jax":
        from jax import jit

        return jit(func)
    else:
        return func
