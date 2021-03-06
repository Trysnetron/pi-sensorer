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
for i = 1:4000
   rawData(i,1)=0; 
   rawData(i,2)=0; 
end
for i = 1:13000
   rawData(i,1)=0; 
   rawData(i,2)=0; 
end
%for i = 10000:31250
%   rawData(i,1)=0; 
%   rawData(i,2)=0; 
%end
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
plot(y,abs(fft(rawData(:,1))));
ylim([0,15000000]);
xlim([5,1000]);
xlabel('Hz');

%mic1[312500];
I = 8;
xq = 1:1/I:31250;
x =1:1:31250; 

v=rawData(:,1);
mic1 = interp1(x, v, xq);

v=rawData(:,2);
mic2 = interp1(x, v, xq);

v=rawData(:,3);
mic3 = interp1(x, v, xq);

fs = 27700;
timePeriod = 1/fs;
kryssKorr1 = xcorr(mic2-2047, mic1-2047);
kryssKorr2 = xcorr(mic3-2047, mic1-2047);
kryssKorr3 = xcorr(mic3-2047, mic2-2047);

[maxValue1, maxPosition1] = max(kryssKorr1);
forsinkelse1 = maxPosition1 - (length(kryssKorr1)+1)/2;
t2_1 = forsinkelse1*timePeriod;

[maxValue2, maxPosition2] = max(kryssKorr2);
forsinkelse2 = maxPosition2 - (length(kryssKorr2)+1)/2;
t3_1 = forsinkelse2*timePeriod;

[maxValue3, maxPosition3] = max(kryssKorr3);
forsinkelse3 = maxPosition3 - (length(kryssKorr3)+1)/2;
t3_2 = forsinkelse3*timePeriod;

%t1 = 0;
%t2 = 0.001;
%t3 = 0.001;


tetaRad = atan(sqrt(3)*(t2_1+t3_1)/(t2_1-t3_1-2*t3_2));
%tetaDeg = tetaRad*180/pi;
if (t3_2>=0)
        tetaDeg = tetaRad*180/pi+90;
else
        tetaDeg = tetaRad*180/pi+270;
end

%figure
%subplot(3,1,1)   
%plot(kryssKorr1)
%xlim([31000,600000]);
%title('Subplot 1')
%subplot(3,1,2)
%plot(kryssKorr2)
%xlim([0,600000]);
%title('Subplot 2')
%subplot(3,1,3)       
%plot(kryssKorr3)    
%xlim([31000,600000]);
%title('Subplot 3')


%%%%% Finish take FFT of data and plot amplitude response %%%%%


