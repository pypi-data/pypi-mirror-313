"""
Solve the emitter-observer problem for two given timelike curves.
"""

import logging
from multiprocessing import Process, Semaphore, cpu_count, Queue
import numpy as np
import pandas as pd
from scipy.optimize import differential_evolution, root
from scipy.integrate import solve_ivp, solve_bvp
from scipy.interpolate import interp1d
from scipy.constants import c
from .config import Config
from .orbit_calc import geodesic_equation
from .metric_config_numpy import metric_lambdified
from .metric_config_sympy import metric_line_elements
from .common import (
    gram_schmidt_process,
    data_interpolation,
    scalar_product,
    cartesian_coordinates,
    curve_dataframe,
    VectorNd,
    Tuple2,
    NpTuple2,
    Tuple4Nd,
    MetricFunction,
    MetricDerivativesFunction,
    ODESolution,
)
from ._solversetupconfig import _SolverSetupConfig

logger = logging.getLogger(__name__)


def tangent_vector_lightlike(
        normalisation_factor: float,
        tetrad_vectors: Tuple4Nd,
        initial_angles: Tuple2,
        signal_frequency: float = 3.6e9  # Telecom frequency
) -> VectorNd:
    """Calculate tangent vector for given celestial coordinates.

    Since normalisation_factor can be chosen freely, vector is not necessarily
    normalised.

    Parameters
    ----------
    normalisation_factor
        Needs to be chosen correctly for correct normalisation.
    tetrad_vectors
        Tetrad of linearly-independent vectors.
    initial_angles
        Reference frame dependent celestial coordinates covering the emitter's
        celestial sphere; usually defined on the intervals [0, Pi], [0, 2*Pi].
    signal_frequency
        Initial signal frequency measured in the emitter frame.

    Returns
    -------
        Tangent vector components defined via the celestial coordinates.
    """

    e0, e1, e2, e3 = tetrad_vectors
    psi, chi = initial_angles
    tangent_vector = signal_frequency / c * (
        e0
        + normalisation_factor * (
            np.sin(psi) * np.cos(chi) * e1
            + np.sin(psi) * np.sin(chi) * e2
            + np.cos(psi) * e3
        )
    )

    return tangent_vector


def spacelike_geodesic_proper_length(
        emission_event: list[float] | VectorNd,
        reception_event: list[float] | VectorNd,
        metric_function: MetricFunction,
        metric_derivatives: MetricDerivativesFunction,
        metric_inverse: MetricFunction,
        affine_parameter_mesh_length: int,
) -> np.float64:
    """Calculate the geodesic's proper length between two events.

    The proper length along a curve in General Relativity is given by a line
    integral. The proper length between two events is calculated by first
    calculating a geodesic between the given events and then integrating along
    the resulting curve. The integral is calculated here using the
    [Chebyshev-Gauss]_ quadrature.

    Parameters
    ----------
    emission_event
        Emission event's spacetime coordinates.
    reception_event
        Reception event's spacetime coordinates.
    metric_function
        Metric line element as a function of spacetime coordinates.
    metric_derivatives
        List of metric line element derivatives w.r.t. spacetime coordinates.
    metric_inverse
        Inverted metric line element.
    affine_parameter_mesh_length
        Number of mesh nodes for the solution of the geodesic equation
        boundary-value problem.

    Returns
    -------
        Proper length of geodesic between events.

    References
    ----------
    .. [Chebyshev-Gauss] M. Abramowitz, IA Stegun, eds. "Handbook of
        Mathematical Functions with Formulas, Graphs, and Mathematical Tables"
        Dover (1972): 889.
    """

    cg_lower_bound, cg_upper_bound = -1, 1

    spacelike_geodesic = spacelike_geodesic_solver(
        emission_event,
        reception_event,
        metric_derivatives,
        metric_inverse,
        np.linspace(cg_lower_bound,
                    cg_upper_bound,
                    affine_parameter_mesh_length),
    )

    spacelike_geodesic_interval_max = len(spacelike_geodesic.y[0])

    length = np.float64(0)

    for index in range(spacelike_geodesic_interval_max):

        factor = np.sqrt(1
                         - np.cos((2 * index - 1) * np.pi
                                  / (2 * spacelike_geodesic_interval_max))**2)

        factor_2 = np.sqrt(
            np.einsum(
                'ij,i,j->',
                metric_function(*spacelike_geodesic.y[0:4, index]),
                spacelike_geodesic.y[4:8, index],
                spacelike_geodesic.y[4:8, index])
        )

        length += np.pi * factor * factor_2 / spacelike_geodesic_interval_max

    return length


def euclidean_distance(
        event_1_coordinates: list[float] | VectorNd,
        event_2_coordinates: list[float] | VectorNd,
) -> np.float64:
    """Approximate spacelike (hypersurface) distance between two events.

    By omitting the metric in the calculation (assuming flat spacetime), the
    resulting coordinate difference is just an approximation and for large
    coordinate differences not a real "physical" distance. Only for small
    coordinate differences does it become a distance in the euclidean sense.

    Parameters
    ----------
    event_1_coordinates
        First event's spacetime coordinates.
    event_2_coordinates
        Second event's spacetime coordinates.

    Returns
    -------
        hypersurface distance between events in the euclidean sense.
    """

    vector_1 = cartesian_coordinates(*event_1_coordinates)
    vector_2 = cartesian_coordinates(*event_2_coordinates)

    difference_vector = vector_1 - vector_2

    return np.linalg.norm(difference_vector)


