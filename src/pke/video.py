import cv,cv2

from frame import Frame

class Video(object):
    def __init__(self, **keys):
        self.frames = []

        if "filepath" in keys:
            video = cv2.VideoCapture(keys["filepath"])
        
            self.frames = []
        
            while(True):
                f, frame = video.read()
                if not f:
                    break

                self.addFrame(Frame(frame))

            return

        if "frames" in keys:
            for f in keys["frames"]:
                self.addFrame(f)
            return

    def addFrame(self, frame):
        self.frames.append(frame)

    def __len__(self):
        return len(self.frames)

    def __getitem__(self, i):
        return self.frames[i]

    #def __iter__(self):
    #    return iter(self.frames)
