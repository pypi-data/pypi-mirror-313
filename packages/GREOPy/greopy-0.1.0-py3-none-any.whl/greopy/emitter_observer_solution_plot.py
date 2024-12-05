"""
This module visualises the results of the emitter-observer problem.
"""

from collections.abc import Generator
import inspect
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as mpl_axes3d
from .common import cartesian_coordinates, VectorNd


def plot_sphere(radius_sphere: np.float64, axis: mpl_axes3d.Axes3D) -> None:
    """Plot a sphere of radius_sphere.

    Here, the step length of mgrid is the complex number 30j, meaning the
    final point b of mgrid[a:b:step] is part of the grid. See the [mgrid]_
    documentation for more info.

    Parameters
    ----------
    radius_sphere
        Spherical coordinate radius of the sphere to be plotted.
    axis
        Determines the figure to be plotted in.

    Returns
    -------
    None

    References
    ----------
    .. [mgrid] https://numpy.org/doc/stable/reference/generated/numpy.mgrid.html
    """

    theta, phi = np.mgrid[0:2 * np.pi:30j,  # type: ignore[misc]
                          0:2 * np.pi:30j]  # type: ignore[misc]
    vectors = cartesian_coordinates(radius_sphere,
                                    theta,
                                    phi)

    vectors_x, vectors_y, vectors_z = vectors[0], vectors[1], vectors[2]

    axis.plot_wireframe(vectors_x,
                        vectors_y,
                        vectors_z,
                        color='gray',
                        alpha=0.2)


def plot_curve_dataframe(curve: pd.DataFrame, axis: mpl_axes3d.Axes3D) -> None:
    """Plot curve from a DataFrame.

    Parameters
    ----------
    curve
        Curve coordinates and tangent vector at each event.
    axis
        Determines the figure to be plotted in.

    Returns
    -------
    None
    """

    vectors = cartesian_coordinates(
        curve.loc[:, 'r_coordinate'].to_numpy(),
        curve.loc[:, 'theta_coordinate'].to_numpy(),
        curve.loc[:, 'phi_coordinate'].to_numpy(),
    )

    vectors_x, vectors_y, vectors_z = vectors[0], vectors[1], vectors[2]

    axis.plot(vectors_x, vectors_y, vectors_z)


def plot_curve_arrays(
        spatial_coordinates: tuple[
            VectorNd,
            VectorNd,
            VectorNd,
        ],
        axis: mpl_axes3d.Axes3D
) -> None:
    """Plot curve given by spherical coordinate arrays.

    Parameters
    ----------
    spatial_coordinates
        Spherical coordinate arrays describing the curve.
    axis
        Determines the figure to be plotted in.

    Returns
    -------
    None
    """

    vectors = cartesian_coordinates(
        spatial_coordinates[0],
        spatial_coordinates[1],
        spatial_coordinates[2]
    )

    vectors_x, vectors_y, vectors_z = vectors[0], vectors[1], vectors[2]

    axis.plot(vectors_x, vectors_y, vectors_z)


def eop_plot(
        curve_1: pd.DataFrame,
        curve_2: pd.DataFrame,
        light_rays: list | Generator,
) -> None:
    """Plot the emitter-observer problem setup with light ray solutions.

    Parameters
    ----------
    curve_1
        Curve 1 coordinates and tangent vector at each event.
    curve_2
        Curve 2 coordinates and tangent vector at each event.
    light_rays
        Indexed light ray curves' coordinates and tangent vectors.

    Returns
    -------
    None
    """

    if not inspect.isgenerator(light_rays):
        light_rays = [light_ray[1] for light_ray in light_rays]

    ax_1 = plt.figure().add_subplot(projection='3d')
    # ax_1.set_box_aspect((1, 1, 1))
    plot_sphere(np.float64(6371e3), ax_1)
    for i in [curve_1, curve_2]:
        plot_curve_dataframe(i, ax_1)

    for light_ray in light_rays:
        xi_values = (
            light_ray.loc[:, 'r_coordinate'].to_numpy(),
            light_ray.loc[:, 'theta_coordinate'].to_numpy(),
            light_ray.loc[:, 'phi_coordinate'].to_numpy(),
        )
        plot_curve_arrays(xi_values, ax_1)
