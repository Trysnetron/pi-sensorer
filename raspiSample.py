import sys
import subprocess
import numpy as np

assert sys.version_info >= (3, 0)

def sample(path, sample_number):
	resolution = 4096
	channels = 5
	
	subprocess.run(["sudo", "./adc_sampler", str(sample_number)])

	sample_period = np.fromfile(path, dtype="double", count=1) * 1.0e-06
	adc_data = np.fromfile(path, dtype="uint16")
	adc_data = np.delete(adc_data, [0, 1, 2, 3])

	print(str(sample_number) + " samples per channel")
    
	samples = []
	for i in range(0, channels):
		current_channel_samples = np.zeros(sample_number)
		for j in range(0, sample_number):
			current_channel_samples[j] = adc_data[i * channels + j] - resolution / 2
		samples.append(current_channel_samples)

	return samples