class MinimumEvent:
    """Class to find a minimum between solve_ivp solution and reference curve.

    Attributes
    ----------
    orbit_receiver_interpolation: interp1d
        Receiver curve interpolated w.r.t. coordinate time x0.
    euclidean_approximation: bool
        If true, euclidean approximation is used for distance measurements;
        recommended only for weakly curved regions of spacetime.
    terminal: bool
        If true, functions calling this event stop once minimum is found.
    """

    def __init__(
            self,
            orbit_receiver_interpolation: interp1d,
            euclidean_approximation: bool,
            terminal: bool,
    ) -> None:
        """Define class attributes.

        Parameters
        ----------
        orbit_receiver_interpolation
            Receiver curve interpolated w.r.t. coordinate time x0.
        euclidean_approximation
            If true, euclidean approximation is used for distance measurements;
            recommended only for weakly curved regions of spacetime.
        terminal
            If true, functions calling this event stop once minimum is found.
        """
        self.store: np.float64 | None = None
        self.orbit_receiver_interpolation = orbit_receiver_interpolation
        self.euclidean_approximation = euclidean_approximation
        self.terminal = terminal

    def __call__(
        self,
        _affine_parameter: np.float64,
        light_ray_data: VectorNd,
        metric_function: MetricFunction,
        metric_derivatives: MetricDerivativesFunction,
        metric_inverse: MetricFunction,
        affine_parameter_mesh_length: int,
    ) -> int:
        """Define class attributes.

        Parameters
        ----------
        _affine_parameter
            Affine parameter that parametrises the geodesic.
        light_ray_data
            Light ray event coordinates and tangent vector to the event.
        metric_function
            Metric line element as a function of spacetime coordinates.
        metric_derivatives
            List of metric line element derivatives w.r.t. spacetime coordinates.
        metric_inverse
            Inverted metric line element.
        affine_parameter_mesh_length
            Number of mesh nodes for the solution of the geodesic equation
            boundary-value problem.

        Returns
        -------
            1 if the calculated distance is smaller than the previously
            calculated distance; 0 if larger. The latter case indicates a
            minimum along the given curve having been found.
        """

        x0_coordinate = light_ray_data[0]
        if self.euclidean_approximation:
            spatial_receiver_coordinates = self.orbit_receiver_interpolation(
                x0_coordinate
            )[0:3]
            spatial_light_ray_coordinates = light_ray_data[1:4]
            distance_measure = euclidean_distance(
                spatial_receiver_coordinates,
                spatial_light_ray_coordinates,
            )

        else:
            receiver_event = np.array([
                x0_coordinate,
                *self.orbit_receiver_interpolation(x0_coordinate)[0:3],
            ])
            light_event = light_ray_data[0:4]
            distance_measure = spacelike_geodesic_proper_length(
                light_event,
                receiver_event,
                metric_function,
                metric_derivatives,
                metric_inverse,
                affine_parameter_mesh_length,
            )

        if self.store is None or distance_measure < self.store:
            self.store = distance_measure
            return 1

        return 0


def _geodesic_equation_ivp_wrapper(
        affine_parameter: float,
        event_velocity_array: VectorNd,
        _metric_function: MetricFunction,
        metric_derivatives: MetricDerivativesFunction,
        metric_inverse: MetricFunction,
        _affine_parameter_mesh_length: int,
) -> VectorNd:
    """Wrap geodesic equation to allow for event handling."""

    return geodesic_equation(affine_parameter,
                             event_velocity_array,
                             metric_derivatives,
                             metric_inverse)


def light_ray_ivp(
        initial_angles: Tuple2,
        tetrad_vectors: Tuple4Nd,
        emission_event: VectorNd,
        curve_receiver_interpolation: interp1d,
        metric_function: MetricFunction,
        metric_derivatives: MetricDerivativesFunction,
        metric_inverse: MetricFunction,
        solver_setup_config: _SolverSetupConfig,
        affine_parameter_interval: NpTuple2 | None = None,
) -> ODESolution:
    """Solve initial value problem for given initial angles and emission event.

    The length of the curve is determined via an 'event' passed to the
    scipy.integrate.solve_ivp solver: For each step of the solver, check
    whether the coordinate difference between light ray and receiver decreases
    or increases. In weakly curved (!) spacetimes, the coordinate difference
    will be a function (of affine parameter s) with at most one minimum. When
    this minimum is passed, the coordinate difference increases, triggering the
    event. In case the light ray starts in the 'wrong' direction, the
    difference will increase immediately, also triggering the event.

    Parameters
    ----------
    initial_angles
        Reference frame dependent celestial coordinates covering the emitter's
        celestial sphere; usually defined on the intervals [0, Pi], [0, 2*Pi].
    tetrad_vectors
        Tetrad of linearly-independent vectors.
    emission_event
        Emission event's spacetime coordinates.
    curve_receiver_interpolation
        Timelike receiver curve's coordinates and tangent vector interpolation.
    metric_function
        Metric line element as a function of spacetime coordinates.
    metric_derivatives
        List of metric line element derivatives w.r.t. spacetime coordinates.
    metric_inverse
        Inverted metric line element.
    solver_setup_config
        Class instance containing parameters for approximations and solvers.
    affine_parameter_interval
        Initial and final affine parameter value elapsing along solution curve.

    Returns
    -------
        Curve solving the initial value problem for given celestial angles.
    """

    if affine_parameter_interval is None:
        affine_parameter_interval = (np.float64(0), np.float64(np.inf))

    metric_evaluated = metric_function(*emission_event)

    # By definition of the tangent vector through a tetrad, the normalisation
    # factor is 1. Check this by finding the root of the normalisation equation
    # and look specifically near x0=1:
    normalisation_factor = root(
        lambda norm: scalar_product(
            metric_evaluated,
            tangent_vector_lightlike(norm,
                                     tetrad_vectors,
                                     initial_angles),
            tangent_vector_lightlike(norm,
                                     tetrad_vectors,
                                     initial_angles)),
        x0=1,
        tol=solver_setup_config.root_tolerance).x

    initial_tangent_vector = tangent_vector_lightlike(normalisation_factor,
                                                      tetrad_vectors,
                                                      initial_angles)

    past_minimum = MinimumEvent(curve_receiver_interpolation,
                                solver_setup_config.euclidean_approximation,
                                terminal=True)

    return solve_ivp(
        _geodesic_equation_ivp_wrapper,
        affine_parameter_interval,
        (*emission_event, *initial_tangent_vector),
        events=past_minimum,
        atol=solver_setup_config.solve_ivp_absolute_tolerance,
        rtol=solver_setup_config.solve_ivp_relative_tolerance,
        args=(metric_function,
              metric_derivatives,
              metric_inverse,
              solver_setup_config.affine_parameter_mesh_length),
    )


