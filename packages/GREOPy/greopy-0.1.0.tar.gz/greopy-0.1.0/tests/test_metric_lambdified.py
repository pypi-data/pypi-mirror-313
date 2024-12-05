"""
This module contains tests for the metric_sympy_lambdified function.
"""

from unittest import TestCase
import tomli
import sympy
from numpy.testing import assert_array_equal
from greopy.metric_config_numpy import (
    metric_lambdified,
    metric_sympy_differentiate,
)
from greopy.metric_config_sympy import metric_line_elements


class TestMetricSympyLambdified(TestCase):
    def test_metric_sympy_lambdified(self) -> None:

        x0, r, theta, phi = sympy.symbols('x0 r theta phi')

        with open('tests/example_configs/example_config_pN.toml',
                  mode='rb') as fp:
            config = tomli.load(fp)

        metric_function = metric_line_elements[config['Metric']['name']]
        metric_params = config['Metric']['params']
        metric_parametrised = metric_function(**metric_params)

        lambdified_functions = metric_lambdified(metric_parametrised)

        line_element_lambdified = sympy.lambdify(
            [x0, r, theta, phi],
            metric_parametrised
        )
        metric_derivatives_lambdified = sympy.lambdify(
            [x0, r, theta, phi],
            metric_sympy_differentiate(metric_parametrised)
        )
        metric_inverse_lambdified = sympy.lambdify(
            [x0, r, theta, phi],
            metric_parametrised ** -1
        )

        x0_eval, radius_eval, theta_eval, phi_eval = 0, 1, 2, 3

        line_element_evaluated = line_element_lambdified(
            x0_eval,
            radius_eval,
            theta_eval,
            phi_eval,
        )
        line_element_evaluated_func = lambdified_functions[0](
            x0_eval,
            radius_eval,
            theta_eval,
            phi_eval,
        )
        assert_array_equal(line_element_evaluated, line_element_evaluated_func)

        metric_derivatives_evaluated = metric_derivatives_lambdified(
            x0_eval,
            radius_eval,
            theta_eval,
            phi_eval,
        )
        metric_derivatives_evaluated_func = lambdified_functions[1](
            x0_eval,
            radius_eval,
            theta_eval,
            phi_eval,
        )
        assert_array_equal(metric_derivatives_evaluated,
                           metric_derivatives_evaluated_func)

        metric_inverse_evaluated = metric_inverse_lambdified(
            x0_eval,
            radius_eval,
            theta_eval,
            phi_eval,
        )
        metric_inverse_evaluated_func = lambdified_functions[2](
            x0_eval,
            radius_eval,
            theta_eval,
            phi_eval,
        )
        assert_array_equal(metric_inverse_evaluated,
                           metric_inverse_evaluated_func)
