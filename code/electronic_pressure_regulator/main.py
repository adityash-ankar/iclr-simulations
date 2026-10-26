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
from component_classes.ereg_component import EregJIT
from component_classes.feed_system_critical_path import (
    FeedSystemCriticalPath,
)
from pyfluids import Fluid, FluidsList, Input
from util_funcs import *


def barA(pa):
    """Convert a pressure value from bar to pascals for pyfluids inputs.

    Parameters
    ----------
    pa : float
        Pressure value in bar.

    Returns
    -------
    float
        Pressure value expressed in pascals.
    """
    return pa * 1e5


if __name__ == "__main__":
    print("Starting JIT-optimized simulation...")
    print("Note: First iteration may be slow due to JIT compilation")

    # Example usage with JIT optimization
    fluid = Fluid(FluidsList.Nitrogen)
    # PyFluids' configured unit system uses Celsius for temperature inputs.
    fluid.update(Input.temperature(-5), Input.pressure(barA(300)))
    simTime = 1  # s


    ereg_setpoint = 250

    feed_system = FeedSystemCriticalPath(dt=1e-2, totalPipeLength=  0.5, fluid=fluid, N=5, mdot=2.0,
                                        inletPressure=barA(300), outletPressure=barA(200))


    ereg = EregJIT(
        fluid=fluid,
        location=2,
        pt_location=2,
        pos=2 * feed_system.dL,
        pressureIn=feed_system.discretisedFeed[1].getPressureOut(),
        pressureOut=barA(ereg_setpoint),
        temp=feed_system.initTemp,
        mdot=2.0,
        ID=0.035,
        CdA=194e-6,
        type="e",
    )

    # Replace the second pipe with the regulator.
    feed_system.discretisedFeed[2] = ereg

    dL = feed_system.dL
    initial_velocity = feed_system.discretisedFeed[1].getVelocity()
    sound_speed = fluid.sound_speed

    # Proper CFL condition: dt < dx / (|u| + a)
    cfl_dt = dL / (abs(initial_velocity) + sound_speed)

    # Use a more conservative explicit-step safety factor to keep the transient update bounded.
    dt = 0.4 * cfl_dt
    feed_system.dt = dt
    timeIterations = int(simTime / dt)
    feed_system.setMaxIterations(timeIterations + 100)
    feed_system.initCont()

    print(f"Sim time: {simTime} s, dt: {dt:.2e} s, dL: {dL} m, CFL dt: {cfl_dt:.2e} s")
    print(f"Sound speed: {sound_speed:.1f} m/s, Initial velocity: {initial_velocity:.3f} m/s")
    print(f"{timeIterations} iterations")

    # Print initial pressure distribution
    print("\nInitial pressure distribution:")
    for i, comp in enumerate(feed_system.discretisedFeed):
        if comp.type != 'g':
            print(f"  {comp.type}_{comp.getID()}: {comp.getPressureIn()/1e5:.3f} bar")

    import time as time_module
    start_time = time_module.time()

    print(dt)
    for i in range(timeIterations):
        feed_system.solve()

        # Check for instability every 10 iterations
        if i % 10 == 0 and i > 0:
            max_pressure = np.max(feed_system.pressure_history[:, i])
            min_pressure = np.min(feed_system.pressure_history[:, i])

            if max_pressure > 1e8 or min_pressure < 0:
                print(f"Instability detected at iteration {i}")
                print(f"Max pressure: {max_pressure:.2e} Pa, Min pressure: {min_pressure:.2e} Pa")
                break

        if i > 0 and i % 100 == 0:
            elapsed = time_module.time() - start_time
            progress = i / timeIterations * 100
            estimated_total = elapsed / (i / timeIterations)
            remaining = estimated_total - elapsed
            print(f"Progress: {progress:.1f}% - Elapsed: {elapsed:.1f}s - Remaining: {remaining:.1f}s", end='\r')

        # Print pressure distribution every 1000 iterations for debugging
        if i > 0 and i % 1000 == 0:
            print(f"\nIteration {i} pressure distribution:")
            for j, comp in enumerate(feed_system.discretisedFeed):
                if comp.type != 'g':
                    print(f"  {comp.type}_{comp.getID()}: {comp.getPressureIn()/1e5:.3f} bar")

            print(f"CdA: {feed_system.getCDA()}")

    end_time = time_module.time()
    total_time = end_time - start_time

    print("Progress: 100.00000%")
    print(f"JIT-optimized simulation completed in {total_time:.2f} seconds")
    print(f"Performance: {timeIterations/total_time:.0f} iterations/second")

    output_folder = f"simulation_results_jit_{dt:.2e}_{simTime}"

    # Write CSV files to the new folder
    feed_system.write_to_csv(
        pressure_filename="pressure_results.csv",
        massflow_filename="massflow_results.csv",
        temperature_filename="temperature_results.csv",
        output_dir=output_folder
    )

    print(f"\nJIT-optimized simulation completed. Data written to {output_folder}")
