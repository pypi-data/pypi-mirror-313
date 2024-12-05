"""
This module contains tests for the geodesic_equation function.
"""

import numpy as np
from unittest import TestCase
from unittest.mock import Mock
from greopy.orbit_calc import geodesic_equation


class TestGeodesicEquation(TestCase):
    def test_geodesic_equation(self) -> None:

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
        event_coords = np.array([0, 0, 2, 2, 4, 5, 6, 7])
        geodesic_eq_rhs = geodesic_equation(0,
                                            event_coords,
                                            mockfunc,
                                            mockfunc_2)

        results_analytical = np.array([*event_coords[4:8], 0, 0, -8.75, -12])

        for i in range(8):
            self.assertAlmostEqual(results_analytical[i], geodesic_eq_rhs[i])