def spacelike_distance_minimisation(
        initial_angles: Tuple2,
        tetrad_vectors: Tuple4Nd,
        emission_event: VectorNd,
        curve_receiver_interpolation: interp1d,
        metric_function: MetricFunction,
        metric_derivatives: MetricDerivativesFunction,
        metric_inverse: MetricFunction,
        solver_setup_config: _SolverSetupConfig,
        affine_parameter_interval: NpTuple2 | None = None,
        affine_parameter_output: bool = False,
) -> np.float64:
    """Find minimal spacelike coordinate difference between two curves.

    For given initial angles and emission event, solve initial value problem
    for light ray curve and find minimal spacelike coordinate difference
    between light ray and some receiver curve.

    Parameters
    ----------
    initial_angles
        Reference frame dependent celestial coordinates covering the emitter's
        celestial sphere; usually defined on the intervals [0, Pi], [0, 2*Pi].
    tetrad_vectors
        Tetrad of linearly-independent vectors.
    emission_event
        Emission event's spacetime coordinates.
    curve_receiver_interpolation
        Timelike receiver curve's coordinates and tangent vector interpolation.
    metric_function
        Metric line element as a function of spacetime coordinates.
    metric_derivatives
        List of metric line element derivatives w.r.t. spacetime coordinates.
    metric_inverse
        Inverted metric line element.
    affine_parameter_interval
        Initial and final affine parameter value elapsing along solution curve.
    solve_ivp_absolute_tolerance
        Absolute tolerance of the scipy.integrate.solve_ivp function.
    solve_ivp_relative_tolerance
        Relative tolerance of the scipy.integrate.solve_ivp function.
    max_euclidean_distance
        Maximum euclidean distance between light ray and receiver curves.
    affine_parameter_output
        Function returns affine parameter at minimal distance if True, minimal
        distance if False.

    Returns
    -------
        Minimal distance between curves or respective affine parameter value.
    """

    if affine_parameter_interval is None:
        affine_parameter_interval = (np.float64(0), np.float64(np.inf))

    light_ray_solution = light_ray_ivp(
        initial_angles,
        tetrad_vectors,
        emission_event,
        curve_receiver_interpolation,
        metric_function,
        metric_derivatives,
        metric_inverse,
        solver_setup_config,
        affine_parameter_interval,
    )

    # need to remove final values because of scipy_ivp behaviour with events,
    # where the final event is added twice to the arrays
    light_ray_solution_t = np.delete(light_ray_solution.t, -1)
    light_ray_solution_y = [np.delete(array, -1) for array in
                            light_ray_solution.y]

    while True:

        if len(light_ray_solution_t) < 2:
            closest_x0 = light_ray_solution_y[0][0]
            closest_event = [coordinate_array[-1] for coordinate_array
                             in light_ray_solution_y[0:4]]

            if solver_setup_config.euclidean_approximation:
                minimal_distance_measure = euclidean_distance(
                    curve_receiver_interpolation(closest_x0)[0:3],
                    closest_event[1:4],
                )
            else:
                receiver_event = np.array([
                    closest_x0,
                    *curve_receiver_interpolation(closest_x0)[0:3],
                ])
                minimal_distance_measure = spacelike_geodesic_proper_length(
                    closest_event,
                    receiver_event,
                    metric_function,
                    metric_derivatives,
                    metric_inverse,
                    solver_setup_config.affine_parameter_mesh_length,
                )

            logger.debug('Minimal distance %s',
                         np.abs(minimal_distance_measure))

            return np.abs(minimal_distance_measure)

        (penultimate_affine_parameter,
         final_affine_parameter) = light_ray_solution_t[-2:]
        penultimate_x0, closest_x0 = light_ray_solution_y[0][-2:]
        closest_event = [coordinate_array[-1] for coordinate_array
                         in light_ray_solution_y[:4]]
        penultimate_event = [coordinate_array[-2] for coordinate_array
                             in light_ray_solution_y[:4]]
        penultimate_tangent_vectors = [vector_array[-2] for vector_array
                                       in light_ray_solution_y[4:8]]

        if solver_setup_config.euclidean_approximation:
            minimal_distance_measure = euclidean_distance(
                curve_receiver_interpolation(closest_x0)[:3],
                closest_event[1:4],
            )
            penultimate_distance_measure = euclidean_distance(
                curve_receiver_interpolation(penultimate_x0)[:3],
                penultimate_event[1:4],
            )
        else:
            closest_receiver_event = np.array([
                closest_x0,
                *curve_receiver_interpolation(closest_x0)[:3],
            ])
            minimal_distance_measure = spacelike_geodesic_proper_length(
                closest_event,
                closest_receiver_event,
                metric_function,
                metric_derivatives,
                metric_inverse,
                solver_setup_config.affine_parameter_mesh_length,
            )
            penultimate_receiver_event = np.array([
                penultimate_x0,
                *curve_receiver_interpolation(penultimate_x0)[:3],
            ])
            penultimate_distance_measure = spacelike_geodesic_proper_length(
                penultimate_event,
                penultimate_receiver_event,
                metric_function,
                metric_derivatives,
                metric_inverse,
                solver_setup_config.affine_parameter_mesh_length,
            )

        if (penultimate_distance_measure - minimal_distance_measure
           < solver_setup_config.max_distance_measure):

            logger.debug('Minimal distance %s',
                         np.abs(minimal_distance_measure))

            if affine_parameter_output:
                return final_affine_parameter
            return np.abs(minimal_distance_measure)

        new_max_step = (final_affine_parameter
                        - penultimate_affine_parameter) / 2

        past_minimum = MinimumEvent(curve_receiver_interpolation,
                                    solver_setup_config.euclidean_approximation,
                                    terminal=True)

        light_ray_solution = solve_ivp(
            _geodesic_equation_ivp_wrapper,
            (penultimate_affine_parameter, np.inf),
            (*penultimate_event, *penultimate_tangent_vectors),
            events=past_minimum,
            max_step=new_max_step,
            atol=solver_setup_config.solve_ivp_absolute_tolerance,
            rtol=solver_setup_config.solve_ivp_relative_tolerance,
            args=(metric_function,
                  metric_derivatives,
                  metric_inverse,
                  solver_setup_config.affine_parameter_mesh_length),
        )
        light_ray_solution_t = np.delete(light_ray_solution.t, -1)
        light_ray_solution_y = [np.delete(array, -1) for array in
                                light_ray_solution.y]


