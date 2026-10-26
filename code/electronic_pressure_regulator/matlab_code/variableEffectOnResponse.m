function [resultStruct] = variableEffectOnResponse(variableNameArray, variableValueArray, signalName, modelName)

    % Open the Simulink model in the background
    open_system(modelName);
    set_param(modelName, "FastRestart", "on")
    set_param(modelName, 'SimulationMode', 'Accelerator')

    if numel(variableNameArray) ~= numel(variableValueArray)
        error('Variable Value Array and Name Array must be of the same length.')
    end

    % --- FOLDER CREATION ---
    % Generate a safe timestamp (no colons)
    timestamp = char(datetime('now', 'Format', 'yyyy_MM_dd_HH_mm_ss'));
    
    % Define the folder name
    resultsFolder = sprintf('variable_effect_on_response_results_%s', timestamp);
    
    % Create the folder in the current working directory
    mkdir(resultsFolder);
    
    resultStruct = struct();
    multipliers = [0.8, 0.9, 1.0, 1.2]; % The 4 percentage shifts

    for i = 1:numel(variableNameArray)
        iVarName = string(variableNameArray(i));
        iVarValue = variableValueArray(i);
        varValueArray = multipliers * iVarValue;
        
        % 1. Log the test values used for this variable
        resultStruct.(iVarName).TestValues = varValueArray;
        
        comparisonResults = struct();
        
        % --- STEP RESPONSE PLOTTING SETUP ---
        stepFig = figure('Name', sprintf('Step Responses: %s', iVarName), 'Visible', 'off');
        
        for j = 1:numel(varValueArray)
            assignin('base', char(iVarName), varValueArray(j));
            simOut = sim(modelName);
            logsOut = simOut.get('logsout');
            signalOut = logsOut.get(signalName).Values;
            
            % 2. Store the raw Time and Data 
            resultStruct.(iVarName).StepResponseData(j).Multiplier = multipliers(j);
            resultStruct.(iVarName).StepResponseData(j).Time = signalOut.Time;
            resultStruct.(iVarName).StepResponseData(j).Data = signalOut.Data;
            
            % Target the j-th position in a 2x2 grid
            subplot(2, 2, j);
            
            % Plot this iteration's step response
            plot(signalOut.Time, signalOut.Data, 'LineWidth', 1.5);
            
            % Format this specific subplot
            title(sprintf('Value: %.2f (%.1fx)', varValueArray(j), multipliers(j)));
            xlabel('Time');
            ylabel('Signal Amplitude');
            grid on;
            
            % Calculate stepinfo
            stepInfo = stepinfo(signalOut.Data, signalOut.Time);
            comparisonResults(j).stepInfo = stepInfo;
        end
        
        % Add a super-title to the overall 2x2 figure
        sgtitle(sprintf('System Step Responses varying %s', iVarName), 'Interpreter', 'none');
        
        % Save to the newly created folder, then CLOSE
        stepFigPath = fullfile(resultsFolder, sprintf('%s_StepResponses.fig', iVarName));
        savefig(stepFig, stepFigPath);
        close(stepFig); 
        
        % --- TREND ANALYSIS & SUBPLOT SETUP ---
        xaxis = 1:numel(varValueArray);
        stepInfoNames = fieldnames(comparisonResults(1).stepInfo);
        
        trendFig = figure('Name', sprintf('Metric Trends: %s', iVarName), ...
                          'Position', [100, 100, 1200, 800], ...
                          'Visible', 'off');
        
        for k = 1:numel(stepInfoNames)
            metricName = stepInfoNames{k};
            metricValues = arrayfun(@(x) x.stepInfo.(metricName), comparisonResults);
            
            % 3. Store the raw 4 metrics in the struct
            resultStruct.(iVarName).RawMetrics.(metricName) = metricValues;
            
            % Calculate the trendline
            p = polyfit(xaxis, metricValues, 1);
            yfit = polyval(p, xaxis); 
            
            % 4. Log the trend direction
            if p(1) >= 0
                resultStruct.(iVarName).Trend.(metricName) = "Increases";
            else 
                resultStruct.(iVarName).Trend.(metricName) = "Decreases";
            end
            
            % Create a 4x4 grid of plots for the metrics
            subplot(4, 4, k);
            
            % Plot data points and fit line
            plot(varValueArray, metricValues, 'bo', 'MarkerFaceColor', 'b'); 
            hold on;
            plot(varValueArray, yfit, 'r-', 'LineWidth', 1.5); 
            
            title(metricName, 'Interpreter', 'none'); 
            xlabel('Variable Value');
            grid on;
            hold off;
        end
        
        % Save to the newly created folder, then CLOSE
        trendFigPath = fullfile(resultsFolder, sprintf('%s_MetricTrends.fig', iVarName));
        savefig(trendFig, trendFigPath);
        close(trendFig);

        assignin('base', char(iVarName), varValueArray(3));
    end

    tableStruct = struct(); 
    
    fieldNames = fieldnames(resultStruct);
    tableStruct.TestedVariables = string(fieldNames); 
    
    trendFieldNames = fieldnames(resultStruct.(fieldNames{1}).Trend);
    
    for j = 1:numel(trendFieldNames)
        tableStruct.(trendFieldNames{j}) = strings(numel(fieldNames), 1); 
    end
    
    for i = 1:numel(fieldNames)
        currentVar = fieldNames{i};
        
        for j = 1:numel(trendFieldNames)
            currentMetric = trendFieldNames{j};
            trendValue = resultStruct.(currentVar).Trend.(currentMetric);
            tableStruct.(currentMetric)(i) = trendValue;
        end
    end
    
    finalTable = struct2table(tableStruct);
    
    disp(finalTable);
    
    excelPath = fullfile(resultsFolder, 'Trend_Analysis_Summary.xlsx');
    writetable(finalTable, excelPath);
end