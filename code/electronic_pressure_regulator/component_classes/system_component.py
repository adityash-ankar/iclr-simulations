"""
Core component base class definitions for the electronic_pressure_regulator
component hierarchy.

This module defines systemComponentJIT which stores common state shared
by pipes, orifices and boundary (ghost) cells. Typical inputs are
pressure/temperature/state from a pyfluids Fluid instance, and outputs
are updated state variables (pressureIn, pressureOut, mdot, velocity).
The class provides small helper methods for recording time-history arrays
that the higher-level FeedSystemCriticalPath controller uses.
"""

import math

from pyfluids import Fluid, Input
from util_funcs import *


class systemComponentJIT:
    """
    Lightweight base class for discretised system components.

    Stores canonical per-component state (id, type, pressures, temperature,
    mass flow and velocity-related fields). Expected inputs: initialization
    parameters from the higher-level model (location index, initial
    pressures, pyfluids Fluid object). Methods update internal state and
    provide small utility wrappers used by JIT-enabled recording helpers.

    Typical usage: subclass this for specific physical components
    (PipeJIT, OrificeJIT, ghostCellJIT) and call record_to_arrays_jit to
    persist runtime histories into pre-allocated numpy arrays.
    """
    def __init__(self, type, location=None, pressureIn=None, pressureOut=None, length=None, pos=None,
                 temp=None, fluid=None, rho=None, mdot=None, initP=None, initT=None, initMdot=None):
        """Create a state container shared by all discrete flow elements.

        Parameters
        ----------
        type : str
            Logical component type such as 'p' (pipe), 'o' (orifice), or 'g' (ghost cell).
        location : int or None, optional
            Position index within the discretized network.
        pressureIn : float or None, optional
            Inlet pressure for the component in pascals.
        pressureOut : float or None, optional
            Outlet pressure for the component in pascals.
        length : float or None, optional
            Component length in metres.
        pos : float or None, optional
            Axial position of the component.
        temp : float or None, optional
            Fluid temperature in Kelvin.
        fluid : pyfluids.Fluid or None, optional
            Fluid model associated with the component.
        rho : float or None, optional
            Fluid density in kg/m^3.
        mdot : float or None, optional
            Mass flow rate in kg/s.

        Returns
        -------
        None
            Initializes the core state fields for the component.
        """
        self.id = location
        self.type = type
        self.pos = pos
        self.pressureIn = pressureIn
        self.pressureOut = pressureOut
        self.length = length
        self.temp = temp
        self.fluid: Fluid = fluid
        self.rho = rho
        self.mdot = mdot

        # Legacy lists for backward compatibility
        self.pressureThroughTime = [initP] if initP is not None else []
        self.tempThroughTime = [initT] if initT is not None else []
        self.mdotThroughTime = [initMdot] if initMdot is not None else []
        self.uIn = None
        self.uOut = None
        self.u_iterate = None
        self._fluid_pressure_cache = None
        self._fluid_temp_cache = None

    def _sync_fluid_state(self, pressure=None, temperature=None):
        """Update the attached pyfluids state only when the pressure/temperature values are valid and changed."""
        if self.fluid is None:
            return
        if pressure is None:
            pressure = self.pressureIn
        if temperature is None:
            temperature = self.temp

        pressure = float(pressure)
        temperature = float(temperature)

        if not math.isfinite(pressure):
            pressure = 1e5
        if not math.isfinite(temperature):
            temperature = 0.0

        # Keep the transient update in a region that pyfluids can evaluate reliably.
        pressure = max(pressure, 1e5)
        temperature = max(min(temperature, 200.0), -250.0)

        if self._fluid_pressure_cache != pressure or self._fluid_temp_cache != temperature:
            try:
                self.fluid.update(Input.temperature(temperature), Input.pressure(pressure))
            except ValueError:
                # A transient overshoot can push the fluid state outside a valid thermodynamic window.
                # Keep the last valid cached state instead of crashing the entire solve step.
                return
            self._fluid_pressure_cache = pressure
            self._fluid_temp_cache = temperature

    def record_to_arrays_jit(self, pressure_history, temp_history, mdot_history, velocity_history, iteration):
        """Record this cell's current state into the solver's preallocated arrays."""
        if self.id is not None:
            update_history_arrays_jit(pressure_history, temp_history, mdot_history, velocity_history,
                                     self.id,
                                     self.pressureIn if self.pressureIn is not None else 0,
                                     self.temp if self.temp is not None else 0,
                                     self.mdot if self.mdot is not None else 0,
                                     self.u_iterate if self.u_iterate is not None else 0,
                                     iteration)

    def record_to_arrays(self, pressure_history, temp_history, mdot_history, velocity_history, iteration):
        """Backward-compatible wrapper around the JIT recording routine."""
        self.record_to_arrays_jit(pressure_history, temp_history, mdot_history, velocity_history, iteration)

    # Standard getters/setters
    def getID(self):
        """Return the cell index assigned to this component in the discretized model."""
        return self.id

    def getuIn(self):
        """Return the upstream velocity state stored on this cell."""
        return self.uIn

    def setuIn(self, uIn):
        """Store the upstream velocity estimate used by the finite-volume update."""
        self.uIn = uIn

    def getPos(self):
        """Return the axial position of the component in the feed system."""
        return self.pos

    def getFluid(self):
        """Return the associated pyfluids fluid object for this component."""
        return self.fluid

    def getuOut(self):
        """Return the downstream velocity state stored on this cell."""
        return self.uOut

    def setuOut(self, uOut):
        """Store the downstream velocity estimate for the current time step."""
        self.uOut = uOut

    def setMdot(self, mdot):
        """Set the mass flow rate for the current component."""
        self.mdot = mdot

    def getMdot(self):
        """Return the current mass flow rate on this component."""
        return self.mdot

    def get_u_iterate(self):
        """Return the current iterate of velocity used during the transient solve."""
        return self.u_iterate

    def set_u_iterate(self, u_iterate):
        """Set the current velocity iterate for the component."""
        self.u_iterate = u_iterate

    def getType(self):
        """Return the component type label (for example 'p', 'o', 'oe', or 'g')."""
        return self.type

    def getPressureIn(self):
        """Return the inlet pressure of the component."""
        return self.pressureIn

    def setPressureIn(self, pressureIn):
        """Set the inlet pressure and sync the pyfluids fluid state to match it."""
        self.pressureIn = pressureIn
        if self.fluid is not None:
            self._sync_fluid_state(self.pressureIn, self.temp)

    def getPressureOut(self):
        """Return the outlet pressure of the component."""
        return self.pressureOut

    def setPressureOut(self, pressureOut):
        """Set the outlet pressure and sync the pyfluids fluid state to match it."""
        self.pressureOut = pressureOut
        if self.fluid is not None:
            self._sync_fluid_state(self.pressureOut, self.temp)

    def update(self, nextPressure=None):
        """Refresh the cached fluid properties from the current component state."""
        if self.fluid is not None:
            self._sync_fluid_state(self.pressureIn, self.temp)
            self.rho = self.fluid.density
            self.viscosity = self.fluid.dynamic_viscosity

        if nextPressure:
            self.pressureOut = nextPressure

    def record(self):
        """Append the latest state to the legacy Python list history buffers."""
        self.pressureThroughTime.append(self.pressureIn)
        self.tempThroughTime.append(self.temp)
        self.mdotThroughTime.append(self.mdot)