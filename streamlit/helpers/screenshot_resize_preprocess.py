import numpy as np
import cv2

def get_observation(self):
        self.game_location = {'top': 280, 'left': 0, 'width': 600, 'height': 500}
        raw = np.array(self.cap.grab(self.game_location))[:,:,:3].astype(np.uint8)
        gray = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(gray, (100,83))
        channel = np.reshape(resized, (1,83,100))
        return channel