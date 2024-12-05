"""
This module contains symbolic definitions of available metric line elements.

Line elements can be imported via the dictionary metric_line_elements with the
corresponding key.
"""

from collections.abc import Callable
import numpy as np
import sympy
from sympy.core.expr import Expr as expression
from scipy.constants import c


x0, r, theta, phi = sympy.symbols('x0 r theta phi')


def gravitational_potential(
        multipole_moments: list[float],
        radius_reference: float,
        gravity_constant: float,
) -> expression:
    """Calculate gravitational potential symbolically in spherical-like coords.

    Parameters
    ----------
    multipole_moments
        Multipole moments of the gravitational potential. When interested in
        higher-order moments, add the required terms.
    radius_reference
        Radius coordinate for gravitating mass' reference/average height.
    gravity_constant
        Gravitating mass' measured gravity constant.

    Returns
    -------
    expression
        Gravitational potential at the given coordinates.
    """

    potential = - gravity_constant / r * (
            multipole_moments[0]
            + multipole_moments[1] * radius_reference / r * sympy.sin(theta)
    )

    return potential


def centrifugal_potential(period_rotation: float) -> expression:
    """Calculate centrifugal potential symbolically in spherical-like coords.

    Parameters
    ----------
    period_rotation
        Gravitating mass' period of rotation.

    Returns
    -------
    expression
        Centrifugal potential at the given coordinates.
    """

    potential = - (
        (2 * np.pi / period_rotation) ** 2 * r ** 2 * sympy.sin(theta) ** 2
    ) / 2

    return potential


def post_newton(
        multipole_moments: list[float],
        radius_reference: float,
        gravity_constant: float,
        period_rotation: float
) -> expression:
    """Calculate line element symbolically in spherical-like coordinates.

    The components metric_00 and metric_ij are given in harmonic coordinates,
    which need to be transformed into spherical coordinates via the standard
    coordinate transformation (see metric).

    Parameters
    ----------
    multipole_moments
        Multipole moments of the gravitational potential. When interested in
        higher-order moments, add the required terms to the
        gravitational_potential function.
    radius_reference
        Radius coordinate for gravitating mass' reference/average height.
    gravity_constant
        Gravitating mass' measured gravity constant.
    period_rotation
        Gravitating mass' period of rotation.

    Returns
    -------
    expression
        post-Newtonian metric line element at the given coordinates.
    """

    gravitational_pot = gravitational_potential(
        multipole_moments,
        radius_reference,
        gravity_constant,
    )

    centrifugal_pot = centrifugal_potential(period_rotation)

    metric_00 = -(1
                  + 2 * (gravitational_pot + centrifugal_pot) / c ** 2
                  + 2 * (gravitational_pot + centrifugal_pot) ** 2 / c ** 4)

    metric_ij = 1 - 2 * gravitational_pot / c ** 2

    metric = sympy.Matrix([
        [metric_00, 0, 0, 0],
        [0, metric_ij, 0, 0],
        [0, 0, metric_ij * r ** 2, 0],
        [0, 0, 0, metric_ij * r ** 2 * sympy.sin(theta) ** 2],
    ])

    return metric


def schwarzschild(multipole_moments: list[float]) -> expression:
    """Calculate line element symbolically in spherical-like coordinates.

    Parameters
    ----------
    multipole_moments
        Monopole moment of the Schwarzschild metric, given by the product of
        the gravitational constant G and the gravitating object's mass m.

    Returns
    -------
        Schwarzschild metric line element at the given coordinates.
    """

    g00_factor = 1 - 2 * multipole_moments[0] / (c ** 2 * r)

    metric = sympy.Matrix([
        [- g00_factor, 0, 0, 0],
        [0, 1 / g00_factor, 0, 0],
        [0, 0, r ** 2, 0],
        [0, 0, 0, r ** 2 * sympy.sin(theta) ** 2]
    ])

    return metric


metric_line_elements: dict[str, Callable] = {
    'pN': post_newton,
    'Schwarzschild': schwarzschild,
}
