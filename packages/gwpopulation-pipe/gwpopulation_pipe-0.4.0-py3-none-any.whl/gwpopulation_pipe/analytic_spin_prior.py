# Adapted from transformations derived in Iwaya et al. 2024

import numpy as np
from gwpopulation.utils import to_numpy, xp

try:
    import jax
except ImportError:
    pass
from scipy.special import spence as scipyspence
from .utils import maybe_jit

# Relative tolerance for the series
TOL = 2.220446092504131e-16
PISQ_6 = 1.6449340668482264365
MAX_ITER = 500


def I1(chieff, chip, q):
    x1max = xp.minimum(
        xp.sqrt(q**2 - ((4 + 3 * q) / (3 + 4 * q)) ** 2 * chip**2),
        (1 + q) * chieff + xp.sqrt(1 - chip**2),
    )
    x1min = xp.maximum(
        -xp.sqrt(q**2 - ((4 + 3 * q) / (3 + 4 * q)) ** 2 * chip**2),
        (1 + q) * chieff - xp.sqrt(1 - chip**2),
    )
    cond1 = chip > 0
    cond2 = q >= (4 + 3 * q) * chip / (3 + 4 * q)
    cond3 = x1max >= x1min

    Fterm = F(x1max, (1 + q) * chieff, chip, (4 + 3 * q) / (3 + 4 * q) * chip, q) - F(
        x1min, (1 + q) * chieff, chip, (4 + 3 * q) / (3 + 4 * q) * chip, q
    )
    return xp.where(cond1 & cond2 & cond3, (1 + q) / (8 * q) * Fterm, 0)


def I2(chieff, chip, q):
    x2max = xp.minimum(q, (1 + q) * chieff + xp.sqrt(1 - chip**2))
    x2min = xp.maximum(-q, (1 + q) * chieff - xp.sqrt(1 - chip**2))

    cond1 = chip > 0
    cond2 = chip < 1
    cond3 = x2max >= x2min

    Fterm = F(x2max, (1 + q) * chieff, chip, 0, q) - F(
        x2min, (1 + q) * chieff, chip, 0, q
    )
    return xp.where(cond1 & cond2 & cond3, -(1 + q) / (8 * q) * Fterm, 0)


def I3(chieff, chip, q):
    x3max = xp.minimum(
        xp.sqrt(1 - chip**2),
        (1 + q) * chieff
        + xp.sqrt(q**2 - ((4 + 3 * q) / (3 + 4 * q)) ** 2 * chip**2),
    )
    x3min = xp.maximum(
        -xp.sqrt(1 - chip**2),
        (1 + q) * chieff
        - xp.sqrt(q**2 - ((4 + 3 * q) / (3 + 4 * q)) ** 2 * chip**2),
    )

    cond1 = chip > 0
    cond2 = q >= (4 + 3 * q) * chip / (3 + 4 * q)
    cond3 = x3max > x3min

    Fterm = F(x3max, (1 + q) * chieff, (4 + 3 * q) / (3 + 4 * q) * chip, chip, 1) - F(
        x3min, (1 + q) * chieff, (4 + 3 * q) / (3 + 4 * q) * chip, chip, 1
    )

    return xp.where(
        cond1 & cond2 & cond3, (1 + q) / (8 * q) * (4 + 3 * q) / (3 + 4 * q) * Fterm, 0
    )


def I4(chieff, chip, q):
    x4max = xp.minimum(
        1,
        (1 + q) * chieff
        + xp.sqrt(q**2 - ((4 + 3 * q) / (3 + 4 * q)) ** 2 * chip**2),
    )
    x4min = xp.maximum(
        -1,
        (1 + q) * chieff
        - xp.sqrt(q**2 - ((4 + 3 * q) / (3 + 4 * q)) ** 2 * chip**2),
    )

    cond1 = chip > 0
    cond2 = q >= (4 + 3 * q) * chip / (3 + 4 * q)
    cond3 = x4max > x4min

    Fterm = F(x4max, (1 + q) * chieff, (4 + 3 * q) / (3 + 4 * q) * chip, 0, 1) - F(
        x4min, (1 + q) * chieff, (4 + 3 * q) / (3 + 4 * q) * chip, 0, 1
    )

    return xp.where(
        cond1 & cond2 & cond3, -(1 + q) / (8 * q) * (4 + 3 * q) / (3 + 4 * q) * Fterm, 0
    )


def F(x, a, b, c, d):
    return G(x / b, a / b, c / b) + xp.log(b**2 / d**2) * (
        xp.arctan((x - a) / b) + xp.arctan(a / b)
    )


def G(x, alpha, beta):
    pre = xp.where(x >= 0, 1, -1)
    alpha = xp.where(x >= 0, alpha, -alpha)
    x = xp.where(x >= 0, x, -x)
    g1 = g(x, alpha, beta)
    g2 = g(x, alpha, -beta)
    g3 = -g(0, alpha, beta)
    g4 = -g(0, alpha, -beta)

    out = pre * xp.imag(g1 + g2 + g3 + g4)
    return out


