
import cv, cv2

def get_partitions(video, (px, py), threshold, nb_parts):
    frames = [[video[0]]]
    function = [px * py]

    last = video[0].getPartHistograms(px,py)
    for i in xrange(1, len(video)):
        current = video[i].getPartHistograms(px,py)

        t = 0
        for ti in range(len(current)):
            v = cv2.compareHist(last[ti], current[ti], cv.CV_COMP_CORREL)
            if v < threshold:
                t += 1

        if t > nb_parts:
            last = current
            frames.append([video[i]])
            function.append(px * py)
        else:
            frames[-1].append(video[i])
            function.append(t)


    return frames, function

