#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import sys
sys.path.append('../src')

import cv, cv2

from pke.video import Video
#from pke.shot_transition_detection.basic_histogram_change import get_shots 
from pke.shot_transition_detection.histogram_part_change import get_shots 
from pke.gui import display_2_frames
from pke.keyframe_detection.basic_keyframe_detection import get_keyframe

if len(sys.argv) != 2:
    print "Usage: ./example.py video"
    sys.exit(0)

video = Video(filepath = sys.argv[1])

#shots = get_shots(video, 0.9)
shots = get_shots(video, (20, 20), 0.9, 150)
print("shots : " + str(len(shots)))

for i in range(len(shots) - 1):
    display_2_frames(shots[i][-1], shots[i + 1][0])

