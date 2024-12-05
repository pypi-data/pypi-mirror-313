"""
This module contains tests for the gravitational_potential function.
"""

from unittest import TestCase
import tomli
import sympy
from sympy import simplify
from greopy.metric_config_sympy import gravitational_potential


class TestGravitationalPotential(TestCase):
    def test_gravitational_potential(self) -> None:

        r, theta = sympy.symbols('r theta')

        with open('tests/example_configs/example_config_pN.toml',
                  mode='rb') as fp:
            config = tomli.load(fp)

        multipole_moments = config['Metric']['params']['multipole_moments']
        radius_reference = config['Metric']['params']['radius_reference']
        gravity_constant = config['Metric']['params']['gravity_constant']

        potential_from_func = gravitational_potential(multipole_moments,
                                                      radius_reference,
                                                      gravity_constant)

        potential_analytical = - gravity_constant / r * (
            multipole_moments[0]
            + (multipole_moments[1] * radius_reference / r
               * sympy.sin(theta))
        )

        potential_difference = simplify(potential_from_func
                                        - potential_analytical)

        self.assertAlmostEqual(potential_difference, 0)
