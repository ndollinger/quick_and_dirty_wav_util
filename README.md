# quick_and_dirty_wav_util

Quick and Dirty command line utility for performing operations on .wav files.

Currently, the following operations are supported:

- Split the channels of a stereo wav to a mono wave

## Usage

```console
usage: wav_split.py [-h] [--output_directory OUTPUT_DIRECTORY] [--output_file_name OUTPUT_FILE_NAME] [--channel CHANNEL] wav_file

Create a Mono .wav from a Stereo .wav

positional arguments:
  wav_file              File Name of Wav file to translate

optional arguments:
  -h, --help            show this help message and exit
  --output_directory OUTPUT_DIRECTORY
                        Directory where split wave files end up
  --output_file_name OUTPUT_FILE_NAME, -o OUTPUT_FILE_NAME
                        File name of the newly created mono wave file. If not supplied, the output file is the
                        input file name with the channel appended to the file name.
  --channel CHANNEL     which channel to keep
```

## Prerequisites

`todo`