class _SpacelikeGeodesicSolver:
    """Class to calculate geodesic between two events (boundary-value problem).

    Attributes
    ----------
    emission_event: VectorNd | list[float]
        Emission event's spacetime coordinates.
    curve_receiver_interpolation: VectorNd | list[float]
        Reception event's spacetime coordinates.
    metric_derivatives: MetricDerivativesFunction
        List of metric line element derivatives w.r.t. spacetime coordinates.
    metric_inverse: MetricFunction
        Inverted metric line element.

    Methods
    -------
    _solve_bvp_boundaries(emission_event, reception_event)
        Define boundary values for the given boundary-value problem.
    _geodesic_equation_wrapper(x, y)
        Bring geodesic_equation return into suitable form for solve_bvp.
    """

    def __init__(
        self,
        emission_event: VectorNd | list[float],
        reception_event: VectorNd | list[float],
        metric_derivatives: MetricDerivativesFunction,
        metric_inverse: MetricFunction,
    ) -> None:
        """Define class attributes.

        Parameters
        ----------
        emission_event
            Emission event's spacetime coordinates.
        reception_event
            Reception event's spacetime coordinates.
        metric_derivatives
            List of metric line element derivatives w.r.t. spacetime coordinates.
        metric_inverse
            Inverted metric line element.
        """

        self.emission_event = emission_event
        self.reception_event = reception_event
        self.metric_derivatives = metric_derivatives
        self.metric_inverse = metric_inverse

    def _solve_bvp_boundaries(self,
                              emission_event: VectorNd,
                              reception_event: VectorNd) -> VectorNd:
        """Define boundary values for the given boundary-value problem.

        Parameters
        ----------
        emission_event
            Emission event's spacetime coordinates.
        reception_event
            Reception event's spacetime coordinates.

        Returns
        -------
            Array containing boundary values.
        """

        initial_condition = emission_event[0:4] - self.emission_event
        reception_condition = reception_event[0:4] - self.reception_event

        return np.array([*initial_condition, *reception_condition])

    def _geodesic_equation_wrapper(self,
                                   affine_parameter: float,
                                   events_grid: VectorNd) -> VectorNd:
        """Bring geodesic_equation return into suitable form for solve_bvp.

        solve_bvp requires a grid of points on which to evaluate the geodesic
        equation, each grid point describing an event coordinate or tangent
        vector component at one event along the geodesic. The grid contains
        all events along the geodesic.

        Parameters
        ----------
        affine_parameter
            Affine parameter that parametrises the geodesic.
        events_grid
            Array of event coordinates and tangent vector to all events along
            the geodesic.

        Returns
        -------
            Array containing all tangent vectors to the events and the
            corresponding accelerations.
        """

        solution_matrix = np.array([])
        # order of the geodesic equation * dimension of spacetime (2 * 4):
        ode_system_dimension = events_grid.shape[0]

        # number of mesh nodes on which geodesic equation is solved:
        grid_length = events_grid.shape[1]
        for i in range(grid_length):

            solution_matrix = np.append(solution_matrix, geodesic_equation(
                affine_parameter,
                events_grid[:, i],
                self.metric_derivatives,
                self.metric_inverse,
            ))

        return solution_matrix.reshape((grid_length, ode_system_dimension)).T

    def __call__(self, initial_mesh: VectorNd) -> ODESolution:
        """Calculate geodesic between two events (boundary-value problem).

        Parameters
        ----------
        initial_mesh
            Initial array containing affine parameter values at which geodesic
            should be calculated.

        Returns
        -------
            Solution to the boundary-value problem.
        """

        spacetime_dimension = 4
        geodesic_equation_order = 2
        ode_system_order = spacetime_dimension * geodesic_equation_order

        initial_guess = np.ones((ode_system_order, initial_mesh.size))

        for i in range(0, spacetime_dimension):
            initial_guess[i] = np.linspace(self.emission_event[i],
                                           self.reception_event[i],
                                           initial_mesh.size)
        return solve_bvp(
            self._geodesic_equation_wrapper,
            self._solve_bvp_boundaries,
            initial_mesh,
            initial_guess,
        )


