from sqlite3 import Time
from xml.etree.ElementTree import PI
import pyautogui
import time
import numpy as np
import os
import subprocess
from PIL import Image


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
path = "./game/Screenshots"
ssTime = 0.2


def controller(inputList):
    for i in range(len(inputList)):
        if(inputList[i] >= 1):
            pyautogui.press(inputDict[i])


def getSS():
    if(len(os.listdir(path)) > 0):
        last_image_path = path+"/"+os.listdir(path)[len(os.listdir(path))-1]
        last_image_array = np.array(Image.open(last_image_path))

        if(np.sum(last_image_array) == 0):
            pyautogui.press("f1")

    if(len(os.listdir(path)) > 50):
        for i in os.listdir(path):
            os.remove(path+"/"+i)

    getSquareLoss()
    pyautogui.press("f12")


def getSquareLoss():
    dirList = os.listdir(path)
    if(len(dirList) >= 2):
        last0_image_path = path+"/"+dirList[len(dirList)-1]
        last0_image_array = np.array(Image.open(last0_image_path))/255.0

        last1_image_path = path+"/"+dirList[len(dirList)-2]
        last1_image_array = np.array(Image.open(last1_image_path))/255.0

        pixNum = np.shape(last0_image_array)[
            0] * np.shape(last0_image_array)[1]

        print((np.sum(np.square(last0_image_array - last1_image_array)))/pixNum)


def main():
    inputs = np.zeros(len(inputDict))
    last_time = time.time()
    ssCounter = ssTime

    subprocess.Popen([r"./game/snes9x-x64.exe"])
    time.sleep(0.3)
    pyautogui.press(["altleft", "f", "down", "right", "enter", "f1"])
    while True:
        if(pyautogui.getActiveWindowTitle() == "mario - Snes9x 1.60"):
            if(ssCounter <= 0):
                getSS()
                ssCounter = ssTime
            else:
                ssCounter = ssCounter - (time.time() - last_time)

            controller(inputs)
            last_time = time.time()


if __name__ == "__main__":
    main()