import wave

class wav_channel_reader:
    
    def __init__(self, wave_read: wave.Wave_read, channel):
        """YEAH."""
        self.audio_bytes = bytearray(wave_read.readframes(wave_read.getnframes()))
        self.num_channels = wave_read.getnchannels()
        self.bytes_per_sample = wave_read.getsampwidth()
        self.channel = channel # Which of the channels in the wave is going to be _this_ channel
        if(channel in range(0, wave_read.getnchannels())):
            self.channel = channel
        else:
            raise ValueError(f'There is no channel {channel}.  {wave_read} only contains {wave_read.getnchannels} channels')

    def __iter__(self):
        """Yield the next byte from the channel."""
        # for index in range(self.channel - 1, len(self.audio_bytes), int((self.num_channels * self.bytes_per_sample))):
        for index in range(self.channel - 1, len(self.audio_bytes), 8):

            # mono_sample = self.audio_bytes[index:int(index+(self.bytes_per_sample/self.num_channels)+1)]
            mono_sample = self.audio_bytes[int(index):int(index+(self.bytes_per_sample/self.num_channels)+1)]
        
            yield mono_sample

    # def __next__(self):
    #     x = self.a
    #     self.a += 1
    #     return x