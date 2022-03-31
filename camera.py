import cv2
from numpy import fliplr as invert

class Camera:
    def __init__(self, camera_id=0, mirrored=True):
        self.camera = cv2.VideoCapture(camera_id)
        self.mirrored = mirrored
    def update(self):
        _, frame = self.camera.read()
        self.frame = invert(frame)
        return self.frame
    def writeFrame(self):
        self.writer.write(self.frame)