#!/usr/bin/python2.7
# -*- coding: utf-8 -*- 

import cv,cv2, sys
import numpy as np

video = cv2.VideoCapture("video1.mp4")



def displayHist(frame):
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

def getHist(frame):
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
    b,g,r = cv2.split(frame)
    color = [(255,0,0),(0,255,0),(0,0,255)]

    # qu'est ce que ça fait ?!
    bins = np.arange(256).reshape(256,1)

    hist = []
    for item,col in zip([b,g,r],color):
        hist_item = cv2.calcHist([item],[0],None,[256],[0,255])
        cv2.normalize(hist_item,hist_item,0,255,cv2.NORM_MINMAX)
        hist.append(hist_item)

    return hist


# faudrait vérifier que la vidéo ai au moins une frame...
f, frame_previous = video.read()
hist_previous = getHist(frame_previous)
shots = [[frame_previous]]
while(f):
    f, frame = video.read()
    if not f:
        break

    hist = getHist(frame)

    t = 0
    for i in range(len(hist)):
        t += cv2.compareHist(hist_previous[i], hist[i], cv.CV_COMP_CORREL)
    t = t / len(hist)

    # 0.9 est un peu prix au hasard ici...mais ça marche pour cet exemple !
    if t < 0.9:
        shots.append([frame])
    else:
        shots[-1].append(frame)
        

    frame_previous = frame
    hist_previous = hist


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

def show2Frames(f1, f2):
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

def showShots(shots):
    for shot in shots:
        show2Frames(shot[0], shot[-1])

#showShots(shots)
#sys.exit(0)
key_frames = []
for shot in shots:
    if len(shot) == 1:
        key_frame.append(shot[0])
        continue

    selected_min = None
    selected_max = None
    for i in range(len(shot) - 1):
        frame1 = shot[i]
        frame2 = shot[i + 1]

        m = opticalFlow(frame1, frame2)
        if selected_min == None:
            selected_min = (m, frame1)
            selected_max = (m, frame2)
        else:
            if m < selected_min[0]:
                selected_min = (m, frame1)
            if m > selected_max[0]:
                selected_max = (m, frame1)

    key_frames.append((selected_min[1], selected_max[1]))


for f1, f2 in key_frames:
    show2Frames(f1, f2)