def spacelike_geodesic_solver(
        emission_event: VectorNd | list[float],
        reception_event: VectorNd | list[float],
        metric_derivatives: MetricDerivativesFunction,
        metric_inverse: MetricFunction,
        initial_mesh: VectorNd,
) -> ODESolution:
    """Instantiate and call the _SpacelikeGeodesicSolver class.

    Parameters
    ----------
    emission_event
        Emission event's spacetime coordinates.
    reception_event
        Reception event's spacetime coordinates.
    metric_derivatives
        List of metric line element derivatives w.r.t. spacetime coordinates.
    metric_inverse
        Inverted metric line element.
    initial_mesh
        Initial array containing affine parameter values at which geodesic
        should be calculated.

    Returns
    -------
        Solution to the boundary-value problem.
    """

    spacelike_geodesic = _SpacelikeGeodesicSolver(emission_event,
                                                  reception_event,
                                                  metric_derivatives,
                                                  metric_inverse)

    return spacelike_geodesic(initial_mesh)


def initial_angle_approximation(
        tangent_vector,
        tetrad_vectors,
        metric_evaluated
) -> Tuple2:
    """Calculate celestial angles of a given tangent vector.

    Parameters
    ----------
    tangent_vector
        Tangent vector to a curve.
    tetrad_vectors
        Tetrad of linearly-independent vectors.
    metric_evaluated
        Spacetime metric evaluated at some event.

    Returns
    -------
        Celestial angles pointing in the direction of the given tangent vector.
    """

    _, e1, e2, e3 = tetrad_vectors

    tangent_vector_norm = (
        tangent_vector
        / scalar_product(metric_evaluated, tangent_vector, tangent_vector)
    )

    scalar_1 = scalar_product(metric_evaluated, tangent_vector_norm, e1)
    scalar_2 = scalar_product(metric_evaluated, tangent_vector_norm, e2)
    scalar_3 = scalar_product(metric_evaluated, tangent_vector_norm, e3)
    psi = np.arccos(scalar_3 / np.linalg.norm([scalar_1, scalar_2, scalar_3]))
    chi = np.arctan2(scalar_2, scalar_1)

    return psi, chi


