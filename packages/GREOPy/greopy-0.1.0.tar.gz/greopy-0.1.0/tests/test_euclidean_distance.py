"""
This module contains tests for the euclidean_distance function.
"""

import numpy as np
from unittest import TestCase
from greopy.emitter_observer_problem import euclidean_distance


class TestEuclideanDistance(TestCase):
    def test_euclidean_distance(self) -> None:

        event_1_coordinates_1 = (10, np.pi / 2, np.pi / 4)
        event_2_coordinates_1 = np.array([10, np.pi / 2, np.pi / 4])

        self.assertAlmostEqual(euclidean_distance(event_1_coordinates_1,
                                                  event_2_coordinates_1),
                               0)

        event_1_coordinates_1 = (5, np.pi / 4, np.pi / 2)
        event_2_coordinates_1 = np.array([20, np.pi / 2, - np.pi / 2])

        self.assertAlmostEqual(euclidean_distance(event_1_coordinates_1,
                                                  event_2_coordinates_1),
                               23.799608321090275)
