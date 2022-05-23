from prometheus_client import Counter
import pyautogui
import time
import numpy as np
import os
import PIL

# arrow keys, A=V, B=C, Y=X, X=D, START=SPACE, SELECT=ENTER, L=A, R=S, loadState = F1, screenShot = F12

inputDict = {
    0: "left",
    1: "right",
    2: "up",
    3: "down",
    4: "v",
    5: "c",
    6: "x",
    7: "d",
    8: "space",
    9: "enter",
    10: "a",
    11: "s",
    12: "f1",
    13: "f12"
}


def controller(inputList):
    for i in range(len(inputList)):
        if(inputList[i] >= 1):
            pyautogui.press(inputDict[i])


def checkImage():
    path = "./game/Screenshots"
    if(len(os.listdir(path)) > 0):
        last_image_path = path+"/"+os.listdir(path)[len(os.listdir(path))-1]
        last_image_array = np.array(PIL.Image.open(last_image_path))

        if(np.sum(last_image_array) == 0):
            pyautogui.press("f1")

    if(len(os.listdir(path)) > 50):
        for i in os.listdir(path):
            os.remove(path+"/"+i)

    pyautogui.press("f12")


ssTime = 0.2
ssCounter = ssTime

inputs = np.zeros(len(inputDict))
last_time = time.time()

while True:
    if(pyautogui.getActiveWindowTitle() == "mario - Snes9x 1.60"):
        if(ssCounter <= 0):
            checkImage()
            ssCounter = ssTime
        else:
            ssCounter = ssCounter - (time.time() - last_time)

    last_time = time.time()

    controller(inputs)
