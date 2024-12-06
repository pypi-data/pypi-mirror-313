"""
Translation of the cython implementation of complex Spence
from scipy to work with jax.
Adapted from https://github.com/scipy/scipy/blob/8971d5e9b72931987b7d3c5a25da1a8e7e5485d0/scipy/special/_spence.pxd
"""

import jax.numpy as jnp

TOL = 1e-15

def cspence_series0(z):
    """
    Small z branch, uses a series expansion about :math:`z = 0`
    for :math:`|z| < 0.5`.
    """

    def body_func(val):
        z, zfac, n, sum1, sum2, term1, term2 = val
        zfac *= z
        term1 = zfac / n**2
        sum1 += term1
        term2 = zfac / n
        sum2 += term2
        n = n + 1
        return jnp.array([z, zfac, n, sum1, sum2, term1, term2])
    
    def cond_fun(val):
        z, zfac, n, sum1, sum2, term1, term2 = val
        return (n > 500) | (
            (abs(term1) > TOL * abs(sum1))
            & (abs(term2) > TOL * abs(sum2))
        )

    val = jnp.array([z, 1.0, 1, 0, 0, 1, 1])
    result = while_loop(cond_fun, body_func, val)
    sum1 = result[3]
    sum2 = result[4]
    return np.pi**2 / 6 - sum1 + jnp.log(z) * sum2


def cspence_series1(z):
    """
    Middle branch, an expansion around :math:`z = 1`
    for :math:`|z| > 0.5` and :math:`|1 - z| > 1`.
    """

    def body_func(val):
        z, zfac, n, res, term = val
        zfac *= z
        term = ((zfac/n**2)/(n + 1)**2)/(n + 2)**2
        res += term
        n = n + 1
        return jnp.array([z, zfac, n, res, term])
    
    def cond_fun(val):
        z, zfac, n, res, term = val
        return (n > 500) | (abs(term) > 1e-15 * abs(res))

    z = 1 - z
    zz = z**2
    val = jnp.array([z, 1.0, 1, 0, 1])
    result = while_loop(cond_fun, body_func, val)
    res = result[3] * 4 * zz
    res += 4 * z + 5.75 * zz + 3 * (1 - zz) * jnp.log(1 - z)
    res /= 1 + 4 * z + zz
    return res


def cspence_series2(z):
    """
    Large :math:`z` branch for :math:`|z| > 0.5` and
    :math:`|1 - z| > 1`. Uses a reflection expression.
    """
    return (
        -cspence_series1(z / (z - 1))
        - np.pi**2 / 6
        - jnp.log(z - 1)**2 / 2
    )


def cspence(z):
    """
    Return the Spence dilogarithm for complex input using
    branches dependent on the value of the input.
    """
    return cond(
        abs(z) < 0.5,
        cspence_series0,
        lambda z: cond(
            abs(1 - z) > 1,
            cspence_series2,
            cspence_series1,
            z,
        ),
        z,
    )
