% startup.m
% Runs automatically when MATLAB is launched

disp('Initializing MATLAB...');

% 1. Define the absolute path to your data file
% REPLACE this path with the actual folder where you keep the .mat file
fluidDataPath = fullfile(pwd,'simscape_fluids_data.mat');

% 2. Check if the file exists and load it
if isfile(fluidDataPath)
    load(fluidDataPath);
    disp('-> Success: Loaded Simscape Nitrogen and Ethanol properties.');
else
    warning('startup.m: Could not find simscape_fluids_data.mat.');
    disp(['Expected location: ', fluidDataPath]);
end