function [bestKp1, bestKp2, bestKc, results, evalLog] = tuningAlgorithm(maxEval, modelName)
    set_param(modelName, "FastRestart", "on")
    set_param(modelName, 'SimulationMode', 'Accelerator')

    % --- search space, same bounds as the original grid ---
    Kp1Var = optimizableVariable('Kp1', [15, 100], 'Type', 'integer');
    Kp2Var = optimizableVariable('Kp2', [100, 1000], 'Type', 'integer');
    KcVar  = optimizableVariable('Kc',  [0.05, 0.5]);

    % --- persistent log of every evaluated point + its signal logs ---
    % (bayesopt only tracks the scalar objective, not signalLogs, so we
    % capture those ourselves via this nested-closure log)
    evalLog = struct('Kp1', {}, 'Kp2', {}, 'Kc', {}, 'ndError', {}, 'signalLogs', {});

    objFun = @(x) tuningObjective(x, modelName);

    results = bayesopt(objFun, [Kp1Var, Kp2Var, KcVar], ...
        'MaxObjectiveEvaluations', maxEval, ...
        'IsObjectiveDeterministic', true, ...
        'AcquisitionFunctionName', 'expected-improvement-plus', ...
        'PlotFcn', {@plotObjectiveModel, @plotMinObjective}, ...
        'Verbose', 1);

    bestKp1 = results.XAtMinObjective.Kp1;
    bestKp2 = results.XAtMinObjective.Kp2;
    bestKc  = results.XAtMinObjective.Kc;

    fprintf('\nBest result: Kp1 = %d, Kp2 = %d, Kc = %0.3f, |ndError| = %g\n', ...
        bestKp1, bestKp2, bestKc, results.MinObjective);

    % --- nested function so it can see/append to evalLog ---
    function objective = tuningObjective(x, modelName)
        Kp1 = x.Kp1;
        Kp2 = x.Kp2;
        Kc  = x.Kc;
        [logsOut, ndError] = runHarness(Kp1, Kp2, Kc, modelName);
        objective = abs(ndError);

        idx = numel(evalLog) + 1;
        evalLog(idx).Kp1 = Kp1;
        evalLog(idx).Kp2 = Kp2;
        evalLog(idx).Kc  = Kc;
        evalLog(idx).ndError = ndError;
        evalLog(idx).signalLogs = logsOut;
    end
end

function [logsOut, ndError] = runHarness(Kp1, Kp2, Kc, modelName)
    fprintf('Running with Kp1 = %d\n', Kp1)
    fprintf('Running with Kp2 = %d\n', Kp2)
    fprintf('Running with Kc = %0.2f\n', Kc) 

    ndError = 0;
    set_param(strcat(modelName, '/Constant2'), 'Value', string(1));
    simOut = sim(modelName);
    logsOut = simOut.get('logsout');
    ndError = ndError + logsOut.get('NonDim Error').Values.Data(end);

    set_param(strcat(modelName, '/Constant2'), 'Value', string(0));
    simOut = sim(modelName);
    logsOut = simOut.get('logsout');
    ndError = ndError + logsOut.get('NonDim Error').Values.Data(end);

    set_param(strcat(modelName, '/Constant2'), 'Value', string(-1));
    simOut = sim(modelName);
    logsOut = simOut.get('logsout');
    ndError = ndError + logsOut.get('NonDim Error').Values.Data(end);
end