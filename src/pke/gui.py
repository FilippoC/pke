# -*- coding: utf-8 -*-

import cv, cv2
import numpy as np


def display_histogram(frame):
    hist_height = 300
    hist_width = 256

    cv2.namedWindow('colorhist', cv2.CV_WINDOW_AUTOSIZE)

    b,g,r = cv2.split(frame)
    color = [(255,0,0),(0,255,0),(0,0,255)]

    # image à afficher
    h = np.zeros((300,256,3))

    # qu'est ce que ça fait ?!
    bins = np.arange(256).reshape(256,1)

    for item,col in zip([b,g,r],color):
        hist_item = cv2.calcHist([item],[0],None,[256],[0,255])
        # les valeurs sont entre 0 et 1, on change donc ça pour avoir 0-255
        # pour un meilleur affichage
        cv2.normalize(hist_item,hist_item,0,255,cv2.NORM_MINMAX)
        hist=np.int32(np.around(hist_item))
        pts = np.column_stack((bins,hist))
        cv2.polylines(h,[pts],False,col)

    h=np.flipud(h)

    cv2.imshow('colorhist',h)
    cv2.waitKey(0)

def display_frame(f1):
    cv2.imshow("test", f1.getCVFrame())
    cv2.waitKey()


def display_2_frames(f1, f2):
    f1 = f1.getCVFrame()
    f2 = f2.getCVFrame()

    # http://stackoverflow.com/questions/7589012/combining-two-images-with-opencv
    # modifié pour afficher des images en couleur
    h1, w1 = f1.shape[:2]
    h2, w2 = f2.shape[:2]
    #vis = np.zeros((max(h1, h2), w1+w2), np.uint32)
    vis = np.zeros((max(h1, h2), w1+w2, 3), np.uint8)
    vis[:h1, :w1] = f1
    vis[:h2, w1:w1+w2] = f2
    #vis = cv2.cvtColor(vis, cv2.COLOR_GRAY2BGR)

    cv2.imshow("test", vis)
    cv2.waitKey()
