"""
This module contains tests for the load_dataset function.
"""

from unittest import TestCase
from greopy.common import load_dataset


class TestLoadDataset(TestCase):
    def test_load_dataset(self) -> None:

        test_curve = load_dataset(
            'tests/example_curves/example_curve_Schwarzschild.h5',
            step_size=2,
        )

        for curve in test_curve:
            self.assertAlmostEqual(curve.loc[808, 'phi_coordinate'],
                                   8.962814814814815)  # taken from DataFrame

        light_rays = load_dataset(
            'tests/example_curves/example_light_rays_Schwarzschild_moving.h5',
            step_size=2,
        )

        comparison_array = [8.79376274195002e-16,
                            0.6846935362880898,
                            1.5597316362930298,
                            2.381253738603591,
                            3.1585327730608865,
                            3.945454813975378,
                            4.766071894797393,
                            5.650509960576619,
                            6.564937678096999,
                            7.468602068539584,
                            8.310523346428546,
                            9.105511421011462]

        for light_ray, comp in zip(light_rays, comparison_array):
            self.assertAlmostEqual(light_ray.loc[4, 'phi_coordinate'], comp)
