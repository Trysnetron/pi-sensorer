% raspiImport takes in a path string and imports a specified binary data
% file from this path. It returns the raw data, the sample period in seconds and the number of samples.
function [samples, sample_period, rawData] = raspiImport(path,channels)

%% Input argumet handling
if nargin < 2
    channels = 1;   % Assume single channel as nothing was specified
    warning('Number of channels not defined, assuming single...');
end

%% Read data
% Make file IDs
fidAdcData = fopen(strcat(path,'skt7.bin'));
% Read binary data to local variables
sample_period = fread(fidAdcData, 1, 'double')*1.0e-06;
adcData = fread(fidAdcData,'uint16');
% Close files properly after import
fclose(fidAdcData);

%% Generate useful raw data
% Useful variables
lenAdcData = length(adcData);       % Total number of ADC data bytes
samples = lenAdcData/channels;      % Total number of samples
rawData = zeros(samples,channels);  % Raw data matrix

% Order separate channel data into a matrix
for i = 0:samples-1
    % ADC data:
    for j = 0:channels-1
        rawData(i+1,j+1) = adcData((i*channels + j) + 1);
    end
end
end
