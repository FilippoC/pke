#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import sys
sys.path.append('../src')

import cv, cv2
import matplotlib.pyplot as plt

from pke.content.histogram import get_partitions
from pke.selection.optical_flow import get_frames

from pke.video import Video
from pke.gui import display_frame


if len(sys.argv) != 2:
    print "Usage: ./example.py video"
    sys.exit(0)



video = Video(filepath = sys.argv[1])

frames, function = get_partitions(video, (10, 10), 0.4, 30)

print(len(frames))

plt.plot(function)
plt.show()

for i in range(len(frames)):
    frame = get_frames(frames[i])[0]
    display_frame(frame)

