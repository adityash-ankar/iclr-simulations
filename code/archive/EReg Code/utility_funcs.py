from typing import List, Optional
from scipy.optimize import root_scalar, fsolve
from pyfluids import Fluid, FluidsList, Input
from thermo.chemical import Chemical
from os import system 
import numpy as np
import csv
import os
from numba import jit, njit, prange
from numba.types import float64

import cProfile

# JIT-compiled utility functions for maximum performance
@njit
def friction_factor_laminar(re):
    """Laminar flow friction factor - JIT compiled"""
    return 64.0 / abs(re) if abs(re) > 1e-10 else 0.0

@njit
def friction_factor_turbulent_approx(re, roughness_ratio):
    """Approximate turbulent friction factor (Swamee-Jain) - JIT compiled"""
    re_abs = abs(re)
    if re_abs < 1e-10:
        return 0.0
    return 1.325 / (np.log((roughness_ratio / 3.7) + (5.74 / re_abs ** 0.9))) ** 2

@njit
def calculate_friction_factor(re, roughness, diameter):
    """Fast friction factor calculation - JIT compiled"""
    roughness_ratio = roughness / diameter
    if abs(re) < 3000:
        return friction_factor_laminar(re)
    else:
        return friction_factor_turbulent_approx(re, roughness_ratio)

@njit
def darcy_weisbach_jit(friction_factor, length, diameter, rho, velocity):
    """JIT-compiled Darcy-Weisbach equation"""
    return friction_factor * (length / diameter) * (rho * velocity * abs(velocity)) / 2

@njit
def reynolds_number_jit(rho, velocity, diameter, viscosity):
    """JIT-compiled Reynolds number calculation"""
    if abs(viscosity) < 1e-10:
        return 0.0
    return (rho * abs(velocity) * diameter) / viscosity

@njit
def pressure_wave_update(pressure_in, rho, sound_speed, du_dx, dt, damping=0.5):
    """JIT-compiled pressure wave equation"""
    dpdt = -rho * sound_speed**2 * du_dx
    return pressure_in + damping * dpdt * dt

@njit
def momentum_update(velocity, rho, dp_dx, friction_term, dt, damping=0.5):
    """JIT-compiled momentum equation"""
    if abs(rho) < 1e-10:
        return velocity
    dudt = -(1.0 / rho) * (dp_dx + friction_term)
    return velocity + damping * dudt * dt

@njit
def orifice_dp_jit(mdot, cd_a, rho):
    """JIT-compiled orifice pressure drop calculation"""
    if abs(rho) < 1e-10 or abs(cd_a) < 1e-10:
        return 0.0
    return (((mdot*abs(mdot)) / (cd_a**2)) )/ (2 * rho)

@njit
def clamp_value(value, min_val, max_val):
    """JIT-compiled value clamping"""
    return max(min_val, min(max_val, value))

@njit
def update_history_arrays_jit(pressure_history, temp_history, mdot_history, velocity_history,
                             cell_id, pressure, temperature, mdot, velocity, iteration):
    """JIT-compiled efficient array update"""
    if cell_id >= 0 and iteration < pressure_history.shape[1] and cell_id < pressure_history.shape[0]:
        pressure_history[cell_id, iteration] = pressure
        temp_history[cell_id, iteration] = temperature
        mdot_history[cell_id, iteration] = mdot
        velocity_history[cell_id, iteration] = velocity