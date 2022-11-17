import pytesseract
from screenshot_resize_preprocess import get_observation

def get_text(self):
        done_cap = get_observation(self)
        res = pytesseract.image_to_string(done_cap)[:4]
        return res