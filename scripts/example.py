#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import sys
sys.path.append('../src')

import cv, cv2

from pke.video import Video
from pke.shot_transition_detection.basic_histogram_change import get_shots 
from pke.gui import display_2_frames
from pke.keyframe_detection.basic_keyframe_detection import get_keyframe

if len(sys.argv) != 2:
    print "Usage: ./example.py video"
    sys.exit(0)

video = Video(filepath = sys.argv[1])

shots = get_shots(video)

keyframes = []
for i in xrange(len(shots)):
    print("Computing keyframe " + str(i + 1) + "/" + str(len(shots)))
    keyframes.append(get_keyframe(shots[i]))

for best, worst in keyframes:
    display_2_frames(best, worst)
