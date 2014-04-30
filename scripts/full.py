#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import sys
sys.path.append('../src')

import cv, cv2

from pke.video import Video

from pke.shot.histogram_part import get_shots 
from pke.content.histogram import get_partitions
from pke.selection.optical_flow import get_frames
from pke.post.shot_redundancy import get_post

if len(sys.argv) != 3:
    print "Usage: ./example.py video directory"
    sys.exit(0)

directory = sys.argv[2]

video = Video(filepath = sys.argv[1])

shots, _ = get_shots(video, (10, 10), 0.65)
shots = [s for s in shots if len(s) > 5]

shots = [
            get_partitions(s, (10,10), 0.4, 30)[0]
            for s
            in shots
        ]

shots2 = []
for s in shots:
    shots2.append([])
    for p in s:
        shots2[-1].append(get_frames(p)[0])

shots2 = get_post(shots2, 4)

for i in range(len(shots2)):
    for j in range(len(shots2[i])):
        shots2[i][j].save(directory + str(i).zfill(2) + "-" + str(j).zfill(2) + ".jpeg")
