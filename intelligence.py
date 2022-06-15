from genetic import Individual, Genetic
import core
from core import Sequential
from core import Conv2D, Dense, ReLu, Sigmoid, Softmax
from tcpConnection import User, _server
import numpy as np

ai_user = User("ai_user", 1235)
ai_user.startListen()
while(ai_user.clientConnect(_server, 1234) == False):
    print("There is no Controller") 

image_counter = 0

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

while True:
    if(ai_user.dataChanged):
        ai_user.dataChanged = False
        image = ai_user.data
        brain = population[0].model
        y = brain.forward(np.array(image))
        print(y)
        ai_user.sendData(y)