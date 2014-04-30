# -*- coding: utf-8 -*-

import cv, cv2
from pke.video import Video

def get_shots(video, (px, py), threshold):
    if len(video) == 0:
        return [], []
    if len(video) == 1:
        return [video], []

    shots = [Video(frames = [video[0]])]
    function = []
    
    for i in xrange(1, len(video)):
        previous = video[i - 1].getPartHistograms(px,py)
        current = video[i].getPartHistograms(px,py)

        t = 0
        for ti in range(len(current)):
            v = cv2.compareHist(previous[ti], current[ti], cv.CV_COMP_CORREL)
            t += v
        t = t / len(current)

        function.append(t)

        if t < threshold:
            shots.append(Video(frames = [video[i]]))
        else:
            shots[-1].addFrame(video[i])

    return shots, function
