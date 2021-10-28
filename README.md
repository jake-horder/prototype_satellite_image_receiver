# prototype_satellite_image_receiver

## Contents
The file `15_10_21.wav` contains an FM-demodulated recording of a pass of the NOAA 19 satellite taken in Sydney, Australia on 15 October 2021 at roughly 8 pm AEDST. The pass takes about 15 minutes, but only around 7 minutes of the recording was worth saving due to a delayed start and noise at the end as the satellite neared the horizon. This WAV file was obtained with the use of a home-made QFH antenna optimised for 137.1 MHz, an RTL-SDR Blog V3 device, and the `GQRX` software running on a 2015 Macbook Air (Mojave).

The python script `wav_to_img.py` does everything necessary to take as input `15_10_21.wav` and produce as output the included `PNG` images. The script contains enough commenting that you should be able to augment it to plot images from your own recordings. One downside is the amount of trial and error required to slice up the data into channels and perform contrast enhancement - but it is still easier than trying to figure out how to use `WxToImg`!

For completeness, this repository includes the bash script `rec.sh` and the file `rc.local` which allows automatic recording from boot on a headless Raspberry Pi that has the command line applications `rtl-fm` and `sox` installed. If you are using a Raspberry Pi, it might be worth using an additional low noise amplifier unit inbetween your antenna and SDR device.
