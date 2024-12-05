"""
This module contains tests for the post_newton function.
"""

from unittest import TestCase
import tomli
import sympy
from scipy.constants import c
from greopy.metric_config_sympy import (
    post_newton,
    gravitational_potential,
    centrifugal_potential
)


class TestPostNewton(TestCase):
    def test_post_newton(self) -> None:

        radius_coordinate, theta_coordinate = sympy.symbols(
                'radius_coordinate theta_coordinate'
            )

        with open('tests/example_configs/example_config_pN.toml',
                  mode='rb') as fp:
            config = tomli.load(fp)

        multipole_moments = config['Metric']['params']['multipole_moments']
        radius_reference = config['Metric']['params']['radius_reference']
        gravity_constant = config['Metric']['params']['gravity_constant']
        period_rotation = config['Metric']['params']['period_rotation']

        metric_00 = -(
            1
            + 2 * (
                gravitational_potential(
                    multipole_moments,
                    radius_reference,
                    gravity_constant
                )
                + centrifugal_potential(period_rotation)
            ) / c ** 2
            + 2 * (
                gravitational_potential(
                    multipole_moments,
                    radius_reference,
                    gravity_constant
                )
                + centrifugal_potential(period_rotation)
            ) ** 2 / c ** 4
        )

        metric_ij = (
            1 - 2 * gravitational_potential(
                multipole_moments,
                radius_reference,
                gravity_constant
            ) / c ** 2
        )

        metric = sympy.Matrix([
            [metric_00, 0, 0, 0],
            [0, metric_ij, 0, 0],
            [0, 0, metric_ij * radius_coordinate ** 2, 0],
            [
                0,
                0,
                0,
                (metric_ij *
                 radius_coordinate ** 2 * sympy.sin(theta_coordinate) ** 2)
            ],
        ])

        metric.equals(post_newton(**config['Metric']['params']))
        metric.equals(post_newton(multipole_moments,
                                  radius_reference,
                                  gravity_constant,
                                  period_rotation))

        post_newton(**config['Metric']['params']).equals(
            post_newton(multipole_moments,
                        radius_reference,
                        gravity_constant,
                        period_rotation)
        )
