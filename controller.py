import ssl
import time
from matplotlib.pyplot import title
import numpy as np
import os
import subprocess

from tcpConnection import User, _server
from pywinauto import keyboard
from pywinauto import findwindows
import cv2

# arrow keys, A=V, B=C, Y=X, X=D, START=SPACE, SELECT=ENTER, L=A, R=S, loadState = F1, screenShot = F12

controller_user = User("controller_user", 1234)
controller_user.startListen()
while(controller_user.clientConnect(_server, 1235) == False):
    print("There is no AI")


inputDict = {
    0: "LEFT",
    1: "RIGHT",
    2: "DOWN",
    3: "x",
}
path = "./game/SNES/Screenshots/"
lastKey = ""


def controller(index):
    global lastKey
    if(lastKey != ""):
        keyboard.send_keys("{"+lastKey+" up}")

    lastKey = inputDict[index]
    keyboard.send_keys("{"+lastKey+" down}")


def getSS():
    ssList = os.listdir(path)
    if(len(ssList) > 0):
        for i in ssList:
            os.remove(path + i)

    keyboard.send_keys("{F12}")
    time.sleep(0.2)
    last_image_array = cv2.imread(path + os.listdir(path)[0], 0)
    if(np.sum(last_image_array) == 0):
        keyboard.send_keys("{F1}")
    else:
        controller_user.sendData(last_image_array)
        print("SENT")


def main():
    subprocess.Popen([r"./game/EmuHawk.exe"])
    time.sleep(2)
    keyboard.send_keys("{VK_MENU down}"
                       "f"
                       "{VK_MENU up}")

    keyboard.send_keys("{DOWN}"
                       "{ENTER}"
                       "{ENTER}"
                       "{F1}")
    while True:
        try:
            findwindows.find_window(
                title="Super Mario World (USA) [SNES] - BizHawk")
            getSS()
            if(controller_user.dataChanged):
                controller_user.dataChanged = False
                print(np.argmax(controller_user.data))
                controller(np.argmax(controller_user.data))
        except:
            pass


if __name__ == "__main__":
    main()
