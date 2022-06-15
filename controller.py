import pyautogui
import time
import numpy as np
import os
import subprocess

from sqlalchemy import false
from tcpConnection import User, _server
import cv2

# arrow keys, A=V, B=C, Y=X, X=D, START=SPACE, SELECT=ENTER, L=A, R=S, loadState = F1, screenShot = F12

controller_user = User("controller_user", 1234)
controller_user.startListen()
while(controller_user.clientConnect(_server,1235) == False):
    print("There is no AI") 


inputDict = {
    0: "left",
    1: "right",
    2: "down",
    3: "v",
}
path = "./game/Screenshots/mario000.png"
lastKey = ""


def controller(index):
    global lastKey
    if(lastKey != ""):
        pyautogui.keyUp(lastKey)

    lastKey = inputDict[index]
    pyautogui.keyDown(lastKey)

def getSS():
    if(os.path.exists(path)):
        os.remove(path)

    pyautogui.press("f12")
    time.sleep(0.8)
    last_image_array = cv2.imread(path, 0)
    if(np.sum(last_image_array) == 0):
        pyautogui.press("f1")
    else:
        controller_user.sendData(last_image_array)
        print("SENT")
    
    # time.sleep(5)


def main():
    subprocess.Popen([r"./game/snes9x-x64.exe"])
    time.sleep(0.3)
    pyautogui.press(["altleft", "f", "down", "right", "enter", "f1"])
    while True:
        if(pyautogui.getActiveWindowTitle() == "mario - Snes9x 1.60"):
            getSS()
            if(controller_user.dataChanged):
                controller_user.dataChanged = False
                print(np.argmax(controller_user.data))
                controller(np.argmax(controller_user.data))


if __name__ == "__main__":
    main()