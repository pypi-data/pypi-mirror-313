"""
This module contains tests for the cartesian_coordinates function.
"""

from unittest import TestCase
import numpy as np
from greopy.common import cartesian_coordinates


class TestCartesianCoordinates(TestCase):
    def test_cartesian_coordinates(self) -> None:

        example_1 = cartesian_coordinates(1, np.pi / 2, 0)
        result_analytical_1 = (1, 0, 0)
        [self.assertAlmostEqual(example_1[i],
                                result_analytical_1[i]) for i in range(3)]

        example_2 = cartesian_coordinates(1, np.pi / 2, np.pi / 2)
        result_analytical_2 = (0, 1, 0)
        [self.assertAlmostEqual(example_2[i],
                                result_analytical_2[i]) for i in range(3)]

        example_3 = cartesian_coordinates(1, np.pi, np.pi)
        result_analytical_3 = (0, 0, -1)
        [self.assertAlmostEqual(example_3[i],
                                result_analytical_3[i]) for i in range(3)]

        example_4_r = np.array([1, 2, 3])
        example_4_theta = np.array([np.pi / 2, 3 / 2 * np.pi, 0])
        example_4_phi = np.array([3 / 2 * np.pi, 0, np.pi])

        example_4 = cartesian_coordinates(example_4_r,
                                          example_4_theta,
                                          example_4_phi)
        result_analytical_4 = np.array([[0, -2, 0], [-1, 0, 0], [0, 0, 3]])
        [self.assertAlmostEqual(example_4[i][j],
                                result_analytical_4[i][j])
            for i in range(3)
            for j in range(3)]
