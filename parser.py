import cv2
import numpy as np
from PIL import Image
import pyscreenshot 
import pytesseract
import pyautogui
import json
import time
import multiprocessing
import os 

def preprocess(im):
    nimg = im.convert('L')
    ret,img = cv2.threshold(np.array(nimg), 125, 255, cv2.THRESH_BINARY)
    img = Image.fromarray(img.astype(np.uint8))
    return img

data = {}
boxes = {'commentary': (140, 820, 1766, 1013),
         'page_right': (1630, 215, 1889, 265),
         'page_left': (20, 211, 342, 300)}

completed = [".".join(f.split(".")[:-1]) for f in os.listdir("C:\\Users\\a\\Desktop\\Programming\\hsbook\\dumps")]


for i in range(0,66):
    try:
        time.sleep(0.3)
    
        if i % 2 != 0:
            pbox = boxes['page_right']

        else:
            pbox = boxes['page_left']

        p_img = pyscreenshot.grab(pbox, childprocess=False)
        
        page = pytesseract.image_to_string(preprocess(p_img)).replace(" ", "").replace("[S]", "")
        if page == '':
            page = pytesseract.image_to_string(p_img).replace(" ", "")
        if "-" in page:
            page = int(page.split("-")[1])

        page = int(page)
        print(page)
    

        for _ in range(0,2):
            pyautogui.keyDown("pagedown")
            pyautogui.keyUp("pagedown")

        if str(page) not in completed:

            c_img = pyscreenshot.grab(boxes['commentary'], childprocess=False)
            commentary = pytesseract.image_to_string(c_img).replace("\n", " ").replace("\\", "")

            try:
                data[page] += "\n\n" + commentary
            except KeyError:
                data[page] = commentary

        pyautogui.keyDown("pagedown")
        pyautogui.keyUp("pagedown")
        
    except ValueError as e:
        print("error page %s" % i)
        print(e)
        for _ in range(0,3):
            pyautogui.keyDown("pagedown")
            pyautogui.keyUp("pagedown")

    

for page in data.keys():
    dct = {'id': 0, 'title': None, 'page': page, 'commentary': data[page], 'notes': None}
    path = "dumps\\%s.json" % page
    with open(path, "w") as f:
        f.write(json.dumps([dct]))
    


                 
                 
                
