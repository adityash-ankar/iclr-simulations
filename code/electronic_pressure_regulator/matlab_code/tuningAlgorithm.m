function [bestKp, bestKc, tuningStruct] = tuningAlgorithm(maxIter, KpDiv, KcDiv, modelName)
    set_param(modelName, "FastRestart", "on")
    set_param(modelName, 'SimulationMode','Accelerator')
    a = KpDiv;
    b = KcDiv;
    KpArray = linspace(1e+01, 1e+03, a);
    KcArray = linspace(0.05, 0.5, b);

    tuningStruct = cell(maxIter, 1);   

    for iter = 1:maxIter
        resultStruct = getResultStruct(KpArray, KcArray, modelName);

        errorArray = zeros(a, b);
        for i = 1:a
            for j = 1:b
                errorArray(i, j) = resultStruct(i, j).ndError;
            end
        end

        [~, errorIdx] = min(abs(errorArray(:)));
        [errorRow, errorCol] = ind2sub(size(errorArray), errorIdx);

        % clamp neighbours so we don't run off the edge of the grid
        rowLo = max(errorRow - 1, 1);
        rowHi = min(errorRow + 1, a);
        colLo = max(errorCol - 1, 1);
        colHi = min(errorCol + 1, b);
        
        shrinkFactor = 0.5;   % tune to taste — smaller = faster convergence, more risk of overshooting the true optimum
        
        KpCenter = resultStruct(errorRow, errorCol).Kp;
        KpWidth  = (KpArray(end) - KpArray(1)) * shrinkFactor;
        KpArray  = linspace(KpCenter - KpWidth/2, KpCenter + KpWidth/2, a);
        
        KcCenter = resultStruct(errorRow, errorCol).Kc;
        KcWidth  = (KcArray(end) - KcArray(1)) * shrinkFactor;
        KcArray  = linspace(KcCenter - KcWidth/2, KcCenter + KcWidth/2, b);

        tuningStruct{iter} = resultStruct;
    end

    bestKp = resultStruct(errorRow, errorCol).Kp;
    bestKc = resultStruct(errorRow, errorCol).Kc;
end

function resultStruct = getResultStruct(KpArray, KcArray, modelName)
    for i = numel(KpArray):-1:1
        for j = numel(KcArray):-1:1
            iKp = KpArray(i);
            iKc = KcArray(j);
            [logsOut, ndError] = runHarness(iKp, iKc, modelName);
            resultStruct(i, j).Kp = iKp;
            resultStruct(i, j).Kc = iKc;
            resultStruct(i, j).ndError = ndError;
            resultStruct(i, j).signalLogs = logsOut;
        end
    end
end

function [logsOut, ndError] = runHarness(Kp, Kc, modelName)
    fprintf('Running with Kp = %d\n', Kp)
    fprintf('Running with Kc = %0.2f\n', Kc)
    set_param(strcat(modelName, '/CdA Correction Factor'), 'Value', string(Kc));
    set_param(strcat(modelName, '/Kp'), 'Value', string(Kp));
    simOut = sim(modelName);
    logsOut = simOut.get('logsout');
    ndError = logsOut.get('NonDim Error').Values.Data(end);
end