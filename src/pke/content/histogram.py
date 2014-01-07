
import cv, cv2

def get_change(video, (px, py), threshold):
    frames = [video[0]]
    function = []

    last = video[0].getPartHistograms(px,py)
    for i in xrange(1, len(video)):
        current = video[i].getPartHistograms(px,py)

        t = 0
        for ti in range(len(current)):
            v = cv2.compareHist(last[ti], current[ti], cv.CV_COMP_CORREL)
            t += v

        t = t / len(current)
        function.append(t)

        if t < threshold:
            last = current
            frames.append(video[i])

    return frames, function


def get_change_function(video, (px, py), threshold):
    ret = []

    last = video[0].getPartHistograms(px,py)
    for i in xrange(1, len(video)):
        current = video[i].getPartHistograms(px,py)

        t = 0
        for ti in range(len(current)):
            v = cv2.compareHist(last[ti], current[ti], cv.CV_COMP_CORREL)
            t += v

        t = t / len(current)
        ret.append(t)

        if t < threshold:
            last = current

    return ret
