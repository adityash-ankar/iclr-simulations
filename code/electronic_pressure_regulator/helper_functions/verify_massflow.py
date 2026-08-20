import os
os.environ['PYTHONPATH'] = os.path.join(os.getcwd(), 'code')

from pyfluids import Fluid, FluidsList, Input
from electronic_pressure_regulator.component_classes.feed_system_critical_path import FeedSystemCriticalPath

fluid = Fluid(FluidsList.Oxygen)
# PyFluids is configured for SIWithCelsiusAndPercents, so temperature is in °C.
fluid.update(Input.temperature(-180), Input.pressure(100e5))
fs = FeedSystemCriticalPath(dt=1e-3, totalPipeLength=9.0, fluid=fluid, N=10, mdot=1.0, inletPressure=100e5, outletPressure=80e5)
print('mdot after init', fs.mdot)
print('target dp', fs.inletPressure - fs.outletPressure)
print('system dp at 1', fs.getSystemDP(1.0))
print('system dp at 0.1', fs.getSystemDP(0.1))
print('system dp at 0', fs.getSystemDP(0.0))
fs.solveMdot(fs.inletPressure, fs.outletPressure)
print('solved mdot', fs.mdot)
