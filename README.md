# Lightshow

A quick frequency-spectrum analyser for Holiday programmable LED lights, or the command line, or anything else you care to add.

Uses the PyAudio package to read data from an audio input, and runs numpy's
FFT to generate frequency spectrum data, which it then sends to an object
implementing a method render().

This package includes two renderers:

* AsciiSpectrum writes an ascii-art spectrum to the command line as a debugging aid
* HolidaySpectrum sends colours to a set of Holiday lights over your wifi

