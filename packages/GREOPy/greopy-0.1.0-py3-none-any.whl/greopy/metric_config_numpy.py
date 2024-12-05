"""
This module calculates symbolic expressions for the metric, its inverse and its
derivatives w.r.t. coordinates and translates expressions into NumPy functions.
"""

import sympy
from sympy import MutableDenseMatrix
from sympy.core.expr import Expr as expression
from .metric_config_sympy import (
    x0,
    r,
    theta,
    phi,
)
from .common import MetricFunction, MetricDerivativesFunction


def metric_sympy_differentiate(
        metric_parametrised: MutableDenseMatrix,
) -> tuple[expression, expression, expression, expression]:
    """Differentiate metric line element w.r.t. given coordinates.

    Parameters
    ----------
    metric_at_event
        Metric line element as a function of spacetime coordinates.

    Returns
    -------
        List of metric line element derivatives w.r.t. spacetime coordinates.
    """

    metric_differentiated = (
        metric_parametrised.diff(x0),
        metric_parametrised.diff(r),
        metric_parametrised.diff(theta),
        metric_parametrised.diff(phi),
    )

    return metric_differentiated


def metric_lambdified(
        metric_parametrised: MutableDenseMatrix,
) -> tuple[MetricFunction,
           MetricDerivativesFunction,
           MetricFunction]:
    """Translate SymPy expressions into NumPy functions.

    Parameters
    ----------
    metric_at_event
        Metric line element as a function of spacetime coordinates.

    Returns
    -------
        Metric, its derivates w.r.t. given coordinates and its inverse as
        functions of event coordinates.
    """

    g_np = sympy.lambdify(
        [x0, r, theta, phi],
        metric_parametrised
    )
    g_diff_np = sympy.lambdify(
        [x0, r, theta, phi],
        metric_sympy_differentiate(metric_parametrised)
    )
    g_inv_np = sympy.lambdify(
        [x0, r, theta, phi],
        metric_parametrised ** -1
    )

    return g_np, g_diff_np, g_inv_np
