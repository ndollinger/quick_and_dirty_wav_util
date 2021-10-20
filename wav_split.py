"""wav_split.py.

Converts a Stereo wav into a mono wav.

One channel is discarded

"""
#!/usr/bin/env python3

import sys
import wave
import uuid
import argparse
import os
from time import perf_counter
from functools import reduce
from wave_channel import wav_channel_reader

def main(wav_file_name, output_directory):
    """Split the Wave."""
    try:
        wf = wave.open(wav_file_name, "rb")
    except wave.Error as wave_except:
        print(f'Error Opening {wav_file_name} : {str(wave_except)}', file=sys.stderr)
    # check for non-mono wavs and convert them, else output message
    if can_be_split(wf):
        temp_wave_file_name = convert_wav_to_mono(wf, output_directory)
        print ("Converted to " + temp_wave_file_name)
    else:
        print (wav_file_name + " wav is already mono")
    wf.close

def can_be_split(wf: wave.Wave_read) -> bool:
    """Detrmine if a Wave_read object can be split into multiple channels."""
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        return True
    else:
        return False

# There is surely a better way to do this than the below.
# Looping through all the frames is needlessly slow
def convert_wav_to_mono(wave_file, output_directory):
    """convert_wav_to_mono."""
    # only going to keep one of the channels

    print(f'There are {wave_file.getsampwidth()} bytes per sample in this wave')
    print(f'The sampling frequency is {wave_file.getframerate()}')

    # TODO: Make it configurable which channel to keep

    mono_wave_file_name = str(uuid.uuid4().int) + ".wav"
    mono_wave = wave.open(f'{output_directory}/{mono_wave_file_name}',"wb")
    params = wave_file.getparams()
    mono_wave.setparams(params)
    mono_wave.setnchannels(1)
    mono_wave.setsampwidth(2) # TODO: this is not _always_ going to be the case
    mono_wave.setframerate(int(wave_file.getframerate()/2))


    # Wav file references
    # https://wavefilegem.com/how_wave_files_work.html

    # The data is the individual samples. An individual sample is the bit size times the number of channels. 
    # For example, a monaural (single channel), eight bit recording has an individual sample size of 8 bits. 
    # A monaural sixteen-bit recording has an individual sample size of 16 bits. 
    # A stereo sixteen-bit recording has an individual sample size of 32 bits.

    # Samples are placed end-to-end to form the data. 
    # So, for example, if you have four samples (s1, s2, s3, s4) then the data would look like: s1s2s3s4.
    
    # Keep track of time required to make the conversion
    start_time = perf_counter()
 
    mono_wave_bytes = alt_get_one_channel(wave_file)

    mono_wave.writeframesraw(mono_wave_bytes)
    mono_wave.close() # done writing to this thing, have to create a Wave_read object later

    print("Conversion completed in: ", perf_counter() - start_time, "seconds")

    return mono_wave_file_name

def get_one_channel(wave_file: wave.Wave_read) -> bytearray:
    """Do the actual job of splitting out one channel."""
    mono_wave_bytes = bytearray()
    #for sound_pos in range(0,wave_file.getnframes(),2):
    for sound_pos in range(0,wave_file.getnframes(),2): # each frame has data from both channels, so don't skip any

        wave_file.setpos(sound_pos)
        # It is best to first set all parameters, perhaps possibly the
        # compression type, and then write audio frames using writeframesraw.
        # When all frames have been written, either call writeframes(b'') or
        # close() to patch up the sizes in the header.
        single_frame = wave_file.readframes(1)
        mono_frame = single_frame[0:2] # ignore the samples from the second channel? (maybe this should be 0 + 1?)
        #print(mono_frame)
        #mono_wave_bytes += bytearray(single_frame)
        mono_wave_bytes += bytearray(mono_frame)
    return mono_wave_bytes  

def alt_get_one_channel(wave_file: wave.Wave_read) -> bytearray:
    """Do the actual job of splitting out one channel."""
    mono_wave_bytes = bytearray()
    channel=wav_channel_reader(wave_file, 1)
    for data_bytes in channel:
        mono_wave_bytes += data_bytes
        #print(data_bytes)
    mono_wave_bytes += b'\x01' # TODO Padding byte if M*Nc*Ns is odd, else 0
    return mono_wave_bytes 

def create_output_dir(output_dir: str):
    """Create a dir to output generated waves if it doesn't already exist."""
    try:
        os.mkdir(output_dir)
    except FileExistsError:
        pass # This is kind of expected, maybe do something clever eventually

if __name__ == '__main__':
    default_output_dir = "generated_waves"
    parser = argparse.ArgumentParser(description='Create a Mono .wav from a Stereo .wav')
    parser.add_argument("wav_file", 
                        help="File Name of Wav file to translate",
                        type=str)
    parser.add_argument("--output_directory",
                       help="Directory to output split wave file to",
                       type=str, 
                       default=default_output_dir)
    args = parser.parse_args()
    wav_file_name = args.wav_file
    output_dir = args.output_directory
    create_output_dir(output_dir)
    main(wav_file_name, output_dir)