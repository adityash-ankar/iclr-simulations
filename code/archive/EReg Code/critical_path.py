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



class FeedSystemCriticalPath:
    def __init__(self, dt=1, totalPipeLength=1.0, fluid: Fluid=None, N=2, extraComponents=[[None,None],[None,None]], 
                 mdot: float = None, inletPressure: float = None, outletPressure: float = None, max_iterations=100000):
        self.N = N # Number of real cells (pipes)
        self.dL = totalPipeLength / N # Cell length
        self.totalPipeLength = totalPipeLength 
        self.inletPressure = inletPressure
        self.outletPressure = outletPressure
        self.extraComponents = extraComponents
        self.fluid = fluid 
        self.mdot = mdot
        self.dt = dt
        self.max_iterations = max_iterations
        self.current_iteration = 0
        self.rampStartCDA = 194e-6  # Initial CdA value
        # Pre-allocate numpy arrays for all time history data
        self.pressure_history = np.zeros((N + 3, max_iterations))  # +3 for ghost cells and exit orifice outlet
        self.temp_history = np.zeros((N + 3, max_iterations))
        self.mdot_history = np.zeros((N + 3, max_iterations))
        self.velocity_history = np.zeros((N + 3, max_iterations))
        fluid.update(Input.temperature(-180), Input.pressure(inletPressure))
        self.initTemp = fluid.temperature
        self.populate()
    def getCDA(self):
        return self.discretisedFeed[-1].getCDA()
    
    def initCont(self):
        #end orifice ramping:
        rampStartTime = 0.05  # seconds
        rampTime = 0.1  # seconds
        rampStartCDA = self.rampStartCDA  # Initial CdA value
        rampEndCDA = 50e-6  # Final CdA value
        rampNum = np.linspace(rampStartCDA, rampEndCDA, int(rampTime / self.dt))
        self.CdAList = []
        for i in range(len(rampNum)):
            self.CdAList.append((rampNum[i], i + int(rampStartTime/self.dt)))
        self.discretisedFeed[-1].setCdAList(self.CdAList)  # Set CdA list for the exit orifice

    


        

    def setMaxIterations(self, max_iterations):
        self.max_iterations = max_iterations
        self.pressure_history = np.zeros((self.N + 3, max_iterations))
        self.temp_history = np.zeros((self.N + 3, max_iterations))
        self.mdot_history = np.zeros((self.N + 3, max_iterations))
        self.velocity_history = np.zeros((self.N + 3, max_iterations))

    def discretise(self):
        self.discretisedFeed = []
        check = True
        for comp in self.extraComponents:
            if comp[0] is not None:
                comp[1] = round(comp[1] / self.dL)
                check = True
            else:
                check = False
        
        if check:
            self.extraComponents.sort(key=lambda comp: comp[0])

        count = 0
        for i in range(self.N):
            pos = count * self.dL
            if i in [comp[1] for comp in self.extraComponents if comp[0] is not None]:
                pass
            else:
                count += 1
                pipe = PipeJIT(fluid=self.fluid, length=self.dL, mdot=self.mdot, pos=pos, 
                              location=i+1, temp=self.initTemp, diameter=0.035)
            self.discretisedFeed.append(pipe)

    def populate(self):
        currentPressure = self.inletPressure
        self.discretise()
        self.discretisedFeed.append(OrificeJIT(location=self.N+1, CdA=self.rampStartCDA,fluid=self.fluid, ID=0.035, pos=self.totalPipeLength, 
                                              pressureIn=self.discretisedFeed[-1].getPressureOut(), 
                                              pressureOut=self.outletPressure, temp=self.initTemp, mdot=self.mdot, type="oe"))
        self.solveMdot(self.inletPressure, self.outletPressure)
        print(self.mdot)
        # Initialize pressures properly with steady-state pressure drop
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
        return sum(comp.dp(mdot=mdot, pressureIn=self.inletPressure) for comp in self.discretisedFeed if comp.getType() != "g")

    def solveMdot(self, inletPressure: Optional[float] = None, outletPressure: Optional[float] = None):
        dpTarget = inletPressure - outletPressure
        
        def dpFunc(mdot):
            return self.getSystemDP(mdot) - dpTarget
    
        brackets_to_try = [[0.001, 10], [0.0001, 1], [0.01, 100], [-1, 1], [-10, 10]]

        result = None
        for bracket in brackets_to_try:
            try:
                result = root_scalar(dpFunc, bracket=bracket, method='brentq')
                self.mdot = result.root
                break
            except Exception as e:
                continue
        
        if result is None:
            try:
                result = fsolve(dpFunc, 1.0)[0]

                self.mdot = result
            except:
                raise ValueError("Failed to solve for mass flow rate with any method.")

    def boundaryPopulation(self):
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
        """Optimized solve method using JIT where possible"""
        # Enforce boundary conditions first
        self.discretisedFeed[0].setPressureIn(self.inletPressure)  # Inlet ghost cell
        #self.discretisedFeed[-1].setPressureIn(self.outletPressure)  # Outlet ghost cell/orifice
        
        # First pass: Update internal cells
        for i, component in enumerate(self.discretisedFeed):
            if component.type == "g":
                component: ghostCellJIT
                if i == 0:  # Inlet ghost cell
                    component.setPressureIn(self.inletPressure)
                    component.setPressureOut(self.inletPressure)
                    component.setuIn(self.discretisedFeed[i+1].getuIn())
                    component.setuOut(self.discretisedFeed[i+1].getuIn())
                    component.set_u_iterate(self.discretisedFeed[i+1].get_u_iterate())
                elif i == len(self.discretisedFeed) - 1:  # Outlet ghost cell
                    component.setPressureIn(self.outletPressure)
                    component.setPressureOut(self.outletPressure)
                    component.setuIn(self.discretisedFeed[i-1].getuOut())
                    component.setuOut(self.discretisedFeed[i-1].getuOut())
                    component.set_u_iterate(self.discretisedFeed[i-1].get_u_iterate())
                continue
                
            if component.type == "oe":
                component: OrificeJIT
                component.solve(self.discretisedFeed[i-1].getPressureOut(), prevCell = self.discretisedFeed[i-1])
                # Enforce outlet pressure for exit orifice
                
            elif component.type == "o":
                component: OrificeJIT
                component.solve(self.discretisedFeed[i-1].getPressureOut(), self.discretisedFeed[i+1])
                self.upWinding(component, self.discretisedFeed[i-1], self.discretisedFeed[i+1])
            else:
                component: PipeJIT
                prev_pressure = self.discretisedFeed[i-1].getPressureIn() if i > 0 else self.inletPressure
                next_pressure = self.discretisedFeed[i+1].getPressureIn() if i < len(self.discretisedFeed)-1 else self.outletPressure
                prev_velocity = self.discretisedFeed[i-1].get_u_iterate() if i > 0 else 0
                
                component.solve_jit(prev_velocity, next_pressure, self.dt)
                self.upWinding(component, self.discretisedFeed[i-1], self.discretisedFeed[i+1])
        
        # Second pass: Update mass flows and record data
        for i, component in enumerate(self.discretisedFeed):
            if component.type == "g":
                continue
                
            if component.type == "oe":
                component.solveMdot(inletPressure=self.discretisedFeed[i-1].getPressureOut())
            else:
                next_pressure = self.discretisedFeed[i+1].getPressureIn()
                component.solveMdotIter()
            # Efficient array recording using JIT
            component.record_to_arrays_jit(self.pressure_history, self.temp_history, 
                                          self.mdot_history, self.velocity_history, 
                                          self.current_iteration)
        self.solveMdot(self.inletPressure, self.outletPressure)

        self.discretisedFeed[-2].velfromMdot(mdot = self.mdot, rho=self.discretisedFeed[-2].getFluid().density)
        self.current_iteration += 1


    def upWinding(self, current, previous, next):
        cellV = current.get_u_iterate()
        if cellV >= 0:
            current.setuIn(previous.get_u_iterate())
            current.setuOut(cellV)
        else:
            current.setuIn(cellV)
            current.setuOut(next.get_u_iterate())

    def get_cell_data(self, cell_id, up_to_iteration=None):
        if up_to_iteration is None:
            up_to_iteration = self.current_iteration
        
        return {
            'pressure': self.pressure_history[cell_id, :up_to_iteration],
            'temperature': self.temp_history[cell_id, :up_to_iteration],
            'mdot': self.mdot_history[cell_id, :up_to_iteration],
            'velocity': self.velocity_history[cell_id, :up_to_iteration]
        }

    def get_final_snapshot(self):
        final_iter = self.current_iteration - 1
        return {
            'pressure': self.pressure_history[:, final_iter],
            'temperature': self.temp_history[:, final_iter],
            'mdot': self.mdot_history[:, final_iter],
            'velocity': self.velocity_history[:, final_iter]
        }

    def write_to_csv(self, pressure_filename="pressure_data.csv", massflow_filename="massflow_data.csv", 
                     temperature_filename="temperature_results.csv", output_dir="simulation_results"):
        """Write data to CSV files with metadata"""
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
        
        # Write metadata file
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
            
            # Add CdA ramp information if available
            exit_orifice = None
            for comp in self.discretisedFeed:
                if hasattr(comp, 'type') and comp.type == 'oe' and hasattr(comp, 'dynamic') and comp.dynamic:
                    exit_orifice = comp
                    break
            
            if exit_orifice and hasattr(exit_orifice, 'CdAList'):
                # CdA ramp start and end times
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
            
            # Calculate and save theoretical pipe frequency (a/4L)
            avg_pressure = (self.inletPressure + self.outletPressure) / 2
            self.fluid.update(Input.pressure(avg_pressure), Input.temperature(self.initTemp))
            sound_speed = self.fluid.sound_speed
            theoretical_frequency = sound_speed / (4 * self.totalPipeLength)
            
            writer.writerow(['Average_Pressure', avg_pressure, 'Pa'])
            writer.writerow(['Sound_Speed', sound_speed, 'm/s'])
            writer.writerow(['Theoretical_Pipe_Frequency', theoretical_frequency, 'Hz'])
        
        # Write pressure data
        with open(pressure_path, 'w', newline='') as pressure_file:
            writer = csv.writer(pressure_file)
            writer.writerow(['# Simulation Metadata'])
            writer.writerow([f'# Total Iterations: {self.current_iteration}'])
            writer.writerow([f'# Time Step (dt): {self.dt} s'])
            writer.writerow(['# Data begins below'])
            
            # Create headers with separate inlet/outlet for orifices
            header = ['Time (s)']
            data_indices = []  # Track which array indices to use for each column
            
            for cell in real_cells:
                if cell.getType() in ['o', 'oe']:  # Orifices
                    header.append(f'{cell.getType()}_{cell.getID()}_Pressure_In (Pa)')
                    header.append(f'{cell.getType()}_{cell.getID()}_Pressure_Out (Pa)')
                    data_indices.append(cell.getID())      # Inlet pressure
                    data_indices.append(cell.getID() + 1)  # Outlet pressure
                else:  # Pipes and other components
                    header.append(f'{cell.getType()}_{cell.getID()}_Pressure (Pa)')
                    data_indices.append(cell.getID())
            
            writer.writerow(header)
            
            for i in range(self.current_iteration):
                row = [time_array[i]]
                for data_idx in data_indices:
                    row.append(self.pressure_history[data_idx, i])
                writer.writerow(row)
        
        # Write mass flow data
        with open(massflow_path, 'w', newline='') as massflow_file:
            writer = csv.writer(massflow_file)
            writer.writerow(['# Simulation Metadata'])
            writer.writerow([f'# Total Iterations: {self.current_iteration}'])
            writer.writerow(['# Data begins below'])
            
            # Create headers with separate inlet/outlet for orifices
            header = ['Time (s)']
            data_indices = []  # Track which array indices to use for each column
            
            for cell in real_cells:
                if cell.getType() in ['o', 'oe']:  # Orifices
                    header.append(f'{cell.getType()}_{cell.getID()}_Massflow_In (kg/s)')
                    header.append(f'{cell.getType()}_{cell.getID()}_Massflow_Out (kg/s)')
                    data_indices.append(cell.getID())      # Inlet massflow
                    data_indices.append(cell.getID() + 1)  # Outlet massflow
                else:  # Pipes and other components
                    header.append(f'{cell.getType()}_{cell.getID()}_Massflow (kg/s)')
                    data_indices.append(cell.getID())
            
            writer.writerow(header)
            
            for i in range(self.current_iteration):
                row = [time_array[i]]
                for data_idx in data_indices:
                    row.append(self.mdot_history[data_idx, i])
                writer.writerow(row)
        
        # Write temperature data
        with open(temperature_path, 'w', newline='') as temperature_file:
            writer = csv.writer(temperature_file)
            writer.writerow(['# Simulation Metadata'])
            writer.writerow([f'# Total Iterations: {self.current_iteration}'])
            writer.writerow(['# Data begins below'])
            
            # Create headers with separate inlet/outlet for orifices
            header = ['Time (s)']
            data_indices = []  # Track which array indices to use for each column
            
            for cell in real_cells:
                if cell.getType() in ['o', 'oe']:  # Orifices
                    header.append(f'{cell.getType()}_{cell.getID()}_Temperature_In (K)')
                    header.append(f'{cell.getType()}_{cell.getID()}_Temperature_Out (K)')
                    data_indices.append(cell.getID())      # Inlet temperature
                    data_indices.append(cell.getID() + 1)  # Outlet temperature
                else:  # Pipes and other components
                    header.append(f'{cell.getType()}_{cell.getID()}_Temperature (K)')
                    data_indices.append(cell.getID())
            
            writer.writerow(header)
            
            for i in range(self.current_iteration):
                row = [time_array[i]]
                for data_idx in data_indices:
                    row.append(self.temp_history[data_idx, i])
                writer.writerow(row)
        # Print summary
        print(f"Data written to:")
        print(f"  Pressure: {pressure_path}")
        print(f"  Mass flow: {massflow_path}")
        print(f"  Metadata: {metadata_path}")
        print(f"Data shape: {self.current_iteration} time steps x {len(real_cell_ids)} cells")
