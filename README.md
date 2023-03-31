# Quick and Dirty audio degrader
#
Simple GUI program, that allows degrading (downsampling and bit decimation) of audio samples. Coded in Python, and compatible with MacOS, Windows and Linux.

One of the more difficult sounds to capture with modern sound equipment and Digital Audio Workstations is the sound of classic samplers. Although the characteristics of any sampler's output are hard to replicate, it's pretty easy to replicate the digital files they use. Often they record samples at less then the CD audio standard of 16bit/44.1kHz; often 8/12 bits and under 32kHz. This program allows you to take one or more `.wav`, `.aiff` or `.mp3` files, degrade to user selected values, and outputs them as `.wav` or `.aiff`.