def g(x, alpha, beta):
    cond1 = xp.abs(beta) < 1
    cond2 = (beta == 1) & (alpha <= 0)
    x_ = xp.where((x == 0) & (beta == 0), 0.01, x)
    ret = xp.nan_to_num(
        xp.where(
            cond1,
            xp.log(x_ - beta * 1j)
            * xp.log((alpha - x_ + 1j) / (alpha + 1j - beta * 1j))
            + Li2((x_ - beta * 1j) / (alpha + 1j - beta * 1j)),
            xp.where(
                cond2,
                0.5 * (xp.log(x_ - alpha - 1j)) ** 2 + Li2(-alpha / (x_ - alpha - 1j)),
                xp.log(alpha + 1j - beta * 1j) * xp.log(alpha - x_ + 1j)
                - Li2((alpha - x_ + 1j) / (alpha + 1j - beta * 1j)),
            ),
        )
    )
    return xp.where((x == 0) & (beta == 0), 0, ret)


def jaxspence(z):
    """
    From scipy.special.spence's implementation:
    Compute Spence's function for complex arguments. The strategy is:
    - If z is close to 0, use a series centered at 0.
    - If z is far away from 1, use the reflection formula

    spence(z) = -spence(z/(z - 1)) - pi**2/6 - ln(z - 1)**2/2

    to move close to 1.
    - If z is close to 1, use a series centered at 1.

    """
    return jax.lax.cond(
        xp.abs(z) < 0.5,
        lambda z: cspence_series0(z),
        lambda z: jax.lax.cond(
            xp.abs(1 - z) > 1,
            lambda z: -cspence_series1(z / (z - 1)) - PISQ_6 - 0.5 * xp.log(z - 1) ** 2,
            lambda z: cspence_series1(z),
            z,
        ),
        z,
    )


def cspence_series0(z):
    """
    A series centered at z = 0; see

    http://functions.wolfram.com/10.07.06.0005.02

    """
    z_ = xp.where(z == 0, 0.01, z)

    def condition(args):
        n, zfac, term1, sum1, term2, sum2 = args
        return (
            (xp.abs(term1) > TOL * xp.abs(sum1)) | (xp.abs(term2) > TOL * xp.abs(sum2))
        ) & (n < MAX_ITER)

    def body(args):
        n, zfac, term1, sum1, term2, sum2 = args
        zfac *= z_
        term1 = zfac / n**2
        sum1 += term1
        term2 = zfac / n
        sum2 += term2
        return (n + 1, zfac, term1, sum1, term2, sum2)

    def body_fori(i, args):
        return body(args)

    n, zfac, term1, sum1, term2, sum2 = jax.lax.fori_loop(
        1, MAX_ITER, body_fori, (1, 1, 0, 0, 0, 0)
    )

    # n, zfac, term1, sum1, term2, sum2 = jax.lax.while_loop(
    # condition, body, (1, 1, xp.inf, 0, xp.inf, 0)
    # )
    return xp.where(z == 0, PISQ_6, PISQ_6 - sum1 + xp.log(z_) * sum2)


def cspence_series1(z):
    """
    A series centered at z = 1 which enjoys faster convergence than
    the Taylor series. The number of terms used comes from
    bounding the absolute tolerance at the edge of the radius of
    convergence where the sum is O(1).

    """

    z_ = xp.where(z == 1, 1 - 1e-10, z)

    z_ = 1 - z_
    zz = z_**2

    def condition(args):
        n, zfac, res, term = args
        return (xp.abs(term) > TOL * xp.abs(res)) & (n < MAX_ITER)

    def body(args):
        n, zfac, res, _ = args
        zfac *= z_
        term = ((zfac / n**2) / (n + 1) ** 2) / (n + 2) ** 2
        res += term
        return (n + 1, zfac, res, term)

    def body_fori(i, args):
        return body(args)

    n, zfac, res, term = jax.lax.fori_loop(1, MAX_ITER, body_fori, (1, 1, 0, xp.inf))
    # n, zfac, res, term = jax.lax.while_loop(condition, body, (1, 1, 0, xp.inf))
    res *= 4 * zz
    res += 4 * z_ + 5.75 * zz + 3 * (1 - zz) * xp.log(1 - z_)
    res /= 1 + 4 * z_ + zz
    return xp.where(z == 1, 0.0, res)


def Li2(z):
    if "jax" in xp.__name__:
        spence = jax.vmap(jaxspence)
    else:
        from scipy.special import spence
    z = xp.atleast_1d(z)
    return spence(1 - z)


@maybe_jit
def prior_chieff_chip_isotropic(chieff, chip, q, amax=1):
    chieff = chieff / amax
    chip = chip / amax
    return (
        I1(chieff, chip, q)
        + I2(chieff, chip, q)
        + I3(chieff, chip, q)
        + I4(chieff, chip, q)
    ) / amax**2
