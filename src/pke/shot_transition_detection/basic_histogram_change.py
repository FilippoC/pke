# -*- coding: utf-8 -*-

import cv, cv2
from pke.video import Video

def get_shots(video):
    if len(video) == 0:
        return []
    if len(video) == 1:
        return [video]

    shots = [Video(frames = [video[0]])]
    
    for i in xrange(1, len(video)):
        previous = video[i - 1].getHistogram()
        current = video[i].getHistogram()

        t = 0
        for ti in range(len(current)):
            t += cv2.compareHist(previous[ti], current[ti], cv.CV_COMP_CORREL)
        t = t / len(current)

        # 0.9 est un peu prix au hasard ici...mais ça marche pour cet exemple !
        if t < 0.9:
            shots.append(Video(frames = [video[i]]))
        else:
            shots[-1].addFrame(video[i])

    return shots
