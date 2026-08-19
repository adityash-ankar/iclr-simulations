
"""
Utility functions used across the electronic_pressure_regulator package.

This module provides JIT-optimized numerical helpers (Darcy-Weisbach,
Reynolds number, orifice pressure-drop, friction factor approximations,
array-history updaters, and simple clamps). Inputs are primitive numeric
values (rho, velocity, diameter, viscosity, etc.) and the functions
return derived scalars used by component computations. Use these
functions inside performance-sensitive solver loops; they are decorated
with numba.njit where possible for speed.
"""

import numpy as np
from numba import njit
from util_funcs import *


# JIT-compiled utility functions for maximum performance
@njit
def friction_factor_laminar(re):
    """Return the Darcy friction factor for fully laminar pipe flow.

    Parameters
    ----------
    re : float
        Reynolds number for the pipe section.

    Returns
    -------
    float
        Darcy friction factor for laminar flow, or 0 when the Reynolds number
        is effectively zero.
    """
    return 64.0 / abs(re) if abs(re) > 1e-10 else 0.0

@njit
def friction_factor_turbulent_approx(re, roughness_ratio):
    """Approximate the turbulent friction factor using the Swamee-Jain formula.

    Parameters
    ----------
    re : float
        Reynolds number for the pipe section.
    roughness_ratio : float
        Relative roughness, defined as roughness / diameter.

    Returns
    -------
    float
        Estimated Darcy friction factor for turbulent flow.
    """
    re_abs = abs(re)
    if re_abs < 1e-10:
        return 0.0
    return 1.325 / (np.log((roughness_ratio / 3.7) + (5.74 / re_abs ** 0.9))) ** 2

@njit
def calculate_friction_factor(re, roughness, diameter):
    """Select the appropriate friction-factor correlation for the current flow regime.

    Parameters
    ----------
    re : float
        Reynolds number.
    roughness : float
        Pipe-wall roughness in metres.
    diameter : float
        Pipe internal diameter in metres.

    Returns
    -------
    float
        Darcy friction factor for the current flow regime.
    """
    roughness_ratio = roughness / diameter
    if abs(re) < 3000:
        return friction_factor_laminar(re)
    else:
        return friction_factor_turbulent_approx(re, roughness_ratio)

@njit
def darcy_weisbach_jit(friction_factor, length, diameter, rho, velocity):
    """Compute the Darcy-Weisbach pressure drop contribution for a pipe segment.

    The result is the static pressure loss term caused by frictional dissipation
    in the pipe. It is used as a local loss term when solving pressure and mass
    flow evolution in the time-stepping loop.
    """
    return friction_factor * (length / diameter) * (rho * velocity * abs(velocity)) / 2

@njit
def reynolds_number_jit(rho, velocity, diameter, viscosity):
    """Compute the Reynolds number for a circular duct section.

    This helper is called repeatedly during the pressure-solver and velocity
    updates to determine whether the flow is in the laminar or turbulent regime.
    """
    if abs(viscosity) < 1e-10:
        return 0.0
    return (rho * abs(velocity) * diameter) / viscosity

@njit
def pressure_wave_update(pressure_in, rho, sound_speed, du_dx, dt, damping=0.5):
    """Advance pressure using the linearised 1D wave equation.

    The update treats the pressure evolution as a wave propagation process driven
    by the axial velocity gradient du/dx and scales the result with a damping
    coefficient for numerical stability.
    """
    dpdt = -rho * sound_speed**2 * du_dx
    return pressure_in + damping * dpdt * dt

@njit
def momentum_update(velocity, rho, dp_dx, friction_term, dt, damping=0.5):
    """Advance velocity using the momentum equation with a friction loss term.

    Parameters
    ----------
    velocity : float
        Current longitudinal flow velocity.
    rho : float
        Fluid density.
    dp_dx : float
        Axial pressure gradient.
    friction_term : float
        Pressure-loss term used to represent wall friction.
    dt : float
        Time step size.
    damping : float, optional
        Stabilising factor applied to the explicit update.
    """
    if abs(rho) < 1e-10:
        return velocity
    dudt = -(1.0 / rho) * (dp_dx + friction_term)
    return velocity + damping * dudt * dt

@njit
def orifice_dp_jit(mdot, cd_a, rho):
    """Compute the pressure differential across an orifice-like restriction.

    The relation uses the standard quadratic form for compressible/incompressible
    flow through a restriction, scaled by the discharge coefficient area and
    density. The function returns a scalar pressure drop in pascals.
    """
    if abs(rho) < 1e-10 or abs(cd_a) < 1e-10:
        return 0.0
    return (((mdot*abs(mdot)) / (cd_a**2)) )/ (2 * rho)

@njit
def clamp_value(value, min_val, max_val):
    """Clamp a scalar to a numeric range while preserving safety during JIT execution."""
    return max(min_val, min(max_val, value))

@njit
def update_history_arrays_jit(pressure_history, temp_history, mdot_history, velocity_history,
                             cell_id, pressure, temperature, mdot, velocity, iteration):
    """Store one time-step snapshot into the preallocated history arrays.

    This helper provides the low-level write path used by component recorders to
    update per-cell historical values without Python-level loops.
    """
    if cell_id >= 0 and iteration < pressure_history.shape[1] and cell_id < pressure_history.shape[0]:
        pressure_history[cell_id, iteration] = pressure
        temp_history[cell_id, iteration] = temperature
        mdot_history[cell_id, iteration] = mdot
        velocity_history[cell_id, iteration] = velocity