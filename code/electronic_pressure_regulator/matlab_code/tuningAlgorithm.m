function [bestParams, results, evalLog] = tuningAlgorithm(maxEval, modelName, varNames, bounds, varTypes)
%TUNINGALGORITHM Bayesian-optimize an arbitrary set of Simulink parameters.
%
%   [bestParams, results, evalLog] = tuningAlgorithm(maxEval, modelName, varNames, bounds)
%   [bestParams, results, evalLog] = tuningAlgorithm(maxEval, modelName, varNames, bounds, varTypes)
%
%   Inputs:
%     maxEval   - max number of bayesopt evaluations (scalar)
%     modelName - Simulink model name (char/string)
%     varNames  - cell array of variable name strings,
%                 e.g. {'Kp1', 'Kp2', 'Kc'}
%     bounds    - Nx2 numeric array of [lower upper] bounds, one row per
%                 variable, same order as varNames.
%                 e.g. [1 100; 1 10000; 1 100]
%     varTypes  - (optional) cell array of 'integer'/'real' per variable,
%                 same order as varNames. Defaults to 'real' for every
%                 variable if omitted (matches optimizableVariable's own
%                 default).
%
%   Outputs:
%     bestParams - struct with one field per varNames entry, holding the
%                  best found value for that variable
%     results    - the bayesopt BayesianOptimization results object
%     evalLog    - struct array logging every evaluated point:
%                  evalLog(i).params      -> struct of that iteration's values
%                  evalLog(i).ndError     -> that iteration's ndError (NaN if the sim errored)
%                  evalLog(i).signalLogs  -> that iteration's logsout (empty if the sim errored)
%                  evalLog(i).error       -> MException if the sim errored, else []
%
%   If sim(modelName) errors for a given point, that point is logged with
%   ndError = NaN and objective = NaN. bayesopt treats a NaN objective as
%   a failed evaluation: it does not stop the run, it just proposes a new
%   guess on the next iteration.

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

    fprintf('\nBest result: |ndError| = %g\n', results.MinObjective);
    for i = 1:nVars
        fprintf('  %s = %g\n', varNames{i}, bestParams.(varNames{i}));
    end

    % --- nested function so it can see/append to evalLog ---
    function objective = tuningObjective(x, modelName, varNames)
        paramStruct = struct();
        for k = 1:numel(varNames)
            paramStruct.(varNames{k}) = x.(varNames{k});
        end

        [logsOut, ndError, simError] = runHarness(paramStruct, modelName);

        if isempty(simError)
            objective = abs(ndError);
        else
            % Sim failed for this point. NaN tells bayesopt this
            % evaluation is invalid; it logs it as an error and moves on
            % to a new guess rather than stopping the whole run.
            objective = NaN;
        end

        idx = numel(evalLog) + 1;
        evalLog(idx).params     = paramStruct;
        evalLog(idx).ndError    = ndError;
        evalLog(idx).signalLogs = logsOut;
        evalLog(idx).error      = simError;
    end
end

function [logsOut, ndError, simError] = runHarness(paramStruct, modelName)
    names = fieldnames(paramStruct);
    for k = 1:numel(names)
        fprintf('Running with %s = %g\n', names{k}, paramStruct.(names{k}));
        assignin('base', names{k}, paramStruct.(names{k}));
    end

    set_param(strcat(modelName, '/Constant2'), 'Value', string(0));

    logsOut  = [];
    ndError  = NaN;
    simError = [];

    try
        simOut  = sim(modelName);
        logsOut = simOut.get('logsout');
        ndCommandError = logsOut.get('NonDim Command Error Fuel').Values.Data(end);
        ndSetpointError = logsOut.get('NonDim Setpoint Error Fuel').Values.Data(end);
        ndError = abs(ndSetpointError);
    catch ME
        simError = ME;
        fprintf(2, 'Sim failed for this point (%s) -- skipping to next guess.\n', ...
            ME.message);
    end
end