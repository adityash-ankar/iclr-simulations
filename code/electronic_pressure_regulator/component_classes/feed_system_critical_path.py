"""
High-level controller for discretised feed-system simulation.

FeedSystemCriticalPath coordinates pipes, orifices and ghost cells to
simulate transient flow and pressure histories. Inputs: model
configuration (dt, totalPipeLength, N, fluid instance, inlet/outlet
pressures, optional extra components). Outputs: time-history numpy
arrays (pressure, temperature, mdot, velocity) and convenience methods
to write CSVs or extract per-cell data for post-processing.
"""

import csv
import os
from typing import cast

import numpy as np
from component_classes.ghost_cell import ghostCellJIT
from component_classes.orifice_component import OrificeJIT
from component_classes.pipe_component import PipeJIT
from pyfluids import Fluid, Input
from scipy.optimize import root_scalar
from util_funcs import *


class FeedSystemCriticalPath:
    """
    Controller that assembles and advances a discretised feed system.

    Responsibilities:
    - Build a list of components (PipeJIT, OrificeJIT, ghostCellJIT) from
      geometric and component specifications.
    - Advance the simulation through time using component solve methods
      and JIT-accelerated kernels.

    Inputs: dt, totalPipeLength, pyfluids Fluid instance, N, mdot,
    inlet/outlet pressures and optional extraComponents list.
    Outputs: populated arrays (pressure_history, temp_history,
    mdot_history, velocity_history) which can be written to CSV via
    write_to_csv or queried per-cell with get_cell_data.
    """
    def __init__(self, dt: float = 1, totalPipeLength: float = 1.0, fluid: Fluid | None = None,
                 N: int = 2, extraComponents: list[list[float | None]] | None = None,
                 mdot: float | None = None, inletPressure: float | None = None, outletPressure: float | None = None,
                 max_iterations: int = 100000, mdot_update_interval: int = 10):
        """Create the discretized feed system and initialize the pressure history arrays.

        Parameters
        ----------
        dt : float, optional
            Time-step size in seconds.
        totalPipeLength : float, optional
            Total axial length of the modeled feed system in metres.
        fluid : pyfluids.Fluid or None, optional
            Fluid model used across all pipe and orifice elements.
        N : int, optional
            Number of pipe segments in the discretized domain.
        extraComponents : list of tuples, optional
            Optional user-specified component locations and metadata.
        mdot : float or None, optional
            Initial mass-flow estimate in kg/s.
        inletPressure : float or None, optional
            Upstream boundary pressure in pascals.
        outletPressure : float or None, optional
            Downstream boundary pressure in pascals.
        max_iterations : int, optional
            Maximum time-step capacity of the history arrays.

        Returns
        -------
        None
            Initializes the discretized feed-system model and preallocates history buffers.
        """
        if fluid is None:
            raise ValueError("A pyfluids Fluid instance is required to initialize FeedSystemCriticalPath.")
        if N <= 0:
            raise ValueError("N must be positive.")
        if totalPipeLength <= 0:
            raise ValueError("totalPipeLength must be positive.")
        if dt <= 0:
            raise ValueError("dt must be positive.")

        self.N = N
        self.dL = totalPipeLength / N
        self.totalPipeLength = totalPipeLength
        self.inletPressure = 100e5 if inletPressure is None else float(inletPressure)
        self.outletPressure = 80e5 if outletPressure is None else float(outletPressure)
        if extraComponents is None:
            extraComponents = [[None, None], [None, None]]
        self.extraComponents = extraComponents
        self.fluid = fluid
        self.mdot = 1.0 if mdot is None else float(mdot)
        self.dt = float(dt)
        self.max_iterations = max_iterations
        self.mdot_update_interval = int(mdot_update_interval)
        self.current_iteration = 0
        self.rampStartCDA = 194e-6  # Initial CdA value
        self.pressure_history = np.zeros((N + 3, max_iterations))
        self.temp_history = np.zeros((N + 3, max_iterations))
        self.mdot_history = np.zeros((N + 3, max_iterations))
        self.velocity_history = np.zeros((N + 3, max_iterations))

        # PyFluids is configured for SIWithCelsiusAndPercents, so temperature inputs are
        # interpreted in degrees Celsius and converted internally to SI.
        self.initTemp = -180.0
        self.fluid.update(Input.temperature(self.initTemp), Input.pressure(self.inletPressure))
        self.initTemp = self.fluid.temperature
        self.populate()

    def getCDA(self):
        """Return the active discharge coefficient area of the exit orifice."""
        return self.discretisedFeed[-1].getCDA()

    def initCont(self):
        """Configure the exit-orifice CdA ramp as a time-dependent discharge schedule.

        Parameters
        ----------
        None
            This method reads the feed-system configuration and its stored ramp baseline.

        Returns
        -------
        None
            Sets the dynamic discharge coefficient schedule on the exit orifice.
        """
        rampStartTime = 0.05
        rampTime = 0.1
        rampStartCDA = self.rampStartCDA
        rampEndCDA = 50e-6
        rampNum = np.linspace(rampStartCDA, rampEndCDA, int(rampTime / self.dt))
        self.CdAList = []
        for i in range(len(rampNum)):
            self.CdAList.append((rampNum[i], i + int(rampStartTime / self.dt)))
        self.discretisedFeed[-1].setCdAList(self.CdAList)

    def setMaxIterations(self, max_iterations):
        """Reallocate the history arrays to a new maximum time-step count.

        Parameters
        ----------
        max_iterations : int
            New number of time steps to reserve in the stored histories.

        Returns
        -------
        None
            Resets the internal pressure, temperature, mass-flow, and velocity arrays.
        """
        self.max_iterations = max_iterations
        self.pressure_history = np.zeros((self.N + 3, max_iterations))
        self.temp_history = np.zeros((self.N + 3, max_iterations))
        self.mdot_history = np.zeros((self.N + 3, max_iterations))
        self.velocity_history = np.zeros((self.N + 3, max_iterations))

    def discretise(self):
        """Construct the pipe-based discretization for the feed system and extra components.

        Parameters
        ----------
        None
            Uses the configured pipe count, pipe length, and extra component list.

        Returns
        -------
        None
            Populates the discretised feed-system list with pipe objects.
        """
        self.discretisedFeed = []
        valid_extra: list[list[float]] = []
        for comp in self.extraComponents:
            if not comp:
                continue
            component_position = comp[0]
            component_index = comp[1]
            if component_position is None or component_index is None:
                continue
            valid_extra.append([float(component_position), float(component_index)])
        for comp in valid_extra:
            component_index = cast(float, comp[1])
            comp[1] = round(component_index / self.dL)

        if valid_extra:
            valid_extra.sort(key=lambda comp: cast(float, comp[0]))
            self.extraComponents = cast(list[list[float | None]], valid_extra)

        count = 0
        for i in range(self.N):
            pos = count * self.dL
            if i in [int(cast(float, comp[1])) for comp in valid_extra]:
                continue
            count += 1
            pipe: PipeJIT | None = PipeJIT(fluid=self.fluid, length=self.dL, mdot=self.mdot, pos=pos,
                                          location=i + 1, temp=self.initTemp, diameter=0.035)
            self.discretisedFeed.append(pipe)

    def populate(self):
        """Build the initial discretized feed-system state with inlet/outlet orifices and boundary ghosts.

        Parameters
        ----------
        None
            Uses the already-configured inlet/outlet pressures and fluid model.

        Returns
        -------
        None
            Creates the initial physical and ghost-cell state for the model.
        """
        currentPressure = self.inletPressure
        self.discretise()
        self.discretisedFeed.append(OrificeJIT(location=self.N + 1, CdA=self.rampStartCDA, fluid=self.fluid, ID=0.035,
                                              pos=self.totalPipeLength,
                                              pressureIn=float(self.discretisedFeed[-1].getPressureOut()),
                                              pressureOut=float(self.outletPressure), temp=self.initTemp,
                                              mdot=self.mdot, type="oe"))
        self.solveMdot(self.inletPressure, self.outletPressure)
        print(self.mdot)
        for i, component in enumerate(self.discretisedFeed):
            if component.type == "p":
                component.pressureIn = currentPressure
                dp = component.dp(currentPressure, self.mdot)
                currentPressure -= dp
                component.pressureOut = currentPressure
                print(f"Pipe {i}: Pin={component.pressureIn/1e5:.2f} bar, Pout={component.pressureOut/1e5:.2f} bar, dp={dp/1e5:.4f} bar")
            elif component.type == "o":
                component.pressureIn = self.inletPressure
                component.pressureOut = self.outletPressure
            elif component.type == "oe":
                component.pressureIn = currentPressure
                component.pressureOut = self.outletPressure
                dp = component.dp(currentPressure, self.mdot)
                print(f"Orifice: Pin={component.pressureIn/1e5:.2f} bar, Pout={component.pressureOut/1e5:.2f} bar, dp={dp/1e5:.4f} bar")
            else:
                raise ValueError(f"Unknown component type: {component.type}")

        self.discretisedFeed.insert(0, ghostCellJIT(location=0, u=self.discretisedFeed[0].getVelocity(), pos=0,
                                                   pressureIn=self.inletPressure, pressureOut=self.inletPressure,
                                                   mdot=self.mdot, temp=self.initTemp))
        self.boundaryPopulation()

    def getSystemDP(self, mdot):
        """Sum the pressure losses across all active physical cells for a trial mass flow.

        Parameters
        ----------
        mdot : float
            Mass-flow trial value in kg/s used to estimate the system pressure drop.

        Returns
        -------
        float
            Total pressure loss across the discretized system for the provided mass flow.
        """
        trial_mdot = abs(float(mdot))
        return sum(comp.dp(mdot=trial_mdot, pressureIn=self.inletPressure) for comp in self.discretisedFeed if comp.getType() != "g")

    def solveMdot(self, inletPressure: float | None = None, outletPressure: float | None = None):
        """Solve for the steady feed-system mass flow that balances the total pressure drop.

        Parameters
        ----------
        inletPressure : float or None, optional
            Upstream pressure in pascals. Defaults to the configured system inlet pressure.
        outletPressure : float or None, optional
            Downstream pressure in pascals. Defaults to the configured system outlet pressure.

        Returns
        -------
        None
            Updates the feed-system mass flow rate in place to match the target differential pressure.
        """
        if inletPressure is None:
            inletPressure = self.inletPressure
        if outletPressure is None:
            outletPressure = self.outletPressure

        inletPressure = max(float(inletPressure), 1e3)
        outletPressure = max(float(outletPressure), 1e3)

        dpTarget = abs(float(inletPressure) - float(outletPressure))
        if dpTarget <= 0.0:
            self.mdot = 0.0
            return

        direction = 1.0 if float(inletPressure) >= float(outletPressure) else -1.0
        max_mdot = 1e3
        max_dp = self.getSystemDP(max_mdot)
        if np.isfinite(max_dp) and max_dp < dpTarget:
            self.mdot = direction * max_mdot
            return

        def dpFunc(mdot_mag):
            mdot_mag = float(mdot_mag)
            if not np.isfinite(mdot_mag) or mdot_mag <= 0.0:
                return 1e30
            return self.getSystemDP(mdot_mag) - dpTarget

        brackets_to_try = [[1e-9, 1e-3], [1e-4, 1e-1], [1e-3, 1.0], [1e-2, 10.0], [1e-2, 100.0], [1e-3, 1000.0]]

        root_value: float | None = None
        result = None
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
                    if result is not None and result.converged:
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
            if best_value is None:
                raise ValueError("Failed to solve for mass flow rate with any method.")
            self.mdot = direction * best_mdot
            return

        self.mdot = direction * root_value

    def boundaryPopulation(self):
        """Initialize the ghost-cell boundary velocities from the adjacent physical states.

        Parameters
        ----------
        None
            Uses the current discretized component velocities to populate boundary values.

        Returns
        -------
        None
            Sets the start-of-domain and end-of-domain velocity states for the solver.
        """
        for i, component in enumerate(self.discretisedFeed):
            if component.type == "g" or component.type == "oe":
                continue
            cellV = component.getVelocity()

            if cellV < 0:
                component.setuIn(cellV)
                component.setuOut(self.discretisedFeed[i+1].getVelocity())
            else:
                component.setuIn(self.discretisedFeed[i-1].getVelocity())
                component.setuOut(cellV)

            component.record()

    def solve(self):
        """Advance the full discretized feed system by one time step using component updates.

        Parameters
        ----------
        None
            Uses the current system states and the configured time step.

        Returns
        -------
        None
            Updates the full transient state of the feed system and records the new history point.
        """
        feed = self.discretisedFeed
        feed[0].setPressureIn(self.inletPressure)

        for i, component in enumerate(feed):
            if component.type == "g":
                ghost = component
                if i == 0:
                    ghost.setPressureIn(self.inletPressure)
                    ghost.setPressureOut(self.inletPressure)
                    ghost.setuIn(feed[i + 1].getuIn())
                    ghost.setuOut(feed[i + 1].getuIn())
                    ghost.set_u_iterate(feed[i + 1].get_u_iterate())
                elif i == len(feed) - 1:
                    ghost.setPressureIn(self.outletPressure)
                    ghost.setPressureOut(self.outletPressure)
                    ghost.setuIn(feed[i - 1].getuOut())
                    ghost.setuOut(feed[i - 1].getuOut())
                    ghost.set_u_iterate(feed[i - 1].get_u_iterate())
                continue

            if component.type == "e":
                ereg = component
                ereg.solve(feed[i - 1].getPressureOut(), feed[i + 1], feed[i - 1])
                self.upWinding(ereg, feed[i - 1], feed[i + 1])
            elif component.type == "oe":
                orifice = component
                orifice.solve(feed[i - 1].getPressureOut(), prevCell=feed[i - 1])
            elif component.type == "o":
                orifice = component
                orifice.solve(feed[i - 1].getPressureOut(), feed[i + 1])
                self.upWinding(orifice, feed[i - 1], feed[i + 1])
            else:
                pipe = component
                prev_velocity = feed[i - 1].get_u_iterate() if i > 0 else 0.0
                next_pressure = feed[i + 1].getPressureIn() if i < len(feed) - 1 else self.outletPressure
                pipe.solve_jit(prev_velocity, next_pressure, self.dt)
                self.upWinding(pipe, feed[i - 1], feed[i + 1])

        for i, component in enumerate(feed):
            if component.type == "g":
                continue

            if component.type in ("e", "oe"):
                component.solveMdot(inletPressure=feed[i - 1].getPressureOut())
            else:
                component.solveMdotIter()
            component.record_to_arrays_jit(self.pressure_history, self.temp_history,
                                          self.mdot_history, self.velocity_history,
                                          self.current_iteration)

        if self.current_iteration % self.mdot_update_interval == 0:
            self.solveMdot(self.inletPressure, self.outletPressure)

        feed[-2].velfromMdot(mdot=self.mdot, rho=feed[-2].getFluid().density)
        self.current_iteration += 1

    def upWinding(self, current, previous, next):
        """Propagate the updated cell velocity to neighboring cells using the current flow direction.

        Parameters
        ----------
        current : PipeJIT or OrificeJIT
            Component whose velocity has just been updated.
        previous : systemComponentJIT
            Upstream neighboring cell.
        next : systemComponentJIT
            Downstream neighboring cell.

        Returns
        -------
        None
            Updates the upstream/downstream velocity states on the current cell.
        """
        cellV = current.get_u_iterate()
        if cellV >= 0:
            current.setuIn(previous.get_u_iterate())
            current.setuOut(cellV)
        else:
            current.setuIn(cellV)
            current.setuOut(next.get_u_iterate())

    def get_cell_data(self, cell_id, up_to_iteration=None):
        """Return the time-history arrays for a given discretization cell.

        Parameters
        ----------
        cell_id : int
            Index of the cell to retrieve.
        up_to_iteration : int or None, optional
            Maximum time-step index to include. Defaults to the current solver iteration.

        Returns
        -------
        dict
            Dictionary containing pressure, temperature, mass-flow, and velocity histories for the cell.
        """
        if up_to_iteration is None:
            up_to_iteration = self.current_iteration

        return {
            'pressure': self.pressure_history[cell_id, :up_to_iteration],
            'temperature': self.temp_history[cell_id, :up_to_iteration],
            'mdot': self.mdot_history[cell_id, :up_to_iteration],
            'velocity': self.velocity_history[cell_id, :up_to_iteration]
        }

    def get_final_snapshot(self):
        """Return the latest per-cell state at the last completed time iteration.

        Parameters
        ----------
        None
            Uses the most recently completed time-step index.

        Returns
        -------
        dict
            Per-cell snapshot of pressure, temperature, mass flow, and velocity at the final iteration.
        """
        final_iter = self.current_iteration - 1
        return {
            'pressure': self.pressure_history[:, final_iter],
            'temperature': self.temp_history[:, final_iter],
            'mdot': self.mdot_history[:, final_iter],
            'velocity': self.velocity_history[:, final_iter]
        }

    def write_to_csv(self, pressure_filename="pressure_data.csv", massflow_filename="massflow_data.csv",
                     temperature_filename="temperature_results.csv", output_dir="simulation_results"):
        """Export the stored transients to CSV files together with summary metadata.

        Parameters
        ----------
        pressure_filename : str, optional
            Name of the pressure history file.
        massflow_filename : str, optional
            Name of the mass-flow history file.
        temperature_filename : str, optional
            Name of the temperature history file.
        output_dir : str, optional
            Directory where the CSV outputs are created.

        Returns
        -------
        None
            Writes the pressure, mass-flow, temperature, and metadata files to disk.
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"Created directory: {output_dir}")

        pressure_path = os.path.join(output_dir, pressure_filename)
        massflow_path = os.path.join(output_dir, massflow_filename)
        temperature_path = os.path.join(output_dir, temperature_filename)
        metadata_path = os.path.join(output_dir, "simulation_metadata.csv")

        real_cells = [c for c in self.discretisedFeed if c.type != 'g']
        real_cell_ids = [c.getID() for c in real_cells]
        time_array = np.arange(self.current_iteration) * self.dt

        with open(metadata_path, 'w', newline='') as metadata_file:
            writer = csv.writer(metadata_file)
            writer.writerow(['Parameter', 'Value', 'Unit'])
            writer.writerow(['Total Iterations', self.current_iteration, 'iterations'])
            writer.writerow(['Time Step (dt)', self.dt, 's'])
            writer.writerow(['Total Simulation Time', time_array[-1] if len(time_array) > 0 else 0, 's'])
            writer.writerow(['Number of Nodes', len(real_cells), 'nodes'])
            writer.writerow(['Pipe Length', self.totalPipeLength, 'm'])
            writer.writerow(['Node Spacing (dL)', self.dL, 'm'])
            writer.writerow(['Inlet Pressure', self.inletPressure, 'Pa'])
            writer.writerow(['Outlet Pressure', self.outletPressure, 'Pa'])
            writer.writerow(['Initial Mass Flow', self.mdot, 'kg/s'])

            exit_orifice = None
            for comp in self.discretisedFeed:
                if hasattr(comp, 'type') and comp.type == 'oe' and hasattr(comp, 'dynamic') and comp.dynamic:
                    exit_orifice = comp
                    break

            if exit_orifice and hasattr(exit_orifice, 'CdAList'):
                ramp_start_iter = min([iter_idx for _, iter_idx in exit_orifice.CdAList])
                ramp_end_iter = max([iter_idx for _, iter_idx in exit_orifice.CdAList])
                ramp_start_time = ramp_start_iter * self.dt
                ramp_end_time = ramp_end_iter * self.dt
                ramp_start_cda = exit_orifice.CdAList[0][0]
                ramp_end_cda = exit_orifice.CdAList[-1][0]

                writer.writerow(['CdA_Ramp_Start_Time', ramp_start_time, 's'])
                writer.writerow(['CdA_Ramp_End_Time', ramp_end_time, 's'])
                writer.writerow(['CdA_Ramp_Start_Value', ramp_start_cda, 'm²'])
                writer.writerow(['CdA_Ramp_End_Value', ramp_end_cda, 'm²'])
                writer.writerow(['CdA_Ramp_Active', 'True', 'boolean'])
            else:
                writer.writerow(['CdA_Ramp_Active', 'False', 'boolean'])

            avg_pressure = (self.inletPressure + self.outletPressure) / 2
            self.fluid.update(Input.pressure(avg_pressure), Input.temperature(self.initTemp))
            sound_speed = float(self.fluid.sound_speed or 0.0)
            theoretical_frequency = sound_speed / (4.0 * self.totalPipeLength)

            writer.writerow(['Average_Pressure', avg_pressure, 'Pa'])
            writer.writerow(['Sound_Speed', sound_speed, 'm/s'])
            writer.writerow(['Theoretical_Pipe_Frequency', theoretical_frequency, 'Hz'])

        with open(pressure_path, 'w', newline='') as pressure_file:
            writer = csv.writer(pressure_file)
            writer.writerow(['# Simulation Metadata'])
            writer.writerow([f'# Total Iterations: {self.current_iteration}'])
            writer.writerow([f'# Time Step (dt): {self.dt} s'])
            writer.writerow(['# Data begins below'])

            header = ['Time (s)']
            data_indices = []

            for cell in real_cells:
                if cell.getType() in ['o', 'oe']:
                    header.append(f'{cell.getType()}_{cell.getID()}_Pressure_In (Pa)')
                    header.append(f'{cell.getType()}_{cell.getID()}_Pressure_Out (Pa)')
                    data_indices.append(cell.getID())
                    data_indices.append(cell.getID() + 1)
                else:
                    header.append(f'{cell.getType()}_{cell.getID()}_Pressure (Pa)')
                    data_indices.append(cell.getID())

            writer.writerow(header)

            for i in range(self.current_iteration):
                row = [time_array[i]]
                for data_idx in data_indices:
                    row.append(self.pressure_history[data_idx, i])
                writer.writerow(row)

        with open(massflow_path, 'w', newline='') as massflow_file:
            writer = csv.writer(massflow_file)
            writer.writerow(['# Simulation Metadata'])
            writer.writerow([f'# Total Iterations: {self.current_iteration}'])
            writer.writerow(['# Data begins below'])

            header = ['Time (s)']
            data_indices = []

            for cell in real_cells:
                if cell.getType() in ['o', 'oe']:
                    header.append(f'{cell.getType()}_{cell.getID()}_Massflow_In (kg/s)')
                    header.append(f'{cell.getType()}_{cell.getID()}_Massflow_Out (kg/s)')
                    data_indices.append(cell.getID())
                    data_indices.append(cell.getID() + 1)
                else:
                    header.append(f'{cell.getType()}_{cell.getID()}_Massflow (kg/s)')
                    data_indices.append(cell.getID())

            writer.writerow(header)

            for i in range(self.current_iteration):
                row = [time_array[i]]
                for data_idx in data_indices:
                    row.append(self.mdot_history[data_idx, i])
                writer.writerow(row)

        with open(temperature_path, 'w', newline='') as temperature_file:
            writer = csv.writer(temperature_file)
            writer.writerow(['# Simulation Metadata'])
            writer.writerow([f'# Total Iterations: {self.current_iteration}'])
            writer.writerow(['# Data begins below'])

            header = ['Time (s)']
            data_indices = []

            for cell in real_cells:
                if cell.getType() in ['o', 'oe']:
                    header.append(f'{cell.getType()}_{cell.getID()}_Temperature_In (K)')
                    header.append(f'{cell.getType()}_{cell.getID()}_Temperature_Out (K)')
                    data_indices.append(cell.getID())
                    data_indices.append(cell.getID() + 1)
                else:
                    header.append(f'{cell.getType()}_{cell.getID()}_Temperature (K)')
                    data_indices.append(cell.getID())

            writer.writerow(header)

            for i in range(self.current_iteration):
                row = [time_array[i]]
                for data_idx in data_indices:
                    row.append(self.temp_history[data_idx, i])
                writer.writerow(row)

        print("Data written to:")
        print(f"  Pressure: {pressure_path}")
        print(f"  Mass flow: {massflow_path}")
        print(f"  Metadata: {metadata_path}")
        print(f"Data shape: {self.current_iteration} time steps x {len(real_cell_ids)} cells")
