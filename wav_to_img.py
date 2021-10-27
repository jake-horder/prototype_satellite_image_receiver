'''
INPUT: WAV audio file
OUTPUT: Histogram and image of optical channel, and
        Histogram and image of IR channel.

DESCRIPTION:
This script takes as input a single-channel (mono, not stereo) audio file
in the WAV format. It then performs amplitude demodulation to obtain a
time series of the amplitude of the audio file. This amplitude time series
is then reshaped into a 2D image, which is sliced into the Optical (OP) 
Channel and Infra Red (IR) Channel. Contrast enhancement is then performed
on each slice, and images are plotted and saved in PNG format.

NOTE:
Variables that have been selected via visual inspection and trial and error
are labelled as being "selected manually". If you wish to import your own
WAV file, you will very likely need to change these values to suit your
recording.
'''


import scipy.io.wavfile as wav
import scipy.signal as signal
import numpy as np
import matplotlib.pyplot as plt



#%% Load and shape data

# Read recorded audio into numpy array
fs, data = wav.read('15_10_21.wav')

# Omit heavy static and recentre channels
data = data[1000:fs*60*7] # These values selected manually

# Use Hilbert transform to get audio envelope
# --> AKA AM demodulation
data = data - np.mean(data)
data_am = np.abs(signal.hilbert(data))

# Set dimensions of image
w = int(0.5*fs)   # half a second
h = data_am.shape[0]//w

# Reshape vector into 2D image array
IMG = np.reshape(data_am[:int(len(data_am)/w)*w], (h,w))

# Rotate image 180 deg if satellite path was south to north
IMG = np.fliplr(np.flipud(IMG))



#%% OP contrast enhance

# Select optical channel
IMG_OP = IMG[:,200:2300] # These values selected manually

# Reshape into 1D vector for histogram plotting
rz, cz = IMG_OP.shape
zv = np.reshape(IMG_OP, (1,rz*cz))

# Rescale upper bound
lim = 300 # This value selected manually
zv[zv>lim] = lim
zv = zv * 255 / lim

# Rescale lower bound
lim = 190 # This value selected manually
zv[zv<lim] = lim
zv = (zv-lim) * 255 / (255-lim)

# Plot histogram
plt.figure()
plt.hist(zv[0], 500)
plt.grid()
plt.xlim([0,255])
plt.ylim([0,12000])
plt.title('Optical Channel')
plt.xlabel('Pixel value [-]')
plt.ylabel('Count [-]')
plt.savefig('15_10_21_hist_OP.png')

# Reshape back into 2D image array and plot
IMG_OP = np.reshape(zv, (rz, cz))
plt.figure(figsize=(10,IMG_OP.shape[0]/100*1.5))
plt.imshow(IMG_OP, extent=[0,w,0,h], aspect='auto', cmap="bone")
plt.axis('off')
plt.savefig('15_10_21_OP.png')



#%% IR contrast enhance

# Select IR channel
IMG_IR = IMG[:,2700:4800] # These values selected manually

# Reshape into 1D vector for histogram plotting
rz, cz = IMG_IR.shape
zv = np.reshape(IMG_IR, (1,rz*cz))

# Rescale upper bound
lim = 260 # This value selected manually
zv[zv>lim] = lim
zv = zv * 255 / lim

# Rescale lower bound
lim = 100 # This value selected manually
zv[zv<lim] = lim
zv = (zv-lim) * 255 / (255-lim)

# Plot histogram
plt.figure()
plt.hist(zv[0], 500)
plt.grid()
plt.xlim([0,255])
plt.ylim([0,12000])
plt.title('Infra Red Channel')
plt.xlabel('Pixel value [-]')
plt.ylabel('Count [-]')
plt.savefig('15_10_21_hist_IR.png')

# Reshape back into 2D image array and plot
IMG_IR = np.reshape(zv, (rz, cz))
plt.figure(figsize=(10,IMG_IR.shape[0]/100*1.5))
plt.imshow(IMG_IR, extent=[0,w,0,h], aspect='auto', cmap="bone")
plt.axis('off')
plt.savefig('15_10_21_IR.png')
