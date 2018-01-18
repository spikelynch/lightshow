#!/usr/bin/env python

import pyaudio

p = pyaudio.PyAudio()
for i in range(p.get_device_count()):
    dev = p.get_device_info_by_index(i)
    line = "{} {} {}".format(i, dev['name'], dev['maxInputChannels'])
    if "USB" in dev['name']:
        line += " <= *This looks good*"
    print(line)
