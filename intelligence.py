from genetic import Individual, Genetic
import core
from core import Sequential
from core import Conv2D, Dense, ReLu, Sigmoid, Softmax
import numpy as np
import time

from pywinauto import keyboard
from pywinauto import findwindows
import cv2
import numpy as np
import os
import subprocess
import cv2

from bizhook import Memory

# arrow keys, A=V, B=C, Y=X, X=D, START=SPACE, SELECT=ENTER, L=A, R=S, loadState = F1, screenShot = F12
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
        return last_image_array

SHAPE = (256, 224)
POP_SIZE = 10

def initialize_pop():
    pop = []
    for _ in range(POP_SIZE):
        brain = Sequential()
        brain.add(Conv2D(input_shape = SHAPE))
        brain.add(Sigmoid())
        brain.add(Dense(32))
        brain.add(Sigmoid())
        brain.add(Dense(8))
        brain.add(Sigmoid())
        brain.add(Dense(4))
        brain.add(Softmax())
        brain.initialize_weights()

        pop.append(Individual(brain))
    return pop

population = initialize_pop()
next_gen = []

combined_wram = Memory('Combined WRAM')
newX = 0
oldX = 0
while True:
    try:
        findwindows.find_window(
                    title="Super Mario World (USA) [SNES] - BizHawk")
        image = getSS()
        oldX = newX
        print("ASD")
        newX = combined_wram.read_s16_le(0x94)
        print(newX, oldX)
        time.sleep(0.1)
        brain = population[0].model
        y = brain.forward(np.array(image))
        controller(np.argmax(y))
    except:
        pass