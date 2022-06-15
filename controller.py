import pyautogui
import time
import numpy as np
import os
import subprocess
from tcpConnection import NumpySocket
import cv2

# arrow keys, A=V, B=C, Y=X, X=D, START=SPACE, SELECT=ENTER, L=A, R=S, loadState = F1, screenShot = F12

npSocket = NumpySocket()
npSocket.startServer(9999)

inputDict = {
    0: "left",
    1: "right",
    2: "down",
    3: "v",
}
path = "./game/Screenshots/mario000.png"

def controller(index):
    pyautogui.press(inputDict[index])

def getSS():
    if(os.path.exists(path)):
        os.remove(path)

    pyautogui.press("f12")
    time.sleep(0.8)
    last_image_array = cv2.imread(path, 0)
    if(np.sum(last_image_array) == 0):
        pyautogui.press("f1")
    else:
        npSocket.send(last_image_array)


def main():
    subprocess.Popen([r"./game/snes9x-x64.exe"])
    time.sleep(0.3)
    pyautogui.press(["altleft", "f", "down", "right", "enter", "f1"])
    while True:
        if(pyautogui.getActiveWindowTitle() == "mario - Snes9x 1.60"):
            getSS()

            print(np.argmax(npSocket.recieve()))
            controller(np.argmax(npSocket.recieve()))


if __name__ == "__main__":
    main()
