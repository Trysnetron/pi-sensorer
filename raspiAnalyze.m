% This script will import the binary data from files written by the C 
% program on Raspberry Pi. You need to update the path for your respective
% remote computer system(s) below in order to load the files.
%
% The script uses the function raspiImport to do the actual import and
% conversion from binary data to numerical values. Make sure you have
% downloaded it as well.
%
% After the import function is finished, the data are written to the
% variable rawData. The number of samples is returned in a variable samples

%% Program start
% First clear everything that was before. Comment this out if you want to
% keep something that is already open
clearvars; close all;


%% Definitions
channels = 5;   % Number of ADC channels used

%% Open, import and close binary data file produced by Raspberry Pi

%%%%% IMPORTANT SETUP %%%%%

% Check computer platform and assign correct path to data files
% BE SURE TO HAVE THE FINAL SLASH PRESENT IN THE PATH
if ismac
    % Code to run on Mac platform
    path = 'path-to-data/on-Mac-system/';
elseif isunix
    % Code to run on Linux platform
    path = 'path-to-data/on-Linux-system/';
elseif ispc
    % Code to run on Windows platform
    path = './';
else
    error('Platform not supported!')
    % Function terminates
end
%%%%% END IMPORTANT SETUP %%%%%


% Run function to import all data from the binary file. If you change the 
% name or want to read more files, you must change the function 
% accordingly.
[samples, nomTp, rawData] = raspiImport(path,channels);

%% Plot all raw data and corresponding amplitude response
%%%%% Plot all raw data %%%%%
fh_raw = figure;    % fig handle
plot(rawData,'-o');
ylim([0, 4095]) % 12 bit ADC gives values in range [0, 4095]
xlabel('sample');
ylabel('conversion value');
legendStr = cell(1,channels);
for i = 1:channels
    legendStr{1,i} = ['ch. ' num2str(i)];
end
legend(legendStr,'location','best');
title('Raw ADC data');
%%%%% Finish plot all raw data %%%%%


%%%%% Plot data as function of time %%%%%
% ...
%%%%% Finish plot data as function of time %%%%%


%%%%% Take FFT of data and plot amplitude response %%%%%
y = linspace(0,27720,31250);
%plot(y,abs(fft(rawData)));
%ylim([0,15000000]);
%xlabel('Hz');

fs = 27700;
timePeriod = 1/fs;
kryssKorr1 = xcorr(rawData(:,4)-2047, rawData(:,3)-2047);
kryssKorr2 = xcorr(rawData(:,5)-2047, rawData(:,3)-2047);
kryssKorr3 = xcorr(rawData(:,5)-2047, rawData(:,4)-2047);

[maxValue1, maxPosition1] = max(kryssKorr1);
forsinkelse1 = maxPosition1 - (length(kryssKorr1)+1)/2;
t4_3 = forsinkelse1*timePeriod;

[maxValue2, maxPosition2] = max(kryssKorr2);
forsinkelse2 = maxPosition2 - (length(kryssKorr2)+1)/2;
t5_3 = forsinkelse2*timePeriod;

[maxValue3, maxPosition3] = max(kryssKorr3);
forsinkelse3 = maxPosition3 - (length(kryssKorr3)+1)/2;
t5_4 = forsinkelse3*timePeriod;

%t1 = 0;
%t2 = 0.001;
%t3 = 0.001;


teta = atan(sqrt(3)*(t4_3+t5_3)/(t4_3-t5_3-2*t5_4));
tetaDeg = teta*180/pi;

figure
subplot(3,1,1)   
plot(kryssKorr1)
xlim([25000,35000]);
title('Subplot 1')
subplot(3,1,2)  
plot(kryssKorr2)   
xlim([25000,35000]);
title('Subplot 2')
subplot(3,1,3)       
plot(kryssKorr3)    
xlim([25000,35000]);
title('Subplot 3')


%%%%% Finish take FFT of data and plot amplitude response %%%%%


