"""Functions to evaluate and manipulate the channels of wave files.

Functions:
    convert_wave_to_mono: creates a new wave file with just one channel out of the passed wave.Wave_read files
    get_one_channel: returns one channel of audio bytes
    read_wave_channel: return an iterator to the bytes of the audio frames in the wav file
Classes:
    InvalidWaveChannel: Exception thrown when an attempt is made to access a channel the doesn't exist in the wave.Wave_read object
"""

import wave
from time import perf_counter
import os

def convert_wav_to_mono(wave_file:wave.Wave_read, output_directory: str, mono_wave_file_name: str, channel_num: int, verbose: int):
    """
    Create a new wave file on disk from one of the channels of the passed Wave_read object.

    Args:
        wave_file: a wave.Wave_read object that will have one audio channel read into a new file.  This object will not be manipulated
        output_directory: The directory on disk where the newly created mono wave file will be stored.
        mono_wave_file_name: name to use for the newly created mono wave file
        channel_num: the channel id of the channel that will be read into the new wave file
        verbose: if set, output additional information about the files and split time

    Returns:
        The name of the newly created wave file # TODO this doesn't really make sense
    """
    # only going to keep one of the channels
    if verbose:
        print(f'There are {wave_file.getsampwidth()} bytes per sample in this wave')
        print(f'The sampling frequency is {wave_file.getframerate()}')

    # TODO: Make it configurable which channel to keep

    # This is an extremely large `try` block, but once the `wave.open` runs it will create a new file on disk which we don't want to be there in the case something goes wrong writing the bytes etc.
    try:
        mono_wave = wave.open(f'{output_directory}/{mono_wave_file_name}',"wb")
        params = wave_file.getparams()
        mono_wave.setparams(params)
        mono_wave.setnchannels(1)
    
        # Keep track of time required to make the conversion
        start_time = perf_counter()
 
        mono_wave_bytes = get_one_channel(wave_file, channel_num)

        mono_wave.writeframesraw(mono_wave_bytes)
        mono_wave.close() # done writing to this thing, have to create a Wave_read object later
    except:
        os.remove(f'{output_directory}/{mono_wave_file_name}')
        raise

    if verbose: print("Conversion completed in: ", perf_counter() - start_time, "seconds")

    return mono_wave_file_name

def get_one_channel(wave_file: wave.Wave_read, channel_num=1) -> bytearray:
    """
    Split out one channel of audio data from the passed Wave_read object

    Args:
        wave_file: a wave.Wave_read object that will have one audio channel read into a new file.  This object will not be manipulated
        channel_num: Which channel's bytes to return

    Returns:
        A bytearray containing the audio frams for one channel of the passed Wave_read object
    """
    mono_wave_bytes = bytearray()
    for data_bytes in read_wave_channel(wave_file, channel_num):
        mono_wave_bytes += data_bytes
    mono_wave_bytes += b'\x01' # TODO Padding byte if M*Nc*Ns is odd, else 0
    return mono_wave_bytes 

def read_wave_channel(wave_file:wave.Wave_read, read_channel_index:int):
    """
    Generator that Yields the next byte from channel "read_channel_index" of the passed Wave_read object

    Args:
        wave_file: a wave.Wave_read object that will have one audio channel read into a new file.  This object will not be manipulated
        read_channel_index: Which channel's bytes to return

    Yields:
        bytes of one channel out of the entire sample
    """
    if(read_channel_index not in range(0, wave_file.getnchannels())):
        raise InvalidWaveChannel(f'There is no channel {read_channel_index}.  {wave_file} only contains {wave_file.getnchannels()} channels')
    
    audio_bytes = bytearray(wave_file.readframes(wave_file.getnframes()))

    # Wav file references
    # https://wavefilegem.com/how_wave_files_work.html

    # The data is the individual samples. An individual sample is the bit size times the number of channels. 
    # For example, a monaural (single channel), eight bit recording has an individual sample size of 8 bits. 
    # A monaural sixteen-bit recording has an individual sample size of 16 bits. 
    # A stereo sixteen-bit recording has an individual sample size of 32 bits.

    # Samples are placed end-to-end to form the data. 
    # So, for example, if you have four samples (s1, s2, s3, s4) then the data would look like: s1s2s3s4.
    # Multiple channels is like |s1ch1s1ch2|s2ch1s2ch2|s3ch1s3ch2|...    
    # therefore, the size of all the samples for all channels is the step size to step between the groups of samples
    size_of_one_sample_from_all_channels = wave_file.getsampwidth()*wave_file.getnchannels()
    # if we want channel 0, start at index 0, otherwise offset the start to align with the channel wanted
    first_index = read_channel_index*wave_file.getsampwidth()

    for index in range(first_index, len(audio_bytes), size_of_one_sample_from_all_channels):
        mono_sample = audio_bytes[index:index+wave_file.getsampwidth()]
        yield mono_sample

class InvalidWaveChannel(Exception):
    """Exception for use with working with wav file channels. Raised in the case a channel that doesn't exist is accessed."""
    
    pass