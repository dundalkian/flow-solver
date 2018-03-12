import time

import numpy as np
import pyautogui as gui
from PIL import ImageGrab

# I'm just testing code in here right now

while True:
    screen = ImageGrab.grab()
    print(screen.getpixel(gui.position()))
