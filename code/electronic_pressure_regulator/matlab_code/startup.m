% startup.m
% Runs automatically when MATLAB is launched
disp('Initializing MATLAB...');
open_system('feed_system_harness_fuel.slx')
addpath(genpath(pwd()))

% 1. Define the absolute path to data file
fluidDataPath = fullfile(pwd,'simscape_fluids_data.mat');

% 2. Check if the file exists and load it
if isfile(fluidDataPath)
    load(fluidDataPath);
    disp('-> Success: Loaded Simscape Fluid properties.');
else
    warning('startup.m: Could not find simscape_fluids_data.mat.');
    disp(['Expected location: ', fluidDataPath]);
end

% 3. Initialise Variables into workspace
simVariables;
CdARelationship;