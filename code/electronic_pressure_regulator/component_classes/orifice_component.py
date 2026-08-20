
"""
Orifice component implementation for the discretised feed system.

Provides OrificeJIT, a subclass of systemComponentJIT, which computes
orifice pressure drops and solves for mass flow given inlet/outlet
pressures. Inputs: fluid state (pyfluids Fluid), geometry (ID/OD/CdA)
and boundary pressures. Outputs: mdot and updated pressureOut. The
module is designed to work inside FeedSystemCriticalPath and uses JIT
utility functions from util_funcs for the core physics kernels.
"""

import numpy as np  # noqa: I001
from pyfluids import Fluid, Input
from scipy.optimize import root_scalar
from util_funcs import *

from component_classes.system_component import (
    systemComponentJIT,
)


class OrificeJIT(systemComponentJIT):
    """
    Orifice element representing a localized flow restriction.

    Responsibilities:
    - Compute dp across an orifice for a given mdot (and vice-versa)
    - Support time-varying CdA (dynamic orifice models)

    Inputs: inlet/outlet pressures, temperature, Fluid object, geometry
    parameters (inner/outer diameters, length, CdA). Outputs: mdot and
    updated local pressures (pressureOut). Use within the FeedSystem
    controller where solveMdot/solve methods are called each timestep.
    """
    def __init__(self, fluid: Fluid | None, OD: float = 0.05, ID: float = 0.04, location: int = 0,
                 pos=None, pressureIn: float = 0.0, pressureOut: float = 0.0,
                 temp=None, rho=None, mdot=None, l: float = 0.01, CdA=None, type: str = 'o'):
        """Create an orifice restriction with a configurable discharge coefficient area.

        Parameters
        ----------
        fluid : pyfluids.Fluid
            Fluid model used to evaluate density and pressure states.
        OD : float, optional
            Outer diameter of the orifice in metres.
        ID : float, optional
            Inner diameter of the orifice in metres.
        location : int, optional
            Discrete index of the orifice in the system grid.
        pos : float or None, optional
            Axial position of the orifice.
        pressureIn : float, optional
            Upstream pressure in pascals.
        pressureOut : float, optional
            Downstream pressure in pascals.
        temp : float or None, optional
            Fluid temperature in Kelvin.
        rho : float or None, optional
            Density in kg/m^3.
        mdot : float or None, optional
            Initial mass-flow estimate in kg/s.
        l : float, optional
            Orifice length in metres.
        CdA : float or None, optional
            Discharge coefficient area in m^2.
        type : str, optional
            Component label, typically 'o' for standard orifice or 'oe' for exit orifice.

        Returns
        -------
        None
            Initializes the local orifice geometry and state.
        """
        super().__init__(type=type, location=location, pos=pos, pressureIn=pressureIn, pressureOut=pressureOut,
                        temp=temp, rho=rho, mdot=mdot, fluid=fluid)
        self.outerD = OD
        self.innerD = ID
        self.length = l
        self.pressureOut = pressureOut
        self.dynamic = False
        self.CdAList = [194e-6, 0] if CdA is None else CdA
        self.CdA = CdA
        self.iteration = 0
        self.constPOut = pressureOut
        self.e = 1/861
        if self.dynamic:
            self.CdA_dict = {iter_index: cdA_value for cdA_value, iter_index in self.CdAList}
        else:
            self.CdA_dict = {}

    def setCdAList(self, CdAList):
        """Configure a time-varying CdA schedule used for valve or ramp actuation.

        Parameters
        ----------
        CdAList : list of tuple
            Sequence of (CdA_value, iteration_index) pairs defining the schedule.

        Returns
        -------
        None
            Updates the orifice's active discharge coefficient schedule.
        """
        self.CdAList = CdAList
        self.dynamic = True
        self.CdA_dict = {iter_index: cdA_value for cdA_value, iter_index in CdAList}
        self.CdA = CdAList[0][0]

    def getVelocity(self):
        """Return the orifice flow velocity implied by the current mass flow and density.

        Returns
        -------
        float
            Flow velocity in metres per second computed from the current mass flow and density.
        """
        if self.rho is None or self.mdot is None:
            raise ValueError("Density and mass flow rate must be set before calculating velocity.")
        area = np.pi * (self.innerD / 2) ** 2
        self.u_iterate = self.mdot / (self.rho * area)
        return self.u_iterate

    def dp(self, pressureIn=None, mdot=None):
        """Compute the pressure drop corresponding to the current mass-flow state.

        Parameters
        ----------
        pressureIn : float or None, optional
            Inlet pressure in pascals. Uses the current value if omitted.
        mdot : float or None, optional
            Mass-flow value in kg/s. Uses the stored value if omitted.

        Returns
        -------
        float
            Pressure drop across the orifice in pascals.
        """
        if pressureIn is None:
            pressureIn = self.pressureIn
        if mdot is not None:
            self.mdot = mdot

        if self.fluid:
            self.fluid.update(Input.pressure(float(pressureIn)), Input.temperature(float(self.temp or 0.0)))
            self.rho = self.fluid.density

        return orifice_dp_jit(self.mdot, self.CdA, self.rho)

    def solveMdotIter(self, inletPressure=None, outletPressure=None):
        """Solve for mass flow using the iterative approach applied during transient stepping.

        Parameters
        ----------
        inletPressure : float or None, optional
            Upstream pressure to use for the solve.
        outletPressure : float or None, optional
            Downstream pressure to use for the solve.

        Returns
        -------
        None
            Updates the orifice mass-flow state in place.
        """
        self.solveMdot()

    def solveMdot(self, inletPressure=None, outletPressure=None):
        """Determine the mass flow that satisfies the pressure-drop target across the orifice.

        Parameters
        ----------
        inletPressure : float or None, optional
            Pressure at the upstream boundary in pascals.
        outletPressure : float or None, optional
            Pressure at the downstream boundary in pascals.

        Returns
        -------
        None
            Sets the internal mass flow rate to the root found for the target pressure differential.
        """
        if inletPressure is None:
            inletPressure = self.pressureIn
        if outletPressure is None:
            outletPressure = self.pressureOut

        targetDp = abs(float(inletPressure) - float(outletPressure))
        if targetDp <= 0.0:
            self.mdot = 0.0
            return

        direction = 1.0 if float(inletPressure) >= float(outletPressure) else -1.0

        def dpFunc(mdot_mag):
            mdot_mag = float(mdot_mag)
            if not np.isfinite(mdot_mag) or mdot_mag <= 0.0:
                return 1e30
            return self.dp(mdot=mdot_mag) - targetDp

        brackets_to_try = [[1e-9, 1e-3], [1e-4, 1e-1], [1e-3, 1.0], [1e-2, 10.0], [1e-2, 100.0], [1e-3, 1000.0]]

        root_value: float | None = None
        for bracket in brackets_to_try:
            try:
                lo, hi = bracket
                f_lo = dpFunc(lo)
                f_hi = dpFunc(hi)
                if not np.isfinite(f_lo) or not np.isfinite(f_hi):
                    continue
                if f_lo == 0.0:
                    root_value = float(lo)
                    break
                if f_hi == 0.0:
                    root_value = float(hi)
                    break
                if f_lo * f_hi < 0:
                    result = root_scalar(dpFunc, bracket=bracket, method='brentq')
                    if result.converged:
                        root_value = float(result.root)
                        break
            except ValueError:
                continue

        if root_value is None:
            candidates = np.geomspace(1e-9, 1e3, 400)
            best_value = None
            best_mdot = 0.0
            for cand in candidates:
                val = abs(dpFunc(cand))
                if best_value is None or val < best_value:
                    best_value = val
                    best_mdot = float(cand)
            self.mdot = direction * best_mdot
            return

        self.mdot = direction * root_value

    def setMdot(self, mdot):
        """Set the mass flow rate on the orifice without modifying its geometry.

        Parameters
        ----------
        mdot : float
            Mass-flow value in kg/s to assign to the orifice.

        Returns
        -------
        None
            Updates the stored mass-flow rate.
        """
        self.mdot = mdot

    def getCDA(self):
        """Return the active discharge coefficient area used by the orifice model.

        Returns
        -------
        float
            Current discharge coefficient area in m^2.
        """
        return self.CdA

    def solve(self, prevPressure, nextCell=None, prevCell=None):
        """Update inlet/outlet pressures and transient velocity based on the local pressure drop.

        Parameters
        ----------
        prevPressure : float
            Upstream pressure in pascals for the current orifice.
        nextCell : object or None, optional
            Downstream neighboring cell that receives the updated outlet pressure.
        prevCell : object or None, optional
            Upstream neighboring cell used for propagation with dynamic orifice updates.

        Returns
        -------
        None
            Updates internal pressure, velocity, and mass-flow state in place.
        """
        self.pressureIn = prevPressure
        self.update()
        self.pressureOut = self.pressureIn - self.dp()
        self.getVelocity()
        if self.dynamic:
            self.iteration += 1
            if self.iteration in self.CdA_dict:
                self.CdA = self.CdA_dict[self.iteration]
            if prevCell is not None:
                prevCell.velfromMdot(self.mdot, self.rho)

        if nextCell is not None:
            nextCell.setPressureIn(self.pressureOut)

    def record_to_arrays_jit(self, pressure_history, temp_history, mdot_history, velocity_history, iteration):
        """Record both inlet and outlet pressures for orifice cells in the history arrays."""
        if self.id is not None:
            update_history_arrays_jit(pressure_history, temp_history, mdot_history, velocity_history,
                                     self.id,
                                     self.pressureIn if self.pressureIn is not None else 0,
                                     self.temp if self.temp is not None else 0,
                                     self.mdot if self.mdot is not None else 0,
                                     self.u_iterate if self.u_iterate is not None else 0,
                                     iteration)
            update_history_arrays_jit(pressure_history, temp_history, mdot_history, velocity_history,
                                     self.id + 1,
                                     self.pressureOut if self.pressureOut is not None else 0,
                                     self.temp if self.temp is not None else 0,
                                     self.mdot if self.mdot is not None else 0,
                                     self.u_iterate if self.u_iterate is not None else 0,
                                     iteration)
