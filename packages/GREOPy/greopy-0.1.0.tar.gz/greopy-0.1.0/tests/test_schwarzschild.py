"""
This module contains tests for the schwarzschild function.
"""

from unittest import TestCase
import tomli
import sympy
from scipy.constants import c
from greopy.metric_config_sympy import schwarzschild


class TestSchwarzschild(TestCase):
    def test_schwarzschild(self) -> None:

        radius_coordinate, theta_coordinate = sympy.symbols(
                'radius_coordinate theta_coordinate'
            )

        with open('tests/example_configs/example_config_schwarzschild.toml',
                  mode='rb') as fp:
            config = tomli.load(fp)

        multipole_moments = config['Metric']['params']['multipole_moments']

        metric = sympy.Matrix([
            [-(1 - 2 * multipole_moments[0] / (c ** 2 * radius_coordinate)),
             0,
             0,
             0],
            [0,
             1 / (1 - 2 * multipole_moments[0] / (c ** 2 * radius_coordinate)),
             0,
             0],
            [0, 0, radius_coordinate ** 2, 0],
            [0,
             0,
             0,
             radius_coordinate ** 2 * sympy.sin(theta_coordinate) ** 2]
        ])

        metric.equals(schwarzschild(**config['Metric']['params']))
        metric.equals(schwarzschild(multipole_moments))
        schwarzschild(**config['Metric']['params']).equals(
            schwarzschild(multipole_moments))
