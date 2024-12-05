"""
This module contains tests for the scalar_product function.
"""

from unittest import TestCase
import numpy as np
from greopy.common import scalar_product


def metric_example(a, b, c, d):
    example = np.array([[a, 0, 0, 0],
                       [0, b, 0, 0],
                       [0, 0, c, 0],
                       [0, 0, 0, d]])

    return example


class TestScalarProduct(TestCase):
    def test_scalar_product(self) -> None:

        event_example = np.array([-1, 1, 1, 1])
        vector_1_example = np.array([1, 1, 1, 1])
        vector_2_example = np.array([1, 1, 1, 1])
        product_result = scalar_product(metric_example(*event_example),
                                        vector_1_example,
                                        vector_2_example)
        self.assertAlmostEqual(product_result, 2)

        event_example_2 = np.array([0, 0, 0, 0])
        vector_1_example_2 = np.array([0, 0, 0, 0])
        vector_2_example_2 = np.array([0, 0, 0, 0])
        product_result_2 = scalar_product(metric_example(*event_example_2),
                                          vector_1_example_2,
                                          vector_2_example_2)
        self.assertAlmostEqual(product_result_2, 0)

        event_example_3 = np.array([10, 0, 3, 0])
        vector_1_example_3 = np.array([1, 0, 5, 0])
        vector_2_example_3 = np.array([0, 2, 6, 0])
        product_result_3 = scalar_product(metric_example(*event_example_3),
                                          vector_1_example_3,
                                          vector_2_example_3)
        self.assertAlmostEqual(product_result_3, 90)
