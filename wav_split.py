#!/usr/bin/env python3

import sys
import os
import wave
import json
import uuid
import argparse
from time import perf_counter

def main(args):

    # TODO: reimplement this using argparse, I don't recall why I took this out
    # parser = argparse.ArgumentParser()
    # parser.add_argument("wav_file", help="File Name of Wav file to translate")
    # parser.parse_args()
    wav_file_name = sys.argv[1]

    wf = wave.open(wav_file_name, "rb")
    # check for non-mono wavs and convert them, else output message
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        temp_wave_file_name = convert_wav_to_mono(wf)
        print ("Converted to " + temp_wave_file_name)
    else:
        print (wav_file_name + "wav is already mono")


# There is surely a better way to do this than the below.
# Looping through all the frames is needlessly slow
def convert_wav_to_mono(wave_file):
    # only going to keep one of the channels
    # TODO: Make it configurable which channel to keep

    mono_wave_file_name = str(uuid.uuid4().int) + ".wav"
    mono_wave = wave.open(mono_wave_file_name,"wb")
    params = wave_file.getparams()
    mono_wave.setparams(params)
    mono_wave.setnchannels(1)

    # The data is the individual samples. An individual sample is the bit size times the number of channels. 
    # For example, a monaural (single channel), eight bit recording has an individual sample size of 8 bits. 
    # A monaural sixteen-bit recording has an individual sample size of 16 bits. 
    # A stereo sixteen-bit recording has an individual sample size of 32 bits.

    # Samples are placed end-to-end to form the data. 
    # So, for example, if you have four samples (s1, s2, s3, s4) then the data would look like: s1s2s3s4.
    
    # Keep track of time required to make the conversion
    start_time = perf_counter()

    for sound_pos in range(0,wave_file.getnframes(),2):
        wave_file.setpos(sound_pos)
        # It is best to first set all parameters, perhaps possibly the
        # compression type, and then write audio frames using writeframesraw.
        # When all frames have been written, either call writeframes(b'') or
        # close() to patch up the sizes in the header.
        mono_wave.writeframesraw(wave_file.readframes(1))
    mono_wave.close() # done writing to this thing, have to create a Wave_read object later

    print("Conversion completed in: ", perf_counter() - start_time, "seconds")

    return mono_wave_file_name

if __name__ == '__main__':
    main(sys.argv[1:])