% startup.m
% Runs automatically when MATLAB is launched

disp('Initializing MATLAB...');

open_system('feed_system_harness.slx')
addpath(genpath(pwd()))
% 1. Define the absolute path to data file

fluidDataPath = fullfile(pwd,'simscape_fluids_data.mat');

% 2. Check if the file exists and load it
if isfile(fluidDataPath)
    load(fluidDataPath);
    disp('-> Success: Loaded Simscape Nitrogen and Ethanol properties.');
else
    warning('startup.m: Could not find simscape_fluids_data.mat.');
    disp(['Expected location: ', fluidDataPath]);
end

% 3. Placeholder simulation parameters

n2TankBlockPressure = 300e+05;
fuelTankBlockPressure = 60e+05;
fuelEregInletBlockTemperature = 300;