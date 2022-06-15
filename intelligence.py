from genetic import Individual, Genetic
import core
from core import Sequential
from core import Conv2D, Dense, ReLu, Sigmoid, Softmax
import tcpConnection
from tcpConnection import User
from PIL import Image
import numpy as np

image_counter = 0

SHAPE = (32, 28)
POP_SIZE = 10

intelligence_user = User("AI", 1235)
intelligence_user.startListen()
intelligence_user.clientConnect(tcpConnection._server, 1234)

def getLastImage():
    global image_counter
    if image_counter > 50:
        image_counter = 0
    image_text = "0"*(3-len(str(image_counter)))+str(image_counter)
    image = Image.open(r".\game\Screenshots\mario"+f"{image_text}.png").convert("L")
    image = image.resize(SHAPE)
    image_counter += 1
    return image

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

while True:
    img = getLastImage()
    brain = population.pop().model
    y = np.argmax(brain.forward(np.array(img)))
    intelligence_user.sendMessage(y)
    if(intelligence_user.messageBox.pop() == "siyah"):
        break