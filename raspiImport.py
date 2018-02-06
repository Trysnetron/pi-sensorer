import numpy as np

def raspiImport(path, channels):
    with open(path, 'rb') as file:
        samplePeriod = np.fromFile(path, dtype=float, count=1) * 1.0e-06
        adcData = np.fromFile(path, dtype=int)
    
        sampleNumber = len(adcData) / channels
        rawData = np.zeros(sampleNumber)
        for i in range(0, sampleNumber - 1):
            for j in range(0, channels - 1):
                rawData[i, j] = adcData[i * channels + j]

        return rawData

sampleData = raspiImport('samples.bin', 5)

print(sampleData[0, 0])