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

def main(wav_file_name, output_directory, output_file_name):
    """Split the Wave."""
    try:
        wf = wave.open(wav_file_name, "rb")
    except wave.Error as wave_except:
        print(f'Error Opening {wav_file_name} : {str(wave_except)}', file=sys.stderr)
    # check for non-mono wavs and convert them, else output message
    if can_be_split(wf):
        convert_wav_to_mono(wf, output_directory, output_file_name)
        print ("Converted to " + output_file_name)
    else:
        print (wav_file_name + " wav is already mono")
    wf.close

def can_be_split(wf: wave.Wave_read) -> bool:
    """Detrmine if a Wave_read object can be split into multiple channels."""
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        return True
    else:
        return False

def convert_wav_to_mono(wave_file:wave.Wave_read, output_directory: str, mono_wave_file_name: str):
    """convert_wav_to_mono."""
    # only going to keep one of the channels

    print(f'There are {wave_file.getsampwidth()} bytes per sample in this wave')
    print(f'The sampling frequency is {wave_file.getframerate()}')

    # TODO: Make it configurable which channel to keep

    mono_wave = wave.open(f'{output_directory}/{mono_wave_file_name}',"wb")
    params = wave_file.getparams()
    mono_wave.setparams(params)
    mono_wave.setnchannels(1)
    mono_wave.setsampwidth(2) # TODO: this is not _always_ going to be the case
    mono_wave.setframerate(int(wave_file.getframerate()/2))
    
    # Keep track of time required to make the conversion
    start_time = perf_counter()
 
    mono_wave_bytes = get_one_channel(wave_file)

    mono_wave.writeframesraw(mono_wave_bytes)
    mono_wave.close() # done writing to this thing, have to create a Wave_read object later

    print("Conversion completed in: ", perf_counter() - start_time, "seconds")

    return mono_wave_file_name

def get_one_channel(wave_file: wave.Wave_read) -> bytearray:
    """Do the actual job of splitting out one channel."""
    mono_wave_bytes = bytearray()
    channel=wav_channel_reader(wave_file, 1)
    for data_bytes in channel:
        mono_wave_bytes += data_bytes
    mono_wave_bytes += b'\x01' # TODO Padding byte if M*Nc*Ns is odd, else 0
    return mono_wave_bytes 

def create_output_dir(output_dir: str):
    """Create a dir to output generated waves if it doesn't already exist."""
    try:
        os.mkdir(output_dir)
    except FileExistsError:
        pass # Suppress the exception

if __name__ == '__main__':
    default_output_dir = "generated_waves"
    parser = argparse.ArgumentParser(description='Create a Mono .wav from a Stereo .wav')
    parser.add_argument("wav_file", 
                        help="File Name of Wav file to translate",
                        type=str)
    parser.add_argument("--output_directory",
                       help="Directory where split wave files end up",
                       type=str, 
                       default=default_output_dir)
    parser.add_argument("--output_file_name",
                        "-o",
                        help="File name of the newly created mono wave file",
                        type=str,
                        default=str(uuid.uuid4().int) + ".wav")
    args = parser.parse_args()
    create_output_dir(args.output_directory)
    main(args.wav_file, args.output_directory, args.output_file_name)