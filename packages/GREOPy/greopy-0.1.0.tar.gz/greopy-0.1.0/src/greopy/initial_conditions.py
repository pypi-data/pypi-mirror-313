"""
This module calculates the curves' initial temporal four-velocity component
from a given set of spatial velocity components.

Code by Jan Patrick Hackstein
"""

import numpy as np
from scipy.optimize import root_scalar
from scipy.constants import c
from .config import Config
from .metric_config_numpy import metric_lambdified
from .metric_config_sympy import metric_line_elements
from .common import scalar_product, VectorNd


def x0_velocity_calc(
        metric_evaluated: VectorNd,
        spatial_velocity: VectorNd,
) -> float:
    """Calculate x0-component of four-velocity given a timelike normalisation.

    x0 = c * t, where t is the coordinate time and c the speed of light.

    Parameters
    ----------
    metric_function
        Metric line element as a function of spacetime coordinates.
    spatial_velocity
        Spatial velocity tangent vector at given event.

    Returns
    -------
        x0-component of desired four-velocity tangent vector.
    """

    # the "bracket" interval is estimated from the normalisation condition:
    lower_boundary_factor = 0.9
    upper_boundary_factor = 2.5

    x0_velocity_result = root_scalar(
        lambda x0_velocity: scalar_product(
            metric_evaluated,
            np.array([x0_velocity, *spatial_velocity]),
            np.array([x0_velocity, *spatial_velocity]),
        ) + c ** 2,
        method='brentq',
        bracket=[lower_boundary_factor * c / np.sqrt(-metric_evaluated[0, 0]),
                 upper_boundary_factor * c / np.sqrt(-metric_evaluated[0, 0])]
    )

    return x0_velocity_result.root


def initial_conditions_calc(
        config: Config,
) -> tuple[VectorNd, VectorNd, VectorNd, VectorNd]:
    """Return initial conditions for timelike curves.

    Parameters
    ----------
    config
        Configuration dictionary with event and spatial velocity information.

    Returns
    -------
    initial conditions
        Initial events and four-velocities of given curves.
    """

    initial_event_coordinates_curve_1 = np.array([
        *config['Curve_1']['initial_event'].values()
    ])
    initial_event_coordinates_curve_2 = np.array([
        *config['Curve_2']['initial_event'].values()
    ])

    initial_spatial_velocity_curve_1 = np.array([
        *config['Curve_1']['initial_velocity'].values()
    ])
    initial_spatial_velocity_curve_2 = np.array([
        *config['Curve_2']['initial_velocity'].values()
    ])

    metric_function = metric_line_elements[config['Metric']['name']]
    metric_params = config['Metric']['params']
    metric_parametrised = metric_function(**metric_params)

    metric_np, _, _ = metric_lambdified(metric_parametrised)

    metric_evaluated_1 = metric_np(*initial_event_coordinates_curve_1)
    metric_evaluated_2 = metric_np(*initial_event_coordinates_curve_2)

    initial_x0_velocity_curve_1, initial_x0_velocity_curve_2 = (
        x0_velocity_calc(metric_evaluated_1,
                         initial_spatial_velocity_curve_1),
        x0_velocity_calc(metric_evaluated_2,
                         initial_spatial_velocity_curve_2),
    )

    initial_velocity_curve_1 = np.array([
        initial_x0_velocity_curve_1,
        *initial_spatial_velocity_curve_1,
    ])

    initial_velocity_curve_2 = np.array([
        initial_x0_velocity_curve_2,
        *initial_spatial_velocity_curve_2,
    ])

    return (initial_event_coordinates_curve_1,
            initial_velocity_curve_1,
            initial_event_coordinates_curve_2,
            initial_velocity_curve_2)
