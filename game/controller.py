from sqlite3 import Time
from xml.etree.ElementTree import PI
import pyautogui
import time
import numpy as np
import os
import subprocess
from PIL import Image
from tcpConnection import User

# arrow keys, A=V, B=C, Y=X, X=D, START=SPACE, SELECT=ENTER, L=A, R=S, loadState = F1, screenShot = F12

controllerUser = User("controller", 1234)
controllerUser.startListen()

inputDict = {
    0: "left",
    1: "right",
    2: "down",
    3: "v",
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

    pyautogui.press("f12")


def main():
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

            if(len(controllerUser.messageBox) > 0):
                controller(controllerUser.messageBox[len(controllerUser.messageBox)-1])
                
            last_time = time.time()


if __name__ == "__main__":
    main()
