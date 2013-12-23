# -*- coding: utf-8 -*-

import cv, cv2
import numpy as np
import math

class Frame(object):

    def __init__(self, cv_frame):
        self.cv_frame = cv_frame

        self.histogram = None
        self.gray_histogram = None
        self.part_hists = {}

    def getCVFrame(self):
        return self.cv_frame

    def getGrayscaleHistogram(self):
        if self.gray_histogram != None:
            return [self.gray_histogram]

        gray_image = cv2.cvtColor(self.getCVFrame(), cv2.COLOR_BGR2GRAY)
        gray_histogram = cv2.calcHist([gray_image],[0],None,[256],[0,255])
        cv2.normalize(gray_histogram,gray_histogram,0,255,cv2.NORM_MINMAX)

        return [gray_histogram]

    def getHistogram(self):
        if self.histogram != None:
            return self.histogram

        """
        hist = cv2.calcHist(
            [frame], [0,1,2], 
            None, 
            [256, 256,256], 
            # http://stackoverflow.com/questions/15834602/how-to-calculate-3d-histogram-in-python-using-open-cv
            # [[0, 255], [0,255],[0,255]]
            [0, 255, -255, 255, -255, 255]
        )"""

        # la normalization doit se faire canal par canal...
        b,g,r = cv2.split(self.getCVFrame())
        color = [(255,0,0),(0,255,0),(0,0,255)]

        # qu'est ce que ça fait ?!
        bins = np.arange(256).reshape(256,1)

        self.histogram = []
        for item,col in zip([b,g,r],color):
            hist_item = cv2.calcHist([item],[0],None,[256],[0,255])
            cv2.normalize(hist_item,hist_item,0,255,cv2.NORM_MINMAX)
            self.histogram.append(hist_item)

        return self.histogram


    # Only grayscale !
    def getPartHistograms(self, px, py):
        if (px, py) in self.part_hists:
            return self.part_hists[(px, py)]

        gray_image = cv2.cvtColor(self.getCVFrame(), cv2.COLOR_BGR2GRAY)
        height, width = gray_image.shape

        size_x = int(math.ceil(float(width)/float(px)))
        size_y = int(math.ceil(float(height)/float(py)))

        hists = []
        for x in range(px):
            for y in range(py):
                
                subimage = gray_image[np.ix_(
                            range(y * size_y, min((y + 1) * size_y, height)),
                            range(x * size_x, min((x + 1) * size_x, width))
                            )]
                h = cv2.calcHist([subimage],[0],None,[256],[0,255])
                cv2.normalize(h,h,0,255,cv2.NORM_MINMAX)

                hists.append(h)

        self.part_hists[(px, py)] = hists

        return hists

    def getOpticalFlow(self, frame2):
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

        frame1_gray = cv2.cvtColor(self.getCVFrame(), cv2.cv.CV_BGR2GRAY)
        frame2_gray = cv2.cvtColor(frame2.getCVFrame(), cv2.cv.CV_BGR2GRAY)

        pt = cv2.goodFeaturesToTrack(frame1_gray, **feature_params)
        p0 = np.float32(pt).reshape(-1, 1, 2)
        
        p1, st, err = cv2.calcOpticalFlowPyrLK(frame1_gray, frame2_gray, p0, None, **lk_params)

        mean_motion = np.mean(np.absolute(np.subtract(p0, p1)))

        return mean_motion