def light_ray_differential_evolution(
        tetrad_vectors: Tuple4Nd,
        emission_event: VectorNd,
        curve_receiver_interpolation: interp1d,
        metric_function: MetricFunction,
        metric_derivatives: MetricDerivativesFunction,
        metric_inverse: MetricFunction,
        solver_setup_config: _SolverSetupConfig,
        dataframe_row_index: int,
        affine_parameter_interval: NpTuple2 | None = None,
) -> tuple[VectorNd, VectorNd]:
    """Find light ray curve connecting emission event and receiver curve.

    It is convenient to transform this boundary value problem, namely
    connecting two events, into multipole initial value problems, since the
    reception boundary event changes during the propagation of the solution
    light ray; this is also known as 'shooting method'. Solving the geodesic
    equation for the light ray requires its initial tangent vector; this can be
    expressed in terms of celestial coordinates pointing to a spot on the
    emitter's celestial sphere.

    Parameters
    ----------
    tetrad_vectors
        Tetrad of linearly-independent vectors.
    emission_event
        Emission event's spacetime coordinates.
    curve_receiver_interpolation
        Timelike receiver curve's coordinates and tangent vector interpolation.
    metric_function
        Metric line element as a function of spacetime coordinates.
    metric_derivatives
        List of metric line element derivatives w.r.t. spacetime coordinates.
    metric_inverse
        Inverted metric line element.
    solver_setup_config
        Class instance containing parameters for approximations and solvers.
    dataframe_row_index
        Row index, only used for logging the number of the emission event.
    affine_parameter_interval
        Initial and final affine parameter value elapsing along solution curve.

    Returns
    -------
        Affine parameter array and coordinate and tangent vector arrays
    """

    if affine_parameter_interval is None:
        affine_parameter_interval = (np.float64(0), np.float64(np.inf))

    emission_x0 = emission_event[0]

    reception_event = np.array([
        emission_x0,
        *curve_receiver_interpolation(emission_x0)[:3],
    ])

    if solver_setup_config.hypersurface_approximation:

        # in its numeric implementation, the geodesic equation only implicitly
        # depends on the affine parameter. Therefore, when choosing an initial
        # mesh on which to solve the eq., the explicit choice of affine
        # parameter is arbitrary, only the length is relevant, e.g. choose
        # affine parameter on an interval [1, 2].
        spacelike_geodesic_solution = spacelike_geodesic_solver(
            emission_event,
            reception_event,
            metric_derivatives,
            metric_inverse,
            initial_mesh=np.linspace(
                1,
                2,
                solver_setup_config.affine_parameter_mesh_length,
            ),
        )
        velocity_tangent_vector = spacelike_geodesic_solution.y[4:8, 0]
        metric_evaluated = metric_function(*emission_event)
        angle_approx = initial_angle_approximation(velocity_tangent_vector,
                                                   tetrad_vectors,
                                                   metric_evaluated)

        # project azimuthal angle from interval [-pi, pi] to [0, 2 * pi]:
        if angle_approx[1] < 0:
            angle_approx = angle_approx[0], angle_approx[1] + 2 * np.pi

        psi_interval = (
            angle_approx[0] - solver_setup_config.hypersurface_angle_range,
            angle_approx[0] + solver_setup_config.hypersurface_angle_range,
        )
        chi_interval = (
            angle_approx[1] - solver_setup_config.hypersurface_angle_range,
            angle_approx[1] + solver_setup_config.hypersurface_angle_range,
        )

    else:

        # test entire celestial sphere; use a buffer to cover edge cases like
        # 0 or pi. With a buffer, the angles are not unique, e.g. for psi the
        # values -0.1 and pi - 0.1 give identical results, but since only the
        # curve is of interest and not the angles, it does not matter.
        angle_buffer = 0.1
        psi_interval = (-angle_buffer, np.pi + angle_buffer)
        chi_interval = (-angle_buffer, 2 * np.pi + angle_buffer)

    minimised_light_ray_solution = differential_evolution(
        spacelike_distance_minimisation,
        bounds=[psi_interval, chi_interval],
        args=(tetrad_vectors,
              emission_event,
              curve_receiver_interpolation,
              metric_function,
              metric_derivatives,
              metric_inverse,
              solver_setup_config,
              affine_parameter_interval),
        popsize=solver_setup_config.de_popsize,
        maxiter=solver_setup_config.de_max_iterations,
        tol=solver_setup_config.de_relative_tolerance,
        atol=solver_setup_config.de_absolute_tolerance,
        mutation=(1e-4, 5e-1),
    )

    initial_angles = minimised_light_ray_solution.x

    final_affine_parameter = spacelike_distance_minimisation(
        initial_angles,
        tetrad_vectors,
        emission_event,
        curve_receiver_interpolation,
        metric_function,
        metric_derivatives,
        metric_inverse,
        solver_setup_config,
        affine_parameter_interval,
        affine_parameter_output=True,
    )

    light_ray_data = light_ray_ivp(
        initial_angles,
        tetrad_vectors,
        emission_event,
        curve_receiver_interpolation,
        metric_function,
        metric_derivatives,
        metric_inverse,
        solver_setup_config,
        (affine_parameter_interval[0], final_affine_parameter),
    )

    final_x0_coordinate = light_ray_data.y[0][-1]
    light_ray_coords = light_ray_data.y[0:4, -1]
    timelike_coords = np.array([
        final_x0_coordinate,
        *curve_receiver_interpolation(final_x0_coordinate)[0:3],
    ])

    metric_evaluated_list = [metric_function(*light_ray_data.y[0:4, i])
                             for i in range(len(light_ray_data.t))]

    light_ray_normalisation = [abs(scalar_product(
        metric_evaluated_list[i],
        light_ray_data.y[4:8, i],
        light_ray_data.y[4:8, i],
    ) / c ** 2) for i in range(len(light_ray_data.t))]

    logger.info('Emission event #%s', dataframe_row_index)
    logger.info('final initial angles: %s', initial_angles)
    logger.info('minimal_distance: %s',
                spacelike_geodesic_proper_length(
                    light_ray_coords,
                    timelike_coords,
                    metric_function,
                    metric_derivatives,
                    metric_inverse,
                    solver_setup_config.affine_parameter_mesh_length,
                ))
    logger.info('Initial and final scalar product: %s, %s',
                light_ray_normalisation[0],
                light_ray_normalisation[-1])

    return light_ray_data.t, light_ray_data.y


