"""
This module contains tests for the curve_dataframe function.
"""

import numpy as np
from unittest import TestCase
from greopy.common import curve_dataframe


class TestCurveDataframe(TestCase):
    def test_curve_dataframe(self) -> None:

        example_array_length = 5
        test_1_array_1 = np.linspace(1, 2, example_array_length)
        dphidtau_control_array = np.linspace(1, 12, example_array_length)
        test_1_array_2 = np.array([
            np.linspace(1, 5, example_array_length),
            np.linspace(1, 6, example_array_length),
            np.linspace(1, 7, example_array_length),
            np.linspace(1, 8, example_array_length),
            np.linspace(1, 9, example_array_length),
            np.linspace(1, 10, example_array_length),
            np.linspace(1, 11, example_array_length),
            dphidtau_control_array,
        ])
        result_dataframe = curve_dataframe((test_1_array_1, test_1_array_2))
        self.assertAlmostEqual(result_dataframe.loc[3, 'dphidtau'],
                               dphidtau_control_array[3])



