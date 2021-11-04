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
from wave_channel import wav_channel_reader, convert_wav_to_mono

def main(wav_file_name, output_directory, output_file_name, channel):
    """Split the Wave."""
    try:
        wf = wave.open(wav_file_name, "rb")
    except wave.Error as wave_except:
        print(f'Error Opening {wav_file_name} : {str(wave_except)}', file=sys.stderr)
    # check for non-mono wavs and convert them, else output message
    if can_be_split(wf):
        convert_wav_to_mono(wf, output_directory, output_file_name, channel)
        print ("Converted to " + output_file_name)
    else:
        print (wav_file_name + " wav is already mono")
    wf.close

def can_be_split(wf: wave.Wave_read) -> bool:
    """Determine if a Wave_read object can be split into multiple channels."""
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        return True
    else:
        return False

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
    parser.add_argument("--channel",
                       help="which channel to keep",
                       type=int, 
                       default=1)
    args = parser.parse_args()
    create_output_dir(args.output_directory)
    main(args.wav_file, args.output_directory, args.output_file_name, args.channel)