"""
Pipe component implementations and JIT-accelerated solvers.

This module provides PipeJIT which models compressible flow along a
pipe segment using simplified pressure-wave and momentum updates. Inputs
include previous/next boundary velocities and pressures, fluid state
and geometric parameters. Outputs are updated pressureIn, mdot and
u_iterate (velocity estimate). The computationally intensive core is
JIT-compiled to improve loop performance inside FeedSystemCriticalPath.
"""

import numpy as np
from numba import njit
from pyfluids import Fluid, Input
from scipy.optimize import root_scalar
from util_funcs import *

from component_classes.system_component import (
    systemComponentJIT,
)


class PipeJIT(systemComponentJIT):
    """
    Pipe segment model implementing JIT-accelerated numerical updates.

    The class exposes solve_jit(prevVelocity, nextPressure, dt) which
    updates local pressure and velocity using a JIT-compiled numerical
    kernel. Inputs: prevVelocity, nextPressure, dt and internal fluid
    properties. Outputs: updated pressureIn, u_iterate, mdot and density.
    Intended for use as the basic discretised element inside
    FeedSystemCriticalPath.
    """
    def __init__(self, fluid: Fluid=None, length=1.0, diameter=0.1, roughness=0.0001, location=0, pos=None,
                 pressureIn=0, pressureOut=0, temp=None, rho=None, mdot=None):
        """Initialise a pipe element with geometry and per-cell state.

        Parameters
        ----------
        fluid : pyfluids.Fluid or None, optional
            Fluid object used to evaluate density and sound speed.
        length : float, optional
            Pipe segment length in metres.
        diameter : float, optional
            Internal pipe diameter in metres.
        roughness : float, optional
            Pipe roughness in metres.
        location : int, optional
            Index of this pipe in the discretized feed system.
        pos : float or None, optional
            Axial position of the segment.
        pressureIn : float, optional
            Inlet pressure in pascals.
        pressureOut : float, optional
            Outlet pressure in pascals.
        temp : float or None, optional
            Temperature in Kelvin.
        rho : float or None, optional
            Density in kg/m^3.
        mdot : float or None, optional
            Mass flow rate in kg/s.

        Returns
        -------
        None
            Initializes the pipe state and geometry.
        """
        super().__init__(type="p", location=location, pressureIn=pressureIn, pressureOut=pressureOut,
                        length=length, pos=pos, temp=temp, fluid=fluid, rho=rho, mdot=mdot)
        self.diameter = diameter
        self.roughness = roughness
        self.Re: float = 0.0

    def getVelocity(self, mdot=None):
        """Convert mass flow into a representative flow speed for this pipe segment."""
        if mdot is None:
            mdot = self.mdot
        if self.rho is None or mdot is None:
            raise ValueError("Density and mass flow rate must be set before calculating velocity.")
        area = np.pi * (self.diameter / 2) ** 2
        self.u_iterate = mdot / (self.rho * area)
        return self.u_iterate

    def solve_jit(self, prevVelocity, nextPressure, dt):
        """Advance the pipe state using the JIT-compiled transient update kernel.

        Parameters
        ----------
        prevVelocity : float
            Velocity from the previous upstream cell.
        nextPressure : float
            Pressure applied at the downstream boundary in pascals.
        dt : float
            Time step duration in seconds.

        Returns
        -------
        None
            Updates the pipe's pressure, velocity, and mass-flow state in place.
        """
        self.fluid.update(Input.temperature(self.temp), Input.pressure(self.pressureIn))
        rho = self.fluid.density
        sound_speed = self.fluid.sound_speed
        viscosity = self.fluid.dynamic_viscosity

        new_pressure, new_velocity, new_mdot = self._solve_numerical_jit(
            self.pressureIn, self.u_iterate, nextPressure,
            rho, sound_speed, viscosity, self.uOut if self.uOut else 0, self.uIn if self.uIn else 0,
            self.length, self.diameter, self.roughness, dt
        )

        self.pressureIn = new_pressure
        self.u_iterate = new_velocity
        self.mdot = new_mdot
        self.rho = rho

        if self.fluid:
            try:
                self.fluid.update(Input.pressure(self.pressureIn), Input.temperature(self.temp))
                self.temp = self.fluid.temperature
                self.rho = self.fluid.density
                self.viscosity = self.fluid.dynamic_viscosity

            except Exception as exc:
                raise ValueError("Failed to update fluid state. Ensure fluid properties are set correctly.") from exc

    @staticmethod
    @njit
    def _solve_numerical_jit(pressure_in, velocity, next_pressure, rho, sound_speed,
                           viscosity, u_out, u_in, length, diameter, roughness, dt):
        """Run the raw JIT-compiled pressure-wave/momentum update for a pipe element.

        Parameters
        ----------
        pressure_in : float
            Current local pressure in pascals.
        velocity : float
            Current local velocity in m/s.
        next_pressure : float
            Downstream boundary pressure in pascals.
        rho : float
            Fluid density in kg/m^3.
        sound_speed : float
            Speed of sound in the fluid in m/s.
        viscosity : float
            Dynamic viscosity in Pa·s.
        u_out : float
            Downstream velocity estimate.
        u_in : float
            Upstream velocity estimate.
        length : float
            Segment length in metres.
        diameter : float
            Internal diameter in metres.
        roughness : float
            Pipe roughness in metres.
        dt : float
            Time step in seconds.

        Returns
        -------
        tuple
            Updated pressure, velocity, and mass flow rate.
        """
        damping_factor = 1

        du_dx = (u_out - u_in) / length
        dp_dx = (next_pressure - pressure_in) / length

        re = reynolds_number_jit(rho, velocity, diameter, viscosity)
        f = calculate_friction_factor(re, roughness, diameter)

        friction_dp_per_length = f * (1.0 / diameter) * (rho * velocity * abs(velocity)) / 2
        dpdt = -rho * sound_speed * sound_speed * du_dx - friction_dp_per_length

        friction_force_per_length = friction_dp_per_length
        dudt = -(1.0 / rho) * (dp_dx + (rho * (u_out)**2 - rho * (u_in)**2) + friction_force_per_length)

        new_pressure = pressure_in + damping_factor * dpdt * dt
        new_velocity = velocity + damping_factor * dudt * dt

        area = np.pi * (diameter / 2)**2
        new_mdot = rho * new_velocity * area
        new_mdot = clamp_value(new_mdot, -1000.0, 1000.0)

        return new_pressure, new_velocity, new_mdot

    def dp(self, pressureIn=None, mdot=None):
        """Estimate the frictional pressure drop for this pipe segment at a given flow state.

        Parameters
        ----------
        pressureIn : float or None, optional
            Inlet pressure to evaluate. If omitted, the current local pressure is used.
        mdot : float or None, optional
            Mass flow rate to evaluate. If omitted, the current stored value is used.

        Returns
        -------
        float
            Estimated pressure loss over the pipe segment in pascals.
        """
        if pressureIn is None:
            pressureIn = self.pressureIn

        if mdot is None:
            mdot = self.mdot

        self.mdot = mdot

        self.fluid.update(Input.pressure(pressureIn), Input.temperature(self.temp))
        self.rho = self.fluid.density
        viscosity = self.fluid.dynamic_viscosity

        velocity = mdot / (self.rho * np.pi * (self.diameter / 2) ** 2)
        re = reynolds_number_jit(self.rho, velocity, self.diameter, viscosity)
        f = calculate_friction_factor(re, self.roughness, self.diameter)
        return darcy_weisbach_jit(f, self.length, self.diameter, self.rho, velocity)

    def solveMdotIter(self, inletPressure=None, outletPressure=None):
        """Update the mass flow rate from the current velocity iterate for the pipe.

        Parameters
        ----------
        inletPressure : float or None, optional
            Inlet pressure used for compatibility with the calling interface.
        outletPressure : float or None, optional
            Outlet pressure used for compatibility with the calling interface.

        Returns
        -------
        None
            Updates the stored mass-flow rate in place from the current velocity.
        """
        self.mdot = self.u_iterate * self.rho * np.pi * (self.diameter / 2) ** 2

    def solveMdot(self, inletPressure=None, outletPressure=None):
        """Solve for the pipe mass flow that matches the target pressure differential.

        Parameters
        ----------
        inletPressure : float or None, optional
            Pressure at the upstream boundary in pascals.
        outletPressure : float or None, optional
            Pressure at the downstream boundary in pascals.

        Returns
        -------
        None
            Updates the pipe mass-flow state in place.
        """
        if inletPressure is None:
            inletPressure = self.pressureIn
        if outletPressure is None:
            outletPressure = self.pressureOut

        dpTarget = inletPressure - outletPressure

        def dpFunc(mdot):
            return self.dp(mdot=mdot) - dpTarget

        brackets_to_try = [[-1, 1], [-10, 10], [-100, 100], [-0.1, 0.1], [0.001, 10], [-10, 0.001]]

        result = None
        for bracket in brackets_to_try:
            try:
                result = root_scalar(dpFunc, bracket=bracket, method='brentq')
                self.mdot = result.root
                break
            except Exception:
                raise ValueError(f"Failed to solve for mass flow rate in bracket {bracket}")

    def solve(self, prevVelocity, nextPressure, dt):
        """Compatibility wrapper that delegates to the JIT-based solver."""
        self.solve_jit(prevVelocity, nextPressure, dt)

    def velfromMdot(self, mdot=None, rho=None):
        """Calculate and store the velocity implied by the given mass flow rate.

        Parameters
        ----------
        mdot : float or None, optional
            Mass flow rate in kg/s. Uses the current value if omitted.
        rho : float or None, optional
            Density in kg/m^3. Uses the fluid density if omitted.

        Returns
        -------
        float
            Updated velocity estimate in m/s.
        """
        if mdot is None:
            mdot = self.mdot
        if rho is None:
            rho = self.fluid.density
        area = np.pi * (self.diameter / 2) ** 2
        uOut = mdot / (rho * area)
        self.u_iterate = uOut