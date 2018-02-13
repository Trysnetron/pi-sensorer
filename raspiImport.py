import numpy as np

def raspiImport(path, channels):
	resolution = 4096
	sample_period = np.fromfile(path, dtype="double", count=1) * 1.0e-06
	adc_data = np.fromfile(path, dtype="uint16")
	adc_data = np.delete(adc_data, [0, 1, 2, 3])

	sample_number = int(len(adc_data) / channels)
	print(str(sample_number) + " samples per channel")
    
	samples = []
	for i in range(0, channels):
		current_channel_samples = np.zeros(sample_number)
		for j in range(0, sample_number):
			current_channel_samples[j] = adc_data[i * channels + j] - resolution / 2
		samples.append(current_channel_samples)

	return samples

sample_data = raspiImport("./samples.bin", 5)

print(sample_data)
