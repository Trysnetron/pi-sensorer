import numpy as np

def raspiImport(path, channels):
    with open(path, 'rb') as file:
        samplePeriod = np.fromfile(path, dtype="double", count=1) * 1.0e-06
        adcData = np.fromfile(path, dtype="uint16")
	
        sampleNumber = len(adcData) / channels
        rawData = np.zeros(int(sampleNumber))
        for i in range(0, sampleNumber - 1):
            for j in range(0, channels - 1):
                rawData[i, j] = adcData[i * channels + j]

        return rawData
    return false

sampleData = raspiImport("./samples.bin", 5)

print(sampleData[0, 0])
