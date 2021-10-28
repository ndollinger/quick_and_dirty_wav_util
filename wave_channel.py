"""Classes and Method to evaluate and manipulate the channels of wave files.

Classes:

    wav_channel_reader
"""

import wave

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
            ValueError - Raised if the "channel" parameter indicates a channel that doesn't exist in the passed Wave_read object.

        """
        self.audio_bytes = bytearray(wave_read.readframes(wave_read.getnframes()))
        self.num_channels = wave_read.getnchannels()
        self.bytes_per_sample = wave_read.getsampwidth()
        self.channel = channel # Set which of the channels in the wave is going to be _this_ channel
        if(channel in range(0, wave_read.getnchannels())):
            self.channel = channel
        else:
            raise ValueError(f'There is no channel {channel}.  {wave_read} only contains {wave_read.getnchannels} channels')

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
        
        for index in range(self.channel - 1, len(self.audio_bytes), 8):
            mono_sample = self.audio_bytes[int(index):int(index+(self.bytes_per_sample/self.num_channels)+1)]
            yield mono_sample
