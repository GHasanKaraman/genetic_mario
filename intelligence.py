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

SHAPE = (256, 224)
SCALE_PERCENT = 50
SHAPE = (int(SHAPE[0] * SCALE_PERCENT / 100), int(SHAPE[1] * SCALE_PERCENT / 100))

def getSS():
    ssList = os.listdir(path)
    if(len(ssList) > 0):
        for i in ssList:
            os.remove(path + i)

    keyboard.send_keys("{F12}")
    time.sleep(0.1)
    last_image_array = cv2.imread(path + os.listdir(path)[0], 0)
    last_image_array[15:32, 152:177] = 255
    width = int(last_image_array.shape[1] * SCALE_PERCENT / 100)
    height = int(last_image_array.shape[0] * SCALE_PERCENT / 100)
    dim = (width, height)

    last_image_array = cv2.resize(last_image_array, dim, interpolation = cv2.INTER_AREA)
    if(np.sum(last_image_array) == 0):
        keyboard.send_keys("{F1}")
    else:
        return last_image_array

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


combined_wram = Memory('Combined WRAM')

def isDied(image):
    if np.sum(image) == 0:
        return True
    oldX = combined_wram.read_s16_le(0x94)
    newX = combined_wram.read_s16_le(0x94)
    i = 0
    if combined_wram.read_s16_le(0x72) != 1024:
        while oldX == newX:
            i+=1
            newX = combined_wram.read_s16_le(0x94)
            if i >= 30:
                return True
    else:
        while combined_wram.read_s16_le(0x72) == 1024:
            i+=1
            if i >= 150:
                return True
            
    return False

next_gen = initialize_pop()
individual = next_gen[POP_SIZE - 1]
population = []
genotype = 1
gen = 1
while True:
    try:
        findwindows.find_window(
                    title="Super Mario World (USA) [SNES] - BizHawk")
        
        if len(population) == 0:
            population = Genetic().crossover(next_gen)
            bfitness = sorted(next_gen, key = lambda i:i.fitness, reverse=True)[0].fitness
            print(f"The Best Fitness Score is {bfitness}")
            next_gen.clear()
            print("New Marios Generated!")
            gen+=1
            genotype = 1

        time.sleep(0.1)           
        image = getSS()

        if isDied(image):
            print(f"Generation = {gen}, Genotype = {genotype}")
            individual.fitness = combined_wram.read_s16_le(0x94)
            next_gen.append(individual)
            individual = population.pop()
            genotype+=1
            keyboard.send_keys("{F1}")
        y = individual.model.forward(np.array(image))
        controller(np.argmax(y))
    except Exception as e:
        print(str(e))