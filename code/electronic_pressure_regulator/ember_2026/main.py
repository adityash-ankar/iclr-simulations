"""
Main runner for the electronic_pressure_regulator package.

Provides a lightweight example of building and running a feed-system
simulation pipeline using JIT-accelerated component classes. Inputs:
- fluid: a pyfluids Fluid instance configured with temperature & pressure
- feed system parameters (dt, N, mdot, inlet/outlet pressures)
Outputs:
- Console log of progress and stability checks
- CSV files written to an output folder containing pressure, massflow
  and temperature histories.
Use this script to validate and profile the package on small test cases.
"""

import numpy as np
from component_classes.feed_system_critical_path import (
    FeedSystemCriticalPath,
)

from component_classes.ereg_component 
from pyfluids import Fluid, FluidsList, Input
from util_funcs import *



def thetaToCd(valve_angle):
        """
        Function to return Orifice Cd based on Valve Angle. 
        """
        Cd = 0.50 + 0.50 * (valve_angle/90)**2
        return Cd


def bar2Pa(bar):
    """Convert pressure from bar to Pascals."""
    return bar * 1e5



def ereg_controller(prop_press_setpoint, prop_press_reading, n2_press_reading):
    pass

if __name__ == "__main__":
    pass


