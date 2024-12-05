"""This module contains class definitions for static typing."""

# pylint: disable=missing-class-docstring
from typing import TypedDict


class ProperTimes(TypedDict):
    time_initial: int
    time_final: int


class InitialEvent(TypedDict):
    x0: int
    radius: int
    theta_factor: int
    phi_factor: int


class InitialVelocity(TypedDict):
    velocity_radial: int
    velocity_polar: int
    velocity_azimuthal: int


class Curve(TypedDict):
    proper_times: ProperTimes
    initial_event: InitialEvent
    initial_velocity: InitialVelocity


class MetricParams(TypedDict):
    radius_reference: int
    gravity_constant: int
    period_rotation: int
    multipole_moments: list[float]


class MetricDict(TypedDict):
    name: str
    params: MetricParams


class Config(TypedDict):
    Curve_1: Curve
    Curve_2: Curve
    Metric: MetricDict
