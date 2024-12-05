"""
This module contains tests for the curve_dataframe function.
"""

import numpy as np
from itertools import product
from unittest import TestCase
from unittest.mock import Mock
from greopy.orbit_calc import gamma


class TestGamma(TestCase):
    def test_gamma(self) -> None:

        def diff_mock(a, b, c, d):

            return np.array([[a, 0, 0, 0],
                             [0, b, 0, 0],
                             [0, 0, c, 0],
                             [0, 0, 0, d]])

        mockfunc = Mock()
        mockfunc.return_value = [diff_mock(0, 0, 0, 0),
                                 diff_mock(0, 0, 0, 0),
                                 diff_mock(0, 0, 0, 1),
                                 diff_mock(0, 0, 1, 0)]

        mockfunc_2 = Mock()
        mockfunc_2.return_value = diff_mock(-1, 1, 1/2, 1/2)
        event_coords = np.array([0, 0, 2, 2])
        gamma_result = gamma(mockfunc, mockfunc_2, event_coords)
        results_analytical = [np.zeros((4, 4)),
                              np.zeros((4, 4)),
                              np.array([[0, 0, 0, 0],
                                       [0, 0, 0, 0],
                                       [0, 0, 0, 1 / 4],
                                       [0, 0, 1 / 4, - 1 / 4]]),
                              np.array([[0, 0, 0, 0],
                                       [0, 0, 0, 0],
                                       [0, 0, - 1 / 4, 1 / 4],
                                       [0, 0, 1 / 4, 0]])]
        for i, j, k in product(range(4), repeat=3):
            self.assertAlmostEqual(results_analytical[i][j][k],
                                   gamma_result[i][j][k])

