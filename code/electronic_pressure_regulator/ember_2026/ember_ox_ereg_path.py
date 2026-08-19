import numpy as np
from component_classes.feed_system_critical_path import (
    FeedSystemCriticalPath,
)
from component_classes.orifice_component import OrificeJIT
from component_classes.pipe_component import (
    PipeJIT,  # noqa: F401
)
from component_classes.system_component import (
    systemComponentJIT,  # noqa: F401
)
from util_funcs import *
from pyfluids import Fluid, FluidsList, Input


def barA(pa):
    """Convert a pressure value from bar to pascals for pyfluids inputs."""
    return pa * 1e5


def OxFeedLine(press_fluid, simTime, ox_fluid=None):
    """Construct a representative oxygen feed-line model and return its transient setup values."""
    ox_cp_pretank = FeedSystemCriticalPath(dt=0.05, totalPipeLength=2.0, fluid=press_fluid, N=40, mdot=3,
                                          inletPressure=barA(300), outletPressure=barA(1.013))
    dL = ox_cp_pretank.dL
    initial_velocity = ox_cp_pretank.discretisedFeed[1].getVelocity()
    sound_speed = press_fluid.sound_speed

    cfl_dt = dL / (abs(initial_velocity) + sound_speed)

    dt = 0.67 * cfl_dt
    ox_cp_pretank.dt = dt
    timeIterations = int(simTime / dt)
    ox_cp_pretank.setMaxIterations(timeIterations * 1.2)
    ox_cp_pretank.initCont()

    return ox_cp_pretank, timeIterations, initial_velocity, cfl_dt, dt


def ereg_orifice(feed: FeedSystemCriticalPath, orifice_OD, orifice_ID, orifice_Location, orifice_position, iteration,
                ereg_mdot, valve_angle, CdA_max):
    """Create an orifice object representing the regulator valve at a specific feed-system location."""
    ereg_orifice = OrificeJIT(
        fluid=feed.fluid,
        OD=orifice_OD,
        ID=orifice_ID,
        location=orifice_Location,
        pos=orifice_position,
        pressureIn=feed.pressure_history[orifice_Location - 1, iteration],
        pressureOut=feed.pressure_history[orifice_Location + 1, iteration],
        temp=feed.initTemp,
        mdot=ereg_mdot,
        type='o',
        CdA=get_nd_CdA(valve_angle, CdA_max)
    )


def get_nd_CdA(theta):
    """Map a valve angle to a normalized discharge coefficient area using a polynomial fit."""
    theta = np.clip(theta, 0, 90)
    return (0.494 * (theta / 90) + 1.995 * (theta / 90) ** 2 - 6.942 * (theta / 90) ** 3 +
            8.870 * (theta / 90) ** 4 - 3.416 * (theta / 90) ** 5)


def calc_ereg_mdot(time_step=1):
    """Return the current estimated regulator mass-flow demand for a given time step."""
    ereg_mdot = 3
    return ereg_mdot


if __name__ == "__main__":
    n2_tank_pressure = barA(400)
    n2_fluid = Fluid(FluidsList.Nitrogen)
    n2_fluid.update(Input.temperature(-5), Input.pressure(n2_tank_pressure))
    simTime = 60
    sound_speed = n2_fluid.sound_speed
    feed_system, timeIterations, initial_velocity, cfl_dt, dt = OxFeedLine(
        press_fluid= n2_fluid,
        simTime= simTime

    )

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
            print(f"Progress: {progress:.1f}% - Elapsed: {elapsed:.1f}s - Remaining: {remaining:.1f}s", end ='\r')

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