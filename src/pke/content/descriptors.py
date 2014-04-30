# -*- coding: utf-8 -*-

import cv, cv2
import numpy as np

def get_partitions(video, threshold):
    frame1 = video[0].getCVFrame()

    detector = cv2.FeatureDetector_create("SIFT")
    descriptor = cv2.DescriptorExtractor_create("SIFT")
     
    skp = detector.detect(frame1)
    #skp, sd = descriptor.compute(img, skp)
    
    print(skp)
    len(skp)
