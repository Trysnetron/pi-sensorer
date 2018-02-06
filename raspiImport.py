import numpy as np

def raspiImport(path, channels):
    with open(path, 'rb') as file:
        samplePeriod = np.fromFile(path, dtype=double, count=1) * 1.0e-06
        adcData = np.fromFile(path, dtype=uint16)
    
    sampleNumber = len(adcData) / channels
    rawData = np.zeros(sampleNumber)
    for i in range(0, sampleNumber - 1):
        for j in range(0, channels - 1):
            rawData[i, j] = adcData[i * channels + j]
            
print("ja")