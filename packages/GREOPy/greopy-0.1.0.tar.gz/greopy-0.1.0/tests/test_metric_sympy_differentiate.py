"""
This module contains tests for the metric_sympy_differentiate function.
"""

from unittest import TestCase
import tomli
import sympy
from greopy.metric_config_numpy import metric_sympy_differentiate
from greopy.metric_config_sympy import metric_line_elements


class TestMetricSympyDifferentiate(TestCase):
    def test_metric_sympy_differentiate(self) -> None:

        x0, r, theta, phi = sympy.symbols('x0 radius theta phi')

        with open('tests/example_configs/example_config_pN.toml',
                  mode='rb') as fp:
            config = tomli.load(fp)

        metric_function = metric_line_elements[config['Metric']['name']]
        metric_params = config['Metric']['params']
        metric_parametrised = metric_function(**metric_params)

        diff_0_kwargs = metric_function(
            **config['Metric']['params']
        ).diff(x0)
        diff_0 = metric_parametrised.diff(x0)

        diff_1_kwargs = metric_function(
            **config['Metric']['params']
        ).diff(r)
        diff_1 = metric_parametrised.diff(r)

        diff_2_kwargs = metric_function(
            **config['Metric']['params']
        ).diff(theta)
        diff_2 = metric_parametrised.diff(theta)

        diff_3_kwargs = metric_function(
            **config['Metric']['params']
        ).diff(phi)
        diff_3 = metric_parametrised.diff(phi)

        metric_diff = metric_sympy_differentiate(metric_parametrised)

        diff_0_kwargs.equals(metric_diff[0])
        diff_1_kwargs.equals(metric_diff[1])
        diff_2_kwargs.equals(metric_diff[2])
        diff_3_kwargs.equals(metric_diff[3])
        diff_0.equals(metric_diff[0])
        diff_1.equals(metric_diff[1])
        diff_2.equals(metric_diff[2])
        diff_3.equals(metric_diff[3])
        diff_0_kwargs.equals(diff_0)
        diff_1_kwargs.equals(diff_1)
        diff_2_kwargs.equals(diff_2)
        diff_3_kwargs.equals(diff_3)
