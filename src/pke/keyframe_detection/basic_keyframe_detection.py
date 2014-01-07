# -*- coding: utf-8 -*-

import cv, cv2
import numpy as np

def opticalFlow(frame1, frame2):
    # voir http://jayrambhia.wordpress.com/2012/08/09/lucas-kanade-tracker/
    lk_params = dict(
        winSize  = (10, 10), 
        maxLevel = 5, 
        criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03)
    )
    feature_params = dict(
        maxCorners = 3000, 
        # à l'origine 0.5
        qualityLevel = 0.1, 
        minDistance = 3, 
        blockSize = 3
    )

    frame1_gray = cv2.cvtColor(frame1, cv2.cv.CV_BGR2GRAY)
    frame2_gray = cv2.cvtColor(frame2, cv2.cv.CV_BGR2GRAY)

    pt = cv2.goodFeaturesToTrack(frame1_gray, **feature_params)
    p0 = np.float32(pt).reshape(-1, 1, 2)
    
    p1, st, err = cv2.calcOpticalFlowPyrLK(frame1_gray, frame2_gray, p0, None, **lk_params)

    mean_motion = np.mean(np.absolute(np.subtract(p0, p1)))

    return mean_motion


def get_keyframe(video):
    selected_min = None
    selected_max = None

    if len(video) == 1:
        return (video[0], video[0])

    for i in range(len(video) - 1):
        frame1 = video[i]
        frame2 = video[i + 1]

        m = opticalFlow(frame1.getCVFrame(), frame2.getCVFrame())
        if selected_min == None:
            selected_min = (m, frame1)
            selected_max = (m, frame2)
        else:
            if m < selected_min[0]:
                selected_min = (m, frame1)
            if m > selected_max[0]:
                selected_max = (m, frame1)

    return ((selected_min[1], selected_max[1]))
