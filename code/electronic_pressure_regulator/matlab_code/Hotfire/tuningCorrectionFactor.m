function [bestParams, results, evalLog] = tuningCorrectionFactor(maxEval, modelName, varNames, bounds, varTypes)
    arguments
        maxEval (1,1) double
        modelName (1,:) char
        varNames cell
        bounds (:,2) double
        varTypes cell = repmat({'real'}, numel(varNames), 1)
    end

    nVars = numel(varNames);
    assert(size(bounds, 1) == nVars, ...
        'bounds must have exactly one row per entry in varNames.');
    assert(numel(varTypes) == nVars, ...
        'varTypes must have exactly one entry per entry in varNames.');

    set_param(modelName, 'FastRestart', 'on');
    set_param(modelName, 'SimulationMode', 'Accelerator');

    % --- build the optimizableVariable array dynamically ---
    optVars = optimizableVariable.empty(0, nVars);
    for i = 1:nVars
        optVars(i) = optimizableVariable(varNames{i}, bounds(i, :), ...
            'Type', varTypes{i});
    end

    % --- persistent log of every evaluated point + its signal logs ---
    % (bayesopt only tracks the scalar objective, not signalLogs, so we
    % capture those ourselves via this nested-closure log)
    evalLog = struct('params', {}, 'ndError', {}, 'signalLogs', {}, 'error', {});

    objFun = @(x) tuningObjective(x, modelName, varNames);

    results = bayesopt(objFun, optVars, ...
        'MaxObjectiveEvaluations', maxEval, ...
        'IsObjectiveDeterministic', true, ...
        'AcquisitionFunctionName', 'expected-improvement-plus', ...
        'PlotFcn', {@plotObjectiveModel, @plotMinObjective}, ...
        'Verbose', 1);

    bestParams = struct();
    for i = 1:nVars
        bestParams.(varNames{i}) = results.XAtMinObjective.(varNames{i});
    end

    fprintf('\nBest result: |RMSE| = %g\n', results.MinObjective);
    for i = 1:nVars
        fprintf('  %s = %g\n', varNames{i}, bestParams.(varNames{i}));
    end

    % --- nested function so it can see/append to evalLog ---
    function objective = tuningObjective(x, modelName, varNames)
        paramStruct = struct();
        for k = 1:numel(varNames)
            paramStruct.(varNames{k}) = x.(varNames{k});
        end

        [logsOut, RMSE, simError] = runHarness(paramStruct, modelName);

        if isempty(simError)
            objective = abs(RMSE);
        else
            % Sim failed for this point. NaN tells bayesopt this
            % evaluation is invalid; it logs it as an error and moves on
            % to a new guess rather than stopping the whole run.
            objective = NaN;
        end

        idx = numel(evalLog) + 1;
        evalLog(idx).params     = paramStruct;
        evalLog(idx).RMSE       = RMSE;
        evalLog(idx).signalLogs = logsOut;
        evalLog(idx).error      = simError;
    end
end

function [logsOut, RMSE, simError] = runHarness(paramStruct, modelName)
    names = fieldnames(paramStruct);
    for k = 1:numel(names)
        fprintf('Running with %s = %g\n', names{k}, paramStruct.(names{k}));
        assignin('base', names{k}, paramStruct.(names{k}));
    end

    set_param(strcat(modelName, '/Constant2'), 'Value', string(0));
    try
        % Real test data
        eregResponse = testData.(fieldname);
        time = testData.Time;   % Change 'Time' if your time column has another name
        
        % Run Simulink model
        simOut = sim('feed_system_harness_fuel_hotfire');
        
        % Get logged simulation outputs
        simResponseLO = simOut.get('logsout');
        
        % Extract simulated valve command
        simCommand = simResponseLO.get('Valve Command');
        
        simCommandData = simCommand.Values.Data;
        simCommandTime = simCommand.Values.Time;
    
       
        % Calculate comparison error
    
        % Interpolate simulation onto measured-data timestamps
        simResponseInterp = interp1( ...
            simCommandTime, ...
            simCommandData, ...
            time, ...
            'linear', ...
            NaN);
        
        validIdx = ~isnan(simResponseInterp) & ~isnan(eregResponse);
        
        error = eregResponse(validIdx) - simResponseInterp(validIdx);
    
        RMSE = sqrt(mean(error.^2));
        MAE  = mean(abs(error));
    
        

    catch ME
        simError = ME;
        fprintf(2, 'Sim failed for this point (%s) -- skipping to next guess.\n', ...
            ME.message);
    end
end