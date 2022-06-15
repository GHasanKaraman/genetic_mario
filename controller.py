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
path = "./game/Screenshots/mario000.png"
ssTime = 0.2


def controller(index):
    pyautogui.press(inputDict[index])


def getSS():
    if(os.path.exists(path)):
        os.remove(path)

    pyautogui.press("f12")
    
    last_image_array = np.array(Image.open(path))
    if(np.sum(last_image_array) == 0):
        controllerUser.sendData("")
        pyautogui.press("f1")
    else:
        controllerUser.sendData(last_image_array)


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

            if(controllerUser.data != ""):
                controller(controllerUser.data)

            last_time = time.time()


if __name__ == "__main__":
    main()