def light_ray_calculation(
        dataframe_emitter_row: pd.DataFrame,
        curve_receiver_interpolation: interp1d,
        metric_function: MetricFunction,
        metric_derivatives: MetricDerivativesFunction,
        metric_inverse: MetricFunction,
        solver_setup_config: _SolverSetupConfig,
        multiprocessing: bool,
) -> tuple[VectorNd, VectorNd]:
    """Calculate and save light ray connecting emission and reception event.

    For simpler tracking of which light ray corresponds to which emission
    event after multiprocessing, the solutions are first indexed and then
    queued instead of just returned.

    Parameters
    ----------
    dataframe_emitter_row
        DataFrame row containing one emission event and tangent vector.
    curve_receiver_interpolation
        Timelike receiver curve's coordinates and tangent vector interpolation.
    metric_function
        Metric line element as a function of spacetime coordinates.
    metric_derivatives
        List of metric line element derivatives w.r.t. spacetime coordinates.
    metric_inverse
        Inverted metric line element.
    solver_setup_config
        Class instance containing parameters for approximations and solvers.
    multiprocessing
        Boolean signifying whether multiprocessing is used.

    Returns
    -------
    None
    """

    emission_event: VectorNd = np.array(dataframe_emitter_row[[
            'x0_coordinate',
            'r_coordinate',
            'theta_coordinate',
            'phi_coordinate',
        ]])[0] if multiprocessing else np.array(dataframe_emitter_row[[
            'x0_coordinate',
            'r_coordinate',
            'theta_coordinate',
            'phi_coordinate',
        ]])

    emitter_velocity: VectorNd = np.array(dataframe_emitter_row[[
            'dx0dtau', 'drdtau', 'dthetadtau', 'dphidtau'
        ]])[0] if multiprocessing else np.array(dataframe_emitter_row[[
            'dx0dtau', 'drdtau', 'dthetadtau', 'dphidtau'
        ]])

    # Choice arbitrary, but initial vectors need to be linearly independent
    tetrad_initial_vectors: Tuple4Nd = (
        emitter_velocity,
        np.array([0, 1, 0, 0]),
        np.array([0, 0, 1, 0]),
        np.array([0, 0, 0, 1])
    )

    metric_evaluated = metric_function(*emission_event)

    tetrad_vectors = gram_schmidt_process(tetrad_initial_vectors,
                                          metric_evaluated)

    if multiprocessing:

        light_ray_solution = light_ray_differential_evolution(
            tetrad_vectors,
            emission_event,
            curve_receiver_interpolation,
            metric_function,
            metric_derivatives,
            metric_inverse,
            solver_setup_config,
            dataframe_emitter_row.index[0],
        )

    else:

        light_ray_solution = light_ray_differential_evolution(
            tetrad_vectors,
            emission_event,
            curve_receiver_interpolation,
            metric_function,
            metric_derivatives,
            metric_inverse,
            solver_setup_config,
            dataframe_emitter_row.name,
        )

    return light_ray_solution


def light_ray_calculation_multiprocessing(
        dataframe_emitter_row: pd.DataFrame,
        curve_receiver_interpolation: interp1d,
        metric_function: MetricFunction,
        metric_derivatives: MetricDerivativesFunction,
        metric_inverse: MetricFunction,
        solver_setup_config: _SolverSetupConfig,
        semaphore_calculations,
        multiprocessing_queue: Queue,
) -> None:
    """Wrap light_ray_calculation function when multiprocessing is used.

    Parameters
    ----------
    dataframe_emitter_row
        DataFrame row containing one emission event and tangent vector.
    curve_receiver_interpolation
        Timelike receiver curve's coordinates and tangent vector interpolation.
    metric_function
        Metric line element as a function of spacetime coordinates.
    metric_derivatives
        List of metric line element derivatives w.r.t. spacetime coordinates.
    metric_inverse
        Inverted metric line element.
    solver_setup_config
        Class instance containing parameters for approximations and solvers.
    semaphore_calculations
        Semaphore for multiprocessing of light ray calculations.
    multiprocessing_queue
        Queue for storing indexed light ray solutions.

    Returns
    -------
    None
    """

    with semaphore_calculations:
        light_ray_solution = light_ray_calculation(
            dataframe_emitter_row,
            curve_receiver_interpolation,
            metric_function,
            metric_derivatives,
            metric_inverse,
            solver_setup_config,
            multiprocessing=True,
        )

        multiprocessing_queue.put((dataframe_emitter_row.index[0],
                                   curve_dataframe(light_ray_solution)))


def light_ray_calculation_no_multiprocessing(
        dataframe_emitter_row: pd.DataFrame,
        curve_receiver_interpolation: interp1d,
        metric_function: MetricFunction,
        metric_derivatives: MetricDerivativesFunction,
        metric_inverse: MetricFunction,
        solver_setup_config: _SolverSetupConfig,
        solutions_list: list[tuple[int, pd.DataFrame]],
) -> None:
    """Wrap light_ray_calculation function when multiprocessing is not used.

    Parameters
    ----------
    dataframe_emitter_row
        DataFrame row containing one emission event and tangent vector.
    curve_receiver_interpolation
        Timelike receiver curve's coordinates and tangent vector interpolation.
    metric_function
        Metric line element as a function of spacetime coordinates.
    metric_derivatives
        List of metric line element derivatives w.r.t. spacetime coordinates.
    metric_inverse
        Inverted metric line element.
    solver_setup_config
        Class instance containing parameters for approximations and solvers.
    solutions_list
        List for storing indexed light ray solutions.

    Returns
    -------
    None
    """

    light_ray_solution = light_ray_calculation(
        dataframe_emitter_row,
        curve_receiver_interpolation,
        metric_function,
        metric_derivatives,
        metric_inverse,
        solver_setup_config,
        multiprocessing=False,
    )

    solutions_list.append((dataframe_emitter_row.name,
                          curve_dataframe(light_ray_solution)))


