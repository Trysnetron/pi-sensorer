"""
Read the input video file, display first frame and ask the user to select a
region of interest.  Will then calculate the mean of each frame within the ROI,
and return the means of each frame, for each color channel, which is written to
file.

Similar to read_video_and_extract_roi.m, but for Python.

Requirements:

* Probably ffmpeg. Install it through your package manager.
* numpy
* OpenCV python package.
    For some reason, the default packages in Debian/Raspian (python-opencv and
    python3-opencv) seem to miss some important features (selectROI not present
    in python3 package, python2.7 package not compiled with FFMPEG support), so
    install them (locally for your user) using pip:
    - pip install opencv-python
    - (or pip3 install opencv-python)
"""
import sys
import numpy as np

# Constants
CROP_SIZE = 128

BPM_MIN = 30
BPM_MAX = 300

# Variables
source_file = ""

# Utility functions
def autocorrelation(x):
	result = np.correlate(x, x, mode="full")
	return result[int(len(result)/2):]

def spectrum(x):
	result = np.abs(np.fft.fft(x))
	return result[:int(len(result) / 2)]

def spectrumIndexToBPM(index, length, fps):
	return index / length * fps / 2 * 60

def hpfilter(signal):
	filtered_signal = np.zeros(len(signal) - 1)
	for i in range(0, len(signal) - 1):
	 	filtered_signal[i] = signal[i + 1] - signal[i];
	return filtered_signal


# CLI options
if len(sys.argv) > 1:
	source_file = sys.argv[1]
else:
	print("[ERROR] " + sys.argv[0] + " needs a target file.\nTry writing '" + sys.argv[0] + " [filename]'.")
	exit()

# Define color channels
signal_red = []
signal_green = []
signal_blue = []

sample_num = 0
sample_rate = 40 # Default value

#################################
##### Read from source file #####
#################################

if (source_file.endswith(".txt")):
	# Read data from text file
	print("Reading data from txt file.")

	mean_signal = np.loadtxt(source_file)
	sample_num = len(mean_signal)

	signal_red = np.zeros(sample_num)
	signal_green = np.zeros(sample_num)
	signal_blue = np.zeros(sample_num)	

	for i in range(0, len(mean_signal)):
		signal_red[i] = mean_signal[i][0]
		signal_green[i] = mean_signal[i][1]
		signal_blue[i] = mean_signal[i][2]
	
elif (source_file.endswith(".mp4")):
	# Read video file
	
	# Needs cv2 module for this
	try:
		import cv2
	except ImportError:
		print("[ERROR] OpenCV is not installed. Please install it.")
		exit()

	cap = cv2.VideoCapture(source_file, cv2.CAP_FFMPEG)
	if not cap.isOpened():
		print("[ERROR] Could not open input file. Wrong filename, or your OpenCV package might not be built with FFMPEG support. See docstring of this Python script.")
		exit()

	sample_num = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
	sample_rate = cap.get(cv2.CAP_PROP_FPS)

	mean_signal = np.zeros((sample_num, 3))

	# Loop through the video
	count = 0
	while cap.isOpened():
		ret, frame = cap.read() #'frame' is a normal numpy array of dimensions [height, width, 3], in order BGR
		if not ret:
			break

		if count == 0:
			frame_width = frame.shape[0]
			frame_height = frame.shape[1]
			region_of_interest = [int((frame_width - CROP_SIZE) / 2), int((frame_height - CROP_SIZE) / 2), CROP_SIZE, CROP_SIZE]
		#    window_text = 'Select ROI by dragging the mouse, and press SPACE or ENTER once satisfied.'
		#    ROI = cv2.selectROI(window_text, frame) #ROI contains: [x, y, w, h] for selected rectangle
		#    cv2.destroyWindow(window_text)
			print("Looping through video.")

		cropped_frame = frame[region_of_interest[1]:region_of_interest[1] + region_of_interest[3], region_of_interest[0]:region_of_interest[0] + region_of_interest[2], :]
		std = np.std(cropped_frame)
		mean_signal[count, :] = np.mean(cropped_frame, axis=(0,1))
		count = count + 1
		print("\rFrame " + str(count) + "/" + str(sample_num), end="")
		
	print()
	cap.release()

	signal_red = mean_signal[:, 2]
	signal_green = mean_signal[:, 1]
	signal_blue = mean_signal[:, 0]

	if "-save" in sys.argv:
		output_file = source_file[:-4] + ".txt"
		np.savetxt(output_file, np.flip(mean_signal, 1))
		print("Data saved to '" + output_file + "', fps = " + str(sample_rate) + " frames/second")

