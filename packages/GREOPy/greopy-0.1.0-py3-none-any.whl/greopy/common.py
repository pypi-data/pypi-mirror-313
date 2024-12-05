"""
This module contains functions used in multiple places throughout the package.
"""

from typing import Any, overload
from collections.abc import Generator, Callable
import numpy as np
import pandas as pd
from scipy import interpolate
from scipy.constants import c


VectorNd = np.ndarray[Any, np.dtype[np.float64]]
Tuple4Nd = tuple[VectorNd, VectorNd, VectorNd, VectorNd]

Tuple2 = tuple[float, float]
NpTuple2 = tuple[np.float64, np.float64]
Tuple3 = tuple[float, float, float]
Tuple4 = tuple[float, float, float, float]

MetricFunction = Callable[[float, float, float, float], VectorNd]
MetricDerivativesFunction = Callable[[float, float, float, float], Tuple4Nd]


class ODESolution:
    """Contain domain t and codomain y of differential equation solution."""

    def __init__(self, t: VectorNd, y: VectorNd):
        self.t: VectorNd = t
        self.y: VectorNd = y


def scalar_product(
        metric_evaluated: VectorNd,
        vector_1: VectorNd,
        vector_2: VectorNd,
) -> float:
    """Calculate scalar product between two vectors at given event.

    Parameters
    ----------
    metric_evaluated
        Metric line element evaluated at event's spacetime coordinates.
    vector_1
        First vector.
    vector_2
        Second vector.

    Returns
    -------
        scalar product between given vectors at the given event coorindates.
    """

    scalar_product_float = np.einsum(
        'ij,i,j->',
        metric_evaluated,
        vector_1,
        vector_2,
    )

    return scalar_product_float


def gram_schmidt_process(
        initial_vectors: Tuple4Nd,
        metric_evaluated: VectorNd,
) -> Tuple4Nd:
    """Calculate a tetrad at a given event using the [Gram-Schmidt]_ process.

    Parameters
    ----------
    initial_vectors
        Set of four linearly independent vectors; four-velocity at event
        convenient as first initial vector.
    event
        Event's spacetime coordinates.
    metric
        Metric line element as a function of spacetime coordinates.

    Returns
    -------
        Set of perpendicular tetrad vectors at given event coordinates.

    References
    ----------
    .. [Gram-Schmidt] Schmidt, Erhard. "Zur Theorie der linearen und
        nichtlinearen Integralgleichungen: I. Teil: Entwicklung willkürlicher
        Funktionen nach Systemen vorgeschriebener." Mathematische Annalen 63,
        no. 4 (1907): 433-476.
    """

    w1, w2, w3, w4 = initial_vectors

    e0_norm = c
    e0 = w1 / e0_norm

    e1_nonorm = (w2
                 - (scalar_product(metric_evaluated, e0, w2) * e0
                    / scalar_product(metric_evaluated, e0, e0)))
    e1_norm = np.sqrt(scalar_product(metric_evaluated, e1_nonorm, e1_nonorm))
    e1 = e1_nonorm / e1_norm

    e2_nonorm = (w3
                 - (scalar_product(metric_evaluated, e0, w3) * e0
                    / scalar_product(metric_evaluated, e0, e0))
                 - (scalar_product(metric_evaluated, e1, w3) * e1
                    / scalar_product(metric_evaluated, e1, e1)))
    e2_norm = np.sqrt(scalar_product(metric_evaluated, e2_nonorm, e2_nonorm))
    e2 = e2_nonorm / e2_norm

    e3_nonorm = (w4
                 - (scalar_product(metric_evaluated, e0, w4) * e0
                    / scalar_product(metric_evaluated, e0, e0))
                 - (scalar_product(metric_evaluated, e1, w4) * e1
                    / scalar_product(metric_evaluated, e1, e1))
                 - (scalar_product(metric_evaluated, e2, w4) * e2
                    / scalar_product(metric_evaluated, e2, e2)))
    e3_norm = np.sqrt(scalar_product(metric_evaluated, e3_nonorm, e3_nonorm))
    e3 = e3_nonorm / e3_norm

    return e0, e1, e2, e3


