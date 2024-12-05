"""This module defines the class that stores solver-specific options."""


class _SolverSetupConfig:
    """Contain parameters for functions that can be adapted by the user."""

    def __init__(
        self,
        multiprocessing: bool,
        hypersurface_approximation: bool,
        hypersurface_angle_range: float,
        de_relative_tolerance: float,
        de_absolute_tolerance: float,
        de_popsize: float,
        de_max_iterations: float,
        solve_ivp_absolute_tolerance: float,
        solve_ivp_relative_tolerance: float,
        root_tolerance: float,
        max_distance_measure: float,
        euclidean_approximation: bool,
        affine_parameter_mesh_length: int,
    ):
        """Save parameters as class attributes.

        Parameters
        ----------
        config
            Configuration dictionary containing metric information.
        curve_emitter
            Emitter curve's coordinates and tangent vector at each event.
        curve_receiver
            Receiver curve's coordinates and tangent vector at each event.
        multiprocessing
            Switch multiprocessing on to calculate multiple light rays in
            parallel.
        hypersurface_approximation
            Switch on celestial angle approximation via geodesics between
            events in the hypersurface x0=const.
        hypersurface_angle_range
            For the case of the hypersurface approximation, defines the
            expected angular deviation in which the correct angles are expected
            to lie. Possible values lie in the range (0, pi).
        de_relative_tolerance
            Relative tolerance of scipy.optimize.differential_evolution.
        de_absolute_tolerance
            Absolute tolerance of scipy.optimize.differential_evolution.
        de_popsize
            Population size of scipy.optimize.differential_evolution.
        de_max_iterations
            Maximum iteration number of scipy.optimize.differential_evolution.
        solve_ivp_absolute_tolerance
            Absolute tolerance of the scipy.integrate.solve_ivp function.
        solve_ivp_relative_tolerance
            Relative tolerance of the scipy.integrate.solve_ivp function.
        root_tolerance
            Tolerance of the scipy.optimize.root function.
        max_distance_measure
            Maximum allowed distance between light ray and receiver curve
            (distance in terms of euclidean distance or proper length depending
            on settings).
        euclidean_approximation
            Switch between defining length in terms of integrals over geodesics
            in spacetime (more robust, more computationally expensive) or in
            the euclidean sense (not suited for all coordinate systems,
            computationally cheaper).
        affine_parameter_mesh_length
            Number of mesh nodes for the solution of the geodesic equation
            boundary-value problem.

        Returns
        -------
        None
        """

        self.multiprocessing = multiprocessing
        self.hypersurface_approximation = hypersurface_approximation
        self.hypersurface_angle_range = hypersurface_angle_range
        self.de_relative_tolerance = de_relative_tolerance
        self.de_absolute_tolerance = de_absolute_tolerance
        self.de_popsize = de_popsize
        self.de_max_iterations = de_max_iterations
        self.solve_ivp_absolute_tolerance = solve_ivp_absolute_tolerance
        self.solve_ivp_relative_tolerance = solve_ivp_relative_tolerance
        self.root_tolerance = root_tolerance
        self.max_distance_measure = max_distance_measure
        self.euclidean_approximation = euclidean_approximation
        self.affine_parameter_mesh_length = affine_parameter_mesh_length