else:
	print("[ERROR] File type not supported")
	exit()

########################
##### Analyze data #####
########################

# Standard deviation
sd_red = np.std(signal_red)
sd_green = np.std(signal_green)
sd_blue = np.std(signal_blue)
print("Standard deviations: r:" + str(sd_red) + " g: " + str(sd_green) + " b: " + str(sd_blue))

# rms (mean)
mean_red = np.mean(signal_red)
mean_green = np.mean(signal_green)
mean_blue = np.mean(signal_blue)
print("RMS: r:" + str(mean_red) + " g: " + str(mean_green) + " b: " + str(mean_blue))

print("-- Image quality SNR --\nr: " + str(mean_red/sd_red) + " g: " + str(mean_green / sd_green) + " b: " + str(mean_blue / sd_blue))

# Filters the signal through a high pass filter
filtered_signal_red = hpfilter(signal_red)
filtered_signal_green = hpfilter(signal_green)
filtered_signal_blue = hpfilter(signal_blue)

#autocorr_red = autocorrelation(filtered_signal_red)
#autocorr_green = autocorrelation(filtered_signal_green)
#autocorr_blue = autocorrelation(filtered_signal_blue)

spectrum_red = spectrum(filtered_signal_red)
spectrum_green = spectrum(filtered_signal_green)
spectrum_blue = spectrum(filtered_signal_blue)
spectrum_length = len(spectrum_red)
spectrum_range = np.zeros(len(spectrum_red))
peak_red = np.argmax(spectrum_red)
peak_green = np.argmax(spectrum_green)
peak_blue = np.argmax(spectrum_blue)

print("Red pulse: " + str(spectrumIndexToBPM(peak_red, spectrum_length, sample_rate)) + " BPM")
print("Green pulse: " + str(spectrumIndexToBPM(peak_green, spectrum_length, sample_rate)) + " BPM")
print("Blue pulse: " + str(spectrumIndexToBPM(peak_blue, spectrum_length, sample_rate)) + " BPM")

peak_height_red = spectrum(signal_red)[peak_red]
print("Pulse signal amplitude (red): " + str(peak_height_red * 2))

cropped_spectrum_red = spectrum_red[int(BPM_MIN * spectrum_length * 2 / sample_rate / 60):int(BPM_MAX * spectrum_length * 2 / sample_rate / 60)]
cropped_spectrum_green = spectrum_green[int(BPM_MIN * spectrum_length * 2 / sample_rate / 60):int(BPM_MAX * spectrum_length * 2 / sample_rate / 60)]
cropped_spectrum_blue = spectrum_blue[int(BPM_MIN * spectrum_length * 2 / sample_rate / 60):int(BPM_MAX * spectrum_length * 2 / sample_rate / 60)]
cropped_spectrum_length = len(cropped_spectrum_red)
cropped_spectrum_range = np.zeros(cropped_spectrum_length)
for i in range(0, cropped_spectrum_length):
	cropped_spectrum_range[i] = i * (BPM_MAX - BPM_MIN) / cropped_spectrum_length + BPM_MIN

if "-plot" in sys.argv:
	try:
		import matplotlib.pyplot as pp
	except ImportError:
		print("You need matplotlib to plot.")
		exit()

	pp.subplot(321)
	pp.plot(signal_red, "r")
	pp.subplot(322)
	pp.plot(spectrum_red, "r")
	
	pp.subplot(323)
	pp.plot(signal_green, "g")
	pp.subplot(324)
	pp.plot(spectrum_green, "g")
	
	pp.subplot(325)
	pp.plot(signal_blue, "b")
	pp.subplot(326)
	pp.plot(spectrum_blue, "b")
	
	pp.show()

print("Done")

#save to file in order R, G, B.
#np.savetxt(output_filename, np.flip(mean_signal, 1))
#print("Data saved to '" + output_filename + "', fps = " + str(fps) + " frames/second")