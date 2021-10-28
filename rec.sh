#!/bin/sh -e
# This script tells the RTL-SDR dongle to sample I/Q data 
# at 256 kSps, then FM-demodulates those data, and converts
# to an audio file (WAV format) with sample rate 10 kSps.
# Sampling lasts for 10 minutes, which is the duration of
# the best reception window for a typical NOAA 19 pass.
# If you have a particularly good antenna, you could sample
# for up to 15 minutes.
cd /home/pi

### Delay while boot completely finishes
sleep 10s

### Increment counter to prevent output file overwrite
# Note: /home/pi must contain counter.txt file
read -r count < counter.txt
file_OUT="rec${count}.wav"
file_OUT_10k="rec${count}_10k.wav"
num=$((count+1))
echo $num > counter.txt

### record signal to WAV file
# timeout safely terminates rtl_fm after 10 minutes
# -f carrier frequency
# -s sample rate (256k is minimum)
# -g gain (50 is maximum)
# sox needs to be told format out rtl_fm output, which is
#     -t raw    (binary data)
#     -e signed (signed integers)
#     -c 1      (single channel)
#     -b 16     (16-bit)
#     -r 256k   (sampled at 256kSps)
timeout 10m rtl_fm -f 137.1M -s 256k -g 50 - | sox -t raw -e signed -c 1 -b 16 -r 256k - $file_OUT

### Downsample to minimise file size for speedy transfer
sox $file_OUT $file_OUT_10k rate 10k
