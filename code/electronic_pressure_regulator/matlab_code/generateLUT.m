%% Run to Generate LUT based on N2 Tank Pressure, Propellant Pressure,
% and Ereg Temperature

clear; clc;

startup

set_param('feed_system_harness','FastRestart','On')
set_param('feed_system_harness','SimulationMode', 'accelerator')
set_param('feed_system_harness', 'StartTime','0','StopTime', '1')
%% Define parameters for LUT generation

n2TankPressure = 300:-60:60;          % bar
n2TankPressurePa = n2TankPressure * 1e5;              % Pa

%% Global LUT axes
% These will automatically remain sorted in ascending order

globalN2Pressure = [];

% CdA LUT:
%   dimension 1 = N2 pressure
CdALUT = [];


%% Tolerances for deciding whether a value already exists
% Prevents tiny floating-point differences from creating extra LUT points.

pressureTolerance = 1;      % Pa
temperatureTolerance = 1e-6; % K


%% Run simulations

for i = 1:length(n2TankPressurePa)
    [simCdASI, ...
     simN2Pressure, ...
     simFuelPressure, ...
     simFuelEregPortTemp] = ...
        calculateFuelCdA( ...
            n2TankPressurePa(i), ...
            propellantPressurePa(j), ...
            eregInletTemperatureK(k));
    
    
    %% Make sure everything is a row vector
    simCdASI            = simCdASI(:).';
    simN2Pressure       = simN2Pressure(:).';
    simFuelPressure     = simFuelPressure(:).';
    simFuelEregPortTemp = simFuelEregPortTemp(:).';
    
    
    %% Check that all returned arrays correspond timestep-by-timestep
    N = length(simCdASI);
    
    assert(length(simN2Pressure) == N, ...
        'simN2Pressure length does not match simCdASI.');
    
    assert(length(simFuelPressure) == N, ...
        'simFuelPressure length does not match simCdASI.');
    
    assert(length(simFuelEregPortTemp) == N, ...
        'simFuelEregPortTemp length does not match simCdASI.');
    
    
    %% Process every timestep from this simulation
    
    for t = 1:N
    
        n2P   = simN2Pressure(t);
        fuelP = simFuelPressure(t);
        temp  = simFuelEregPortTemp(t);
        CdA   = simCdASI(t);
    
    
        %% First datapoint initializes the LUT
        if isempty(CdALUT)
    
            globalN2Pressure = n2P;
            globalFuelPressure = fuelP;
            globalEregTemperature = temp;
    
            CdALUT = nan(1,1,1);
            CdALUT(1,1,1) = CdA;
    
            continue
    
        end
    
    
        %% ---------------------------------------------------------
        % N2 PRESSURE AXIS
        % ----------------------------------------------------------
    
        [globalN2Pressure, idxN2, inserted] = ...
            insertSortedValue( ...
                globalN2Pressure, ...
                n2P, ...
                pressureTolerance);
    
        % If a new pressure was added, insert a corresponding
        % NaN plane into dimension 1 of the CdA LUT.
        if inserted
            CdALUT = insertNaNSlice(CdALUT, 1, idxN2);
        end
    
    
        %% ---------------------------------------------------------
        % FUEL PRESSURE AXIS
        % ----------------------------------------------------------
    
        [globalFuelPressure, idxFuel, inserted] = ...
            insertSortedValue( ...
                globalFuelPressure, ...
                fuelP, ...
                pressureTolerance);
    
        % Insert corresponding NaN plane into dimension 2.
        if inserted
            CdALUT = insertNaNSlice(CdALUT, 2, idxFuel);
        end
    
    
        %% ---------------------------------------------------------
        % EREG TEMPERATURE AXIS
        % ----------------------------------------------------------
    
        [globalEregTemperature, idxTemp, inserted] = ...
            insertSortedValue( ...
                globalEregTemperature, ...
                temp, ...
                temperatureTolerance);
    
        % Insert corresponding NaN plane into dimension 3.
        if inserted
            CdALUT = insertNaNSlice(CdALUT, 3, idxTemp);
        end
    
    
        %% ---------------------------------------------------------
        % INSERT CdA INTO CORRECT LUT LOCATION
        % ----------------------------------------------------------
    
        CdALUT(idxN2, idxFuel, idxTemp) = CdA;
    

    
end


%% Display final LUT dimensions

fprintf('\nLUT generation complete.\n');

fprintf('N2 pressure points:   %d\n', length(globalN2Pressure));

fprintf('CdA LUT dimensions:   %d x %d x %d\n', ...
    size(CdALUT,1), ...
    size(CdALUT,2), ...
    size(CdALUT,3));


%% ========================================================================
% LOCAL FUNCTIONS

function [array, idx, inserted] = insertSortedValue(array, value, tolerance)
% insertSortedValue
%
% Checks whether VALUE already exists in ARRAY within TOLERANCE.
%
% If it exists:
%   - ARRAY is unchanged
%   - IDX gives its existing index
%   - INSERTED = false
%
% If it does not exist:
%   - VALUE is inserted in ascending order
%   - IDX gives its new index
%   - INSERTED = true


    if isempty(array)

        array = value;
        idx = 1;
        inserted = true;
        return

    end


    %% Check whether value already exists

    differences = abs(array - value);

    [minimumDifference, existingIdx] = min(differences);


    if minimumDifference <= tolerance

        idx = existingIdx;
        inserted = false;
        return

    end


    %% Find location where new value should be inserted

    idx = find(array > value, 1, 'first');


    if isempty(idx)

        % New value is larger than everything currently in array
        array(end+1) = value;
        idx = length(array);

    else

        % Insert value before first larger element
        array = [ ...
            array(1:idx-1), ...
            value, ...
            array(idx:end) ...
        ];

    end

    inserted = true;

end


function newLUT = insertNaNSlice(LUT, dimension, idx)
% insertNaNSlice
%
% Inserts a NaN slice at IDX along the requested LUT dimension.
%
% Existing data is shifted so that its relationship with the LUT
% coordinate arrays remains unchanged.


    n1 = size(LUT,1);
    n2 = size(LUT,2);
    n3 = size(LUT,3);


    switch dimension

        %% N2 pressure dimension
        case 1

            newLUT = nan(n1 + 1, n2, n3);

            if idx > 1
                newLUT(1:idx-1,:,:) = LUT(1:idx-1,:,:);
            end

            if idx <= n1
                newLUT(idx+1:end,:,:) = LUT(idx:end,:,:);
            end


        %% Fuel pressure dimension
        case 2

            newLUT = nan(n1, n2 + 1, n3);

            if idx > 1
                newLUT(:,1:idx-1,:) = LUT(:,1:idx-1,:);
            end

            if idx <= n2
                newLUT(:,idx+1:end,:) = LUT(:,idx:end,:);
            end


        %% Temperature dimension
        case 3

            newLUT = nan(n1, n2, n3 + 1);

            if idx > 1
                newLUT(:,:,1:idx-1) = LUT(:,:,1:idx-1);
            end

            if idx <= n3
                newLUT(:,:,idx+1:end) = LUT(:,:,idx:end);
            end


        otherwise

            error('Dimension must be 1, 2, or 3.');

    end

end