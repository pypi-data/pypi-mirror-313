"""Orbit calculation based on parameters defined in setup_params and params.

Code by Jan Patrick Hackstein
"""

import pandas as pd
import numpy as np
from scipy.integrate import solve_ivp
from .config import Config
from .metric_config_numpy import metric_lambdified
from .metric_config_sympy import metric_line_elements
from .common import (
    curve_dataframe,
    VectorNd,
    MetricFunction,
    MetricDerivativesFunction,
)


def gamma(
        metric_derivatives: MetricDerivativesFunction,
        metric_inverse: MetricFunction,
        event_coordinates: VectorNd,
) -> VectorNd:
    """Calculate Christoffel symbols.

    Parameters
    ----------
    metric_derivatives
        List of metric line element derivatives w.r.t. spacetime coordinates.
    metric_inverse
        Inverted metric line element.
    event_coordinates
        Event's spacetime coordinates.

    Returns
    -------
    Christoffel symbols
        List of Christoffel symbols for a given event.
    """
    x0, r, theta, phi = event_coordinates

    g_d = metric_derivatives(x0, r, theta, phi)
    g_i = metric_inverse(x0, r, theta, phi)
    gamma_ijk = 1 / 2 * (
        np.einsum('il,jkl->ijk', g_i, g_d)
        + np.einsum('il,jkl->ikj', g_i, g_d)
        - np.einsum('il,ljk->ijk', g_i, g_d)
    )

    return gamma_ijk


def geodesic_equation(
        _affine_parameter: float,
        event_velocity_array: VectorNd,
        metric_derivatives: MetricDerivativesFunction,
        metric_inverse: MetricFunction,
) -> VectorNd:
    """Calculate left-hand side of geodesic equation.

    Parameters
    ----------
    _affine_parameter
        Parameter elapsing along solution curve.
    event_velocity_array
        Event's spacetime coordinates and given four-velocity tangent vector.
    metric_derivatives
        List of metric line element derivatives w.r.t. spacetime coordinates.
    metric_inverse
        Inverted metric line element.

    Returns
    -------
    geodesic equation
        Components of geodesic equation's left-hand side.
    """

    velocity_acceleration_array = np.concatenate((
        event_velocity_array[4:8],
        - np.einsum(
            'ijk,j,k->i',
            gamma(metric_derivatives,
                  metric_inverse,
                  event_velocity_array[0:4]),
            event_velocity_array[4:8],
            event_velocity_array[4:8],
        ),
    ))

    return velocity_acceleration_array


def geodesic_calc(
        config: Config,
        initial_conditions: tuple,
        step_numbers: tuple[int, int] | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Calculate timelike geodesics (curves) defined via initial conditions.

    Parameters
    ----------
    config
        Configuration dictionary containing metric information.
    initial_conditions
        Initial spacetime coordinates and four-velocity tangent vector.
    step_numbers
        Number of steps along the curve.

    Returns
    -------
    curve solutions
        DataFrames with curve solutions.
    """

    if step_numbers is None:
        step_numbers = (600, 600)

    metric_function = metric_line_elements[config['Metric']['name']]
    metric_params = config['Metric']['params']
    metric_parametrised = metric_function(**metric_params)

    _, metric_diff_np, metric_inv_np = metric_lambdified(metric_parametrised)

    proper_time_interval_curve_1 = [
        config['Curve_1']['proper_times']['time_initial'],
        config['Curve_1']['proper_times']['time_final'],
    ]
    proper_time_interval_curve_2 = [
        config['Curve_2']['proper_times']['time_initial'],
        config['Curve_2']['proper_times']['time_final'],
    ]

    curve_1_solution = solve_ivp(
        geodesic_equation,
        proper_time_interval_curve_1,
        (*initial_conditions[0], *initial_conditions[1]),
        args=(metric_diff_np, metric_inv_np),
        max_step=(proper_time_interval_curve_1[1]
                  - proper_time_interval_curve_1[0]) / step_numbers[0],
    )

    curve_2_solution = solve_ivp(
        geodesic_equation,
        proper_time_interval_curve_2,
        (*initial_conditions[2], *initial_conditions[3]),
        args=(metric_diff_np, metric_inv_np),
        max_step=(proper_time_interval_curve_2[1]
                  - proper_time_interval_curve_2[0]) / step_numbers[1],
    )

    curve_1_data = curve_dataframe((curve_1_solution.t, curve_1_solution.y))
    curve_2_data = curve_dataframe((curve_2_solution.t, curve_2_solution.y))

    return curve_1_data, curve_2_data