@overload
def cartesian_coordinates(
        r: VectorNd,
        theta: VectorNd,
        phi: VectorNd,
) -> VectorNd:
    ...


@overload
def cartesian_coordinates(
        r: np.float64,
        theta: VectorNd,
        phi: VectorNd,
) -> VectorNd:
    ...


@overload
def cartesian_coordinates(
        r: np.float64,
        theta: np.float64,
        phi: np.float64,
) -> VectorNd:
    ...


def cartesian_coordinates(r, theta, phi):
    """Transform spherical-like coordinates into cartesian coordinates.

    Parameters
    ----------
    r
        Radial coordinate value.
    theta
        Angular (polar) coordinate value.
    phi
        Angular (azimuthal) coordinate value.

    Returns
    -------
        Cartesian coordinates corresponding to given input coordinates.
    """

    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)

    return np.array([x, y, z])


def data_interpolation(
        curve_data: pd.DataFrame,
) -> interpolate.interp1d:
    """Interpolate spatial coordinates and tangent vectors with x0.

    Since x0 is a measure of coordinate time, interpolating w.r.t. x0 is
    convenient when comparing spatial coordinate differences (at the same
    coordinate time / on the timelike hypersurface).

    Parameters
    ----------
    curve_data
        Dataset containing either observer or light coordinates and tangent
        vectors.

    Returns
    -------
        Set of spatial coordinate and tangent vector interpolations.
    """

    x_data = curve_data.loc[:, 'x0_coordinate']  # type: ignore[misc]
    y_data = curve_data.loc[:, 'r_coordinate':'dphidtau']  # type: ignore[misc]

    return interpolate.interp1d(x_data.to_numpy(), y_data.to_numpy(), axis=0)


def load_dataset(
        filename: str,
        first_row: int | None = None,
        last_row: int | None = None,
        step_size: int = 1,
) -> Generator[pd.DataFrame, None, None]:
    """Load DataFrames from h5 file.

    Parameters
    ----------
    filename
        Name of file containing the desired DataFrames.
    first_row
        Starting row of the loaded DataFrame.
    last_row
        Last row of the loaded DataFrame.
    step_size
        Interval size from which only first row will be loaded.

    Returns
    -------
        DataFrames containing coordinates and tangent vectors.
    """

    with pd.HDFStore(filename) as store:
        keys = store.keys()

    data: Generator[pd.DataFrame, None, None] = (
        pd.read_hdf(filename, key=key, start=first_row, stop=last_row)
        for key in keys)

    if step_size != 1:
        return (dataset[::step_size] for dataset in data)

    return data


def curve_dataframe(
        dataset: tuple[
            np.ndarray[Any, np.dtype[np.float64]],
            np.ndarray[Any, np.dtype[np.float64]],
        ]
) -> pd.DataFrame:
    """Write curve data into a DataFrame.


    Parameters
    ----------
    dataset
        Affine parameter array and ndarray of coordinates and tangent vectors.

    Returns
    -------
        DataFrame containing affine parameter, coordinates and tangent vectors.
    """

    affine_parameter_array, coordinates_arrays = dataset[0], dataset[1]

    coordinates_dataframe = pd.DataFrame(
        {
            "affine_parameter": affine_parameter_array,
            "x0_coordinate": coordinates_arrays[0, :],
            "r_coordinate": coordinates_arrays[1, :],
            "theta_coordinate": coordinates_arrays[2, :],
            "phi_coordinate": coordinates_arrays[3, :],
            "dx0dtau": coordinates_arrays[4, :],
            "drdtau": coordinates_arrays[5, :],
            "dthetadtau": coordinates_arrays[6, :],
            "dphidtau": coordinates_arrays[7, :],
        }
    )

    return coordinates_dataframe
