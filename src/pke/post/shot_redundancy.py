import cv, cv2

def get_post(shots, n):
    px = 10
    py = 10
    threshold = 0.4
    nb_parts = 30

    for i in range(2, len(shots)):
        first = shots[i][0].getPartHistograms(px,py)
        
        for m in range(n):
            j = i - 2 - n
            if j < 0:
                break

            last = shots[j][-1].getPartHistograms(px, py)

            
            t = 0
            for ti in range(len(first)):
                v = cv2.compareHist(last[ti], first[ti], cv.CV_COMP_CORREL)
                if v < threshold:
                    t += 1

            if t > nb_parts:
                if len(shots[i]) > 1:
                    shots[i] = shots[i][1:]
                else:
                    if len(shots[j]) == 1:
                        shots[i] = []
                break

    return shots
