import cv2
import numpy as np

from PIL import ImageGrab


class PixelFinder:
    def __init__(self, multi_match_f, capture_screen, imageFolder="script_lib/images/"):
        self.imageFolder = imageFolder
        self.multi_match = multi_match_f
        self.capture_screen = capture_screen
        self.game_image = None

    
    

    def FindImage(self, imageName):
        ##Read Main and Needle Image
        #img_rgb = self.capture_screen()
        screenshot = np.array(ImageGrab.grab())
                # Convert the Pillow image to a NumPy array of uint8
        screenshot_np = np.array(screenshot, dtype=np.uint8)

        # Convert the BGR format to RGB (Pillow uses RGB)
        img_rgb = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2RGB)
        template = cv2.imread(f'{self.imageFolder}{imageName}.png')
        if template is None:
            print(f'Image of {imageName} not found!')
            return
        #CV_TM_SQDIFF 

        w, h = template.shape[:-1]
        #cv2.TM_SQDIFF
        res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.95
        loc = np.where(res >= threshold)
    
        #for pt in zip(*loc[::-1]):  # Switch columns and rows
        #    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255),2)
        if len(loc[0]) <= 0:
            return None
        


        return [list(zip(*loc[::-1]))[0][0], list(zip(*loc[::-1]))[0][1] + h/2]