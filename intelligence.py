from genetic import Individual, Genetic
import core
from core import Sequential
from core import Conv2D, Dense, ReLu, Sigmoid, Softmax
from tcpConnection import NumpySocket
import numpy as np

host_ip = '172.22.64.1'
npSocket = NumpySocket()
npSocket.startClient(host_ip, 9999)

image_counter = 0

SHAPE = (32, 28)
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
    image = np.array(npSocket.recieve())
    brain = population[0].model
    y = brain.forward(np.array(image))
    npSocket.send(y)