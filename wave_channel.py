"""Classes and Method to evaluate and manipulate the channels of wave files.

Classes:
    wav_channel_reader

Methods:
    convert_wave_to_mono
    get_one_channel

"""

import wave
from time import perf_counter
import os

def convert_wav_to_mono(wave_file:wave.Wave_read, output_directory: str, mono_wave_file_name: str, channel_num: int):
    """convert_wav_to_mono."""
    # only going to keep one of the channels

    print(f'There are {wave_file.getsampwidth()} bytes per sample in this wave')
    print(f'The sampling frequency is {wave_file.getframerate()}')

    # TODO: Make it configurable which channel to keep

    # This is an extremely large `try` block, but once the `wave.open` runs it will create a new file on disk which we don't want to be there in the case something goes wrong writing the bytes etc.
    try:
        mono_wave = wave.open(f'{output_directory}/{mono_wave_file_name}',"wb")
        params = wave_file.getparams()
        mono_wave.setparams(params)
        mono_wave.setnchannels(1)
        mono_wave.setsampwidth(2) # TODO: this is not _always_ going to be the case
        mono_wave.setframerate(int(wave_file.getframerate()/2)) # TODO: Likewise, not always the case
    
        # Keep track of time required to make the conversion
        start_time = perf_counter()
 
        mono_wave_bytes = get_one_channel(wave_file, channel_num)

        mono_wave.writeframesraw(mono_wave_bytes)
        mono_wave.close() # done writing to this thing, have to create a Wave_read object later
    except:
        os.remove(f'{output_directory}/{mono_wave_file_name}')
        raise

    print("Conversion completed in: ", perf_counter() - start_time, "seconds")

    return mono_wave_file_name

def get_one_channel(wave_file: wave.Wave_read, channel_num=1) -> bytearray:
    """Do the actual job of splitting out one channel."""
    mono_wave_bytes = bytearray()
    channel=wav_channel_reader(wave_file, channel_num)
    for data_bytes in channel:
        mono_wave_bytes += data_bytes
    mono_wave_bytes += b'\x01' # TODO Padding byte if M*Nc*Ns is odd, else 0
    return mono_wave_bytes 

class wav_channel_reader:
    """Wave Channel Reader.

    Act as an interface to the sound bytes of a single channel of a wav file.    

    Methods:
        __iter__ - allows for iteration through the bytes of the channel of the wave file.
    """
    
    def __init__(self, wave_read: wave.Wave_read, channel):
        """Create a new wave_channel_reader.
        
        Parameters:
            wave_read - a Wave_read object
            channel - passed int idicating which audio channel this obj repr.

        Raises:
            InvalidWavChannel - Raised if the "channel" parameter indicates a channel that doesn't exist in the passed Wave_read object.

        """
        self.audio_bytes = bytearray(wave_read.readframes(wave_read.getnframes()))
        self.num_channels = wave_read.getnchannels()
        self.bytes_per_sample = wave_read.getsampwidth()
        self.channel = channel # Set which of the channels in the wave is going to be _this_ channel
        if(channel in range(0, wave_read.getnchannels())):
            self.channel = channel
        else:
            raise InvalidWaveChannel(f'There is no channel {channel}.  {wave_read} only contains {wave_read.getnchannels()} channels')

    def __iter__(self):
        """Yield the next byte from the channel."""
        # Wav file references
        # https://wavefilegem.com/how_wave_files_work.html

        # The data is the individual samples. An individual sample is the bit size times the number of channels. 
        # For example, a monaural (single channel), eight bit recording has an individual sample size of 8 bits. 
        # A monaural sixteen-bit recording has an individual sample size of 16 bits. 
        # A stereo sixteen-bit recording has an individual sample size of 32 bits.

        # Samples are placed end-to-end to form the data. 
        # So, for example, if you have four samples (s1, s2, s3, s4) then the data would look like: s1s2s3s4.
        
        for index in range(self.channel*8, len(self.audio_bytes), 8):
            mono_sample = self.audio_bytes[int(index):int(index+(self.bytes_per_sample/self.num_channels)+1)]
            yield mono_sample

class InvalidWaveChannel(Exception):
    """Exception for use with working with wav file channels. Raised in the case a channel that doesn't exist is accessed."""
    
    pass