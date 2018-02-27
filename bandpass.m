f1 = 1000;
f2 = 10000;
fs = 27000;

d = fdesign.bandpass('N,F3dB1,F3dB2',10,f1,f2,fs);
Hd = design(d,'butter');

fvtool(Hd);