"""
This module contains tests for the centrifugal_potential function.
"""

from unittest import TestCase
import tomli
import sympy
from sympy import simplify
import numpy as np
from greopy.metric_config_sympy import centrifugal_potential


class TestCentrifugalPotential(TestCase):
    def test_centrifugal_potential(self) -> None:

        r, theta = sympy.symbols('r theta')

        with open('tests/example_configs/example_config_pN.toml',
                  mode='rb') as fp:
            config = tomli.load(fp)

        period_rotation = config['Metric']['params']['period_rotation']

        potential_from_func = centrifugal_potential(period_rotation)

        potential_analytical = - (
            (2 * np.pi / period_rotation) ** 2 * r ** 2 * sympy.sin(theta) ** 2
        ) / 2
        potential_difference = simplify(potential_from_func
                                        - potential_analytical)

        self.assertAlmostEqual(potential_difference, 0)
