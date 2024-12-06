from gwpopulation.utils import truncnorm


def all_the_gaussians(
    dataset,
    mean_mass,
    sigma_mass,
    mean_magnitude,
    sigma_magnitude,
    mean_tilt,
    sigma_tilt,
    mean_redshift,
    sigma_redshift,
):
    """
    A simple model to use a test case for numpyro.

    We use a truncated normal for all variables and apply a log-transform to the mass
    """
    from gwpopulation.utils import xp

    prob = truncnorm(dataset["redshift"], mean_redshift, sigma_redshift, low=0, high=3)
    for ii in [1, 2]:
        mass = dataset[f"mass_{ii}"]
        log_mass = xp.log10(mass)
        prob *= truncnorm(log_mass, mean_mass, sigma_mass, low=0, high=2.5) / mass
        prob *= truncnorm(
            dataset[f"a_{ii}"], mean_magnitude, sigma_magnitude, low=0, high=1
        )
        prob *= truncnorm(
            dataset[f"cos_tilt_{ii}"], mean_tilt, sigma_tilt, low=-1, high=1
        )
    return prob
