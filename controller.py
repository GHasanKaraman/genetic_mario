import pyautogui
import time
import numpy as np
import os
import subprocess
from PIL import Image
from tcpConnection import User
from tcpConnection import _server

# arrow keys, A=V, B=C, Y=X, X=D, START=SPACE, SELECT=ENTER, L=A, R=S, loadState = F1, screenShot = F12

controllerUser = User("controller", 1234)
controllerUser.startListen()
while(controllerUser.clientConnect(_server, 1235) == False):
    print("There is no AI")


inputDict = {
    0: "left",
    1: "right",
    2: "down",
    3: "v",
}
path = "./game/Screenshots"
ssTime = 0.2


def controller(index):
    pyautogui.press(inputDict[index])


def getSS():
    SSdir = os.listdir(path)
    if(len(SSdir) > 0):
        last_image_path = path+"/"+SSdir[len(SSdir)-1]
        last_image_array = np.array(Image.open(last_image_path))

        if(np.sum(last_image_array) == 0):
            pyautogui.press("f1")
            controllerUser.sendMessage("siyah")

    if(len(SSdir) > 50):
        for i in SSdir:
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
                controller(controllerUser.messageBox[len(
                    controllerUser.messageBox)-1])

            last_time = time.time()


if __name__ == "__main__":
    main()
