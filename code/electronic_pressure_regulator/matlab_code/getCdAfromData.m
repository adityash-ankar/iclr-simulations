function CdA = getCdAfromData(upPressureData, downPressureData, massFlowData, propDensity)
upstreamPressure = mean(upPressureData);
downstreamPressure = mean(downPressureData);
delP = upstreamPressure - downstreamPressure;
massFlowRate = mean(massFlowData);

CdA = massFlowRate/sqrt(2 * propDensity * delP);