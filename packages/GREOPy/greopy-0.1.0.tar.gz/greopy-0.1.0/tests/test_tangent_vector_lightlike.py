"""
This module contains tests for the tangent_vector_lightlike function.
"""

import numpy as np
from scipy.constants import c
from unittest import TestCase
from greopy.emitter_observer_problem import tangent_vector_lightlike


class TestTangentVectorLightlike(TestCase):
    def test_tangent_vector_lightlike(self) -> None:

        normalisation_factor = 1
        tetrad_vectors_1 = (np.array([0, 1, 2, 3]),
                            np.array([1, 2, 3, 4]),
                            np.array([10, 20, 30, 40]),
                            np.array([0, 2, 3, 4]))

        initial_angles_1 = np.pi / 2, np.pi / 2

        result_analytical_1 = np.array([10, 21, 32, 43])
        result_1 = tangent_vector_lightlike(normalisation_factor,
                                            tetrad_vectors_1,
                                            initial_angles_1,
                                            signal_frequency=c)

        [self.assertAlmostEqual(result_1[i], result_analytical_1[i])
            for i in range(4)]

        initial_angles_2 = 0, 0

        result_analytical_2 = np.array([0, 3, 5, 7])
        result_2 = tangent_vector_lightlike(normalisation_factor,
                                            tetrad_vectors_1,
                                            initial_angles_2,
                                            signal_frequency=c)

        [self.assertAlmostEqual(result_2[i], result_analytical_2[i])
            for i in range(4)]

        initial_angles_3 = np.pi / 2, 0

        result_analytical_3 = np.array([1, 3, 5, 7])
        result_3 = tangent_vector_lightlike(normalisation_factor,
                                            tetrad_vectors_1,
                                            initial_angles_3,
                                            signal_frequency=c)

        [self.assertAlmostEqual(result_3[i], result_analytical_3[i])
            for i in range(4)]
