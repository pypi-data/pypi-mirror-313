"""
This module contains tests for the data_interpolation function.
"""

from unittest import TestCase
from scipy import interpolate
import numpy as np
from greopy.common import data_interpolation, load_dataset


class TestDataInterpolation(TestCase):
    def test_data_interpolation(self) -> None:

        curve_data = load_dataset(
            'tests/example_curves/example_curve_Schwarzschild.h5'
        )

        for curve in curve_data:
            test_curve = curve

        data_interpolated_1_func = data_interpolation(test_curve)

        data_interpolated_1 = interpolate.interp1d(
            test_curve.loc[:, 'x0_coordinate'].to_numpy(),
            test_curve.loc[:, 'r_coordinate':'dphidtau'].to_numpy(),
            axis=0,
        )
        array_length_1 = 7
        x0_value_examples = test_curve.loc[:,
                                           'x0_coordinate'].to_numpy()[0:-1:10]
        [self.assertAlmostEqual(
            data_interpolated_1(i)[j],
            data_interpolated_1_func(i)[j])
            for i in x0_value_examples
            for j in range(array_length_1)]