def eop_solver(
        config: Config,
        curve_emitter: pd.DataFrame,
        curve_receiver: pd.DataFrame,
        multiprocessing: bool = False,
        hypersurface_approximation: bool = True,
        hypersurface_angle_range: float = 1e-4,
        de_relative_tolerance: float = 0,
        de_absolute_tolerance: float = 1e-4,
        de_popsize: float = 50,
        de_max_iterations: float = 15,
        solve_ivp_absolute_tolerance: float = 1e-20,
        solve_ivp_relative_tolerance: float = 3e-14,
        root_tolerance: float = 1e-12,
        max_distance_measure: float = 1e-2,
        euclidean_approximation: bool = False,
        affine_parameter_mesh_length: int = 10,
        verbose: int = 0,
) -> list[tuple[int, pd.DataFrame]]:
    """Calculate light ray solutions for given emitter and receiver orbit data.

    Parameters
    ----------
    config
        Configuration dictionary containing metric information.
    curve_emitter
        Emitter curve's coordinates and tangent vector at each event.
    curve_receiver
        Receiver curve's coordinates and tangent vector at each event.
    multiprocessing
        Switch multiprocessing on to calculate multiple light rays in parallel.
    hypersurface_approximation
        Switch on celestial angle approximation via geodesics between events in
        the hypersurface x0=const.
    hypersurface_angle_range
        For the case of the hypersurface approximation, defines the expected
        angular deviation in which the correct angles are expected to lie.
        Possible values lie in the range (0, pi).
    de_relative_tolerance
        Relative tolerance of scipy.optimize.differential_evolution.
    de_absolute_tolerance
        Absolute tolerance of scipy.optimize.differential_evolution.
    de_popsize
        Population size of scipy.optimize.differential_evolution.
    de_max_iterations
        Maximum number of iterations of scipy.optimize.differential_evolution.
    solve_ivp_absolute_tolerance
        Absolute tolerance of the scipy.integrate.solve_ivp function.
    solve_ivp_relative_tolerance
        Relative tolerance of the scipy.integrate.solve_ivp function.
    root_tolerance
        Tolerance of the scipy.optimize.root function.
    max_distance_measure
        Maximum allowed distance between light ray and receiver curve (distance
        in terms of euclidean distance or proper length depending on settings).
    euclidean_approximation
        Switch between defining length in terms of integrals over geodesics in
        spacetime (more robust, more computationally expensive) or in the
        euclidean sense (not suited for all coordinate systems, computationally
        cheaper).
    affine_parameter_mesh_length
        Number of mesh nodes for the solution of the geodesic equation
        boundary-value problem.
    verbose
        Decide the logging level.
        If 0, no information will be logged.
        If 1, info about the result curves will be logged.
        If 2, the minimal distance of each light ray candidate in differential
        evolution will additionally be logged (recommended for debugging if
        euclidean_approximation and multiprocessing are False).
        Logs will be output in the file 'greopy.log'.

    Returns
    -------
        Coordinates and tangent vectors of light rays between emitter/receiver.
    """

    if verbose == 1:
        logging.basicConfig(filename='greopy.log', level=logging.INFO)

    elif verbose == 2:
        logging.basicConfig(filename='greopy.log', level=logging.DEBUG)

    elif verbose != 0:
        raise ValueError('Verbose is not 0, 1 or 2.')

    logger.info('Started')

    solver_setup_config = _SolverSetupConfig(multiprocessing,
                                             hypersurface_approximation,
                                             hypersurface_angle_range,
                                             de_relative_tolerance,
                                             de_absolute_tolerance,
                                             de_popsize,
                                             de_max_iterations,
                                             solve_ivp_absolute_tolerance,
                                             solve_ivp_relative_tolerance,
                                             root_tolerance,
                                             max_distance_measure,
                                             euclidean_approximation,
                                             affine_parameter_mesh_length)

    orbit_receiver_interpolation = data_interpolation(curve_receiver)

    metric_function = metric_line_elements[config['Metric']['name']]
    metric_params = config['Metric']['params']
    metric_parametrised = metric_function(**metric_params)

    metric, metric_coordinate_derivatives, metric_inverse = metric_lambdified(
        metric_parametrised,
    )

    solutions_list = []

    if multiprocessing:

        cpu_number = cpu_count()
        semaphore_calculations = Semaphore(cpu_number)

        orbit_indexed = [curve_emitter[i:i + 1]
                         for i in range(len(curve_emitter))]

        q: "Queue[tuple[int, pd.DataFrame]]" = Queue()

        processes = [Process(
            target=light_ray_calculation_multiprocessing,
            args=(orbit_indexed[i],
                  orbit_receiver_interpolation,
                  metric,
                  metric_coordinate_derivatives,
                  metric_inverse,
                  solver_setup_config,
                  semaphore_calculations,
                  q)
        ) for i in range(len(orbit_indexed))]

        for process in processes:
            process.start()
        for process in processes:
            process.join()
            light_ray_solution = q.get()
            solutions_list.append(light_ray_solution)

        return solutions_list

    curve_emitter.apply(
        light_ray_calculation_no_multiprocessing,
        args=[orbit_receiver_interpolation,
              metric,
              metric_coordinate_derivatives,
              metric_inverse,
              solver_setup_config,
              solutions_list],
        axis=1,
    )  # type: ignore[call-overload]

    return solutions_list
