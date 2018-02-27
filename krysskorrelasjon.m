numSamples = 100;
delay = 12;
fs = 27700;
timePeriod = 1/fs;

x = 0:0.01:5;
y = 1:0.01:5;


%signal1 = sin(x);
%signal2 = sin(y);

signal1 = zeros(1,numSamples);
signal2 = zeros(1,numSamples);

signal2(1) = 1;
signal1(delay+1) = 1;

kryssKorr = xcorr(signal1, signal2);

%figure
%subplot(3,1,1)       % add first plot in 2 x 1 grid
%plot(y,signal2)
%title('Subplot 1')

%subplot(3,1,2)       % add second plot in 2 x 1 grid
%plot(x,signal1)       % plot using + markers
%title('Subplot 2')

%subplot(3,1,3)       % add second plot in 2 x 1 grid
plot(kryssKorr);       % plot using + markers
%title('Subplot 2')

[maxValue, maxPosition] = max(kryssKorr);
forsinkelse = abs(maxPosition - (length(kryssKorr)+1)/2);

effektivForsinkelse = forsinkelse*timePeriod;

