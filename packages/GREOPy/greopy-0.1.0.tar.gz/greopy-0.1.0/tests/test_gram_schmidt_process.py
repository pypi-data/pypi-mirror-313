"""
This module contains tests for the gram_schmidt_process function.
"""

from unittest import TestCase
import numpy as np
from scipy.constants import c
from greopy.common import gram_schmidt_process, load_dataset
from greopy.metric_config_numpy import metric_lambdified
from greopy.metric_config_sympy import metric_line_elements


class TestGramSchmidtProcess(TestCase):
    def test_gram_schmidt_process(self) -> None:

        curve_data = load_dataset(
            "tests/example_curves/example_curve_Schwarzschild.h5"
        )
        for curve in curve_data:
            orbit_1 = curve

        minkowski_metric = np.array([
            [-1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
        initial_spatial_vectors = (
            np.array([0, 1, 0, 0]),
            np.array([0, 0, 1, 0]),
            np.array([0, 0, 0, 1])
        )

        metric_function = metric_line_elements['Schwarzschild']
        metric_params = {"multipole_moments": [3.9860044150e14]}
        metric_parametrised = metric_function(**metric_params)

        metric_np, _, _ = metric_lambdified(metric_parametrised)

        # Test 1
        x_1 = np.array(orbit_1.iloc[5, 1:5])  # random place
        u_1 = np.array([c / np.sqrt(-metric_np(*x_1)[0, 0]), 0, 0, 0])
        initial_vectors_1 = [i for j in ((u_1,), initial_spatial_vectors)
                             for i in j]

        metric_evaluated = metric_np(*x_1)

        e_vectors_1 = gram_schmidt_process(initial_vectors_1, metric_evaluated)

        [self.assertAlmostEqual(
            np.einsum(
                'ij,i,j->',
                metric_evaluated,
                e_vectors_1[i],
                e_vectors_1[j]
            ),
            minkowski_metric[i][j]
        ) for i in range(0, 4) for j in range(0, 4)]

        # Tests for each orbit step
        for k in range(0, len(orbit_1)):
            x_k = np.array(orbit_1.iloc[k, 1:5])
            u_k = np.array(orbit_1.iloc[k, 5:9])
            initial_vectors_k = [i for j in ((u_k,), initial_spatial_vectors)
                                 for i in j]

            metric_evaluated = metric_np(*x_k)

            e_vectors_k = gram_schmidt_process(initial_vectors_k,
                                               metric_evaluated)

            [self.assertAlmostEqual(
                np.einsum(
                    'ij,i,j->',
                    metric_evaluated,
                    e_vectors_k[i],
                    e_vectors_k[j]
                ),
                minkowski_metric[i][j]
            ) for i in range(0, 4) for j in range(0, 4)]
