function [simCdASI, simN2Pressure, simFuelPressure, simFuelEregPortTemp] = calculateFuelCdA(n2TankPressurePa, propellantPressurePa,eregInletTemperatureK)

n2TankBlockPressure = n2TankPressurePa;
fuelTankBlockPressure = propellantPressurePa;
fuelEregInletBlockTemperature = eregInletTemperatureK;

out = sim("feed_system_harness.slx");
mdot = double(out.simFuelEregMdot.Data);
Q = double(out.simFuelEregInletQ.Data);
rho = mdot./Q;
dP = double(out.simFuelEregInletPressure.Data - out.simFuelEregOutletPressure.Data);

simCdASI = -Q .* sqrt(rho./(2*dP));

simN2Pressure = double(out.simN2TankPressure.Data);
simFuelPressure = double(out.simFuelTankPressure.Data);
simFuelEregPortTemp = double(out.simFuelEregPortTemp.Data);
