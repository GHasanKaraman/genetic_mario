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

while(intelligence_user.clientConnect(tcpConnection._server, 1234) == False):
    print("There is no Controller")

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
    if intelligence_user.data == "":
        print("NO INPUT!")
        intelligence_user.sendData("")
    else:
        image = intelligence_user.data
        brain = population[0].model
        y = np.argmax(brain.forward(np.array(image)))
        intelligence_user.sendData(y)