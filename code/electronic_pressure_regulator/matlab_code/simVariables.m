modelName = 'feed_system_harness_fuel_hotfire';
%% Command Timings
mainValveTime = 2; %s
eregValveDelay = 0;
%% Command Limits
% eregHardStop = 45; %deg
%% Gains 
%Fuel
Kp1Fuel = 0.1; 
Kp2Fuel = 0.1;
KpRampTimeFuel = 2; %s
KcFuel = 1;

%Ox
Kp1Ox = 1; 
Kp2Ox = 16;
KpRampTimeOx = 3.5; %s
KcOx = 1;
%% Pressure Settings
% Nitrogen 
nitrogenPressure = 300; %bar    
nitrogenPressure = nitrogenPressure * 1e+05; %Pa
% Fuel
fuelSetpoint = 45; %bar
fuelSetpoint = fuelSetpoint * 1e+05; %Pa
fuelRho = 790; %kg/m^3
fuelMdot = 0.79; %kg/s
fuelFillMass = 6; %kg

% Ox
oxSetpoint = 45; %bar
oxSetpoint = oxSetpoint * 1e+05; %Pa
oxRho = 963; %kg/m^3
oxMdot = 2.35; %kg/s
oxFillMass = 20; %kg

OFRatio = oxMdot/fuelMdot;
%% Valve Properties
% Fuel 
fuelClose    = 95;
fuelOpen     = 140;
fuelCracking = 108;

oxClose    = 0;
oxOpen     = 45;
oxCracking = 13;
