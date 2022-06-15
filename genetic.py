from copy import deepcopy
from core import Sequential
from core import Dense, ReLu, Sigmoid, Conv2D, Softmax
import numpy as np
import random

class Individual:
    def __init__(self, model):
        self.model = model
        self.fitness = 0

class Genetic:
    def __init__(self, POP_SIZE, architecture, input_shape):
        self.POP_SIZE = POP_SIZE
        self.architecture = architecture
        self.input_shape = input_shape

    def create_model(self):
        model = Sequential()
        model.add(Conv2D(input_shape = self.input_shape))
        model.add(ReLu())
        model.add(Dense(128))
        model.add(Sigmoid())
        model.add(Dense(64))
        model.add(Sigmoid())
        model.add(Dense(16))
        model.add(Sigmoid())
        model.add(Dense(4))
        model.add(Softmax())
        model.initialize_weights()
        return model

    def initialize_population(self):
        pop = []
        for _ in range(self.POP_SIZE):
            pop.append(Individual(self.create_model(self.input_shape)))
        return pop

    def fitness_scores(self, pop, X):
        for ind in pop:
            ind.fitness = ind.model.forward(X)

    def crossover(self, pop):
        best = int(len(pop)*0.1)
        next_gen = []
        for i in range(best):
            next_gen.append(Individual(deepcopy(pop[i].model)))
        
        while not len(next_gen) == self.POP_SIZE:
            model1 = deepcopy(random.choice(next_gen).model)
            model2 = deepcopy(random.choice(next_gen).model)

            new_model = self.create_model()

            for param in new_model.params:
                weight = new_model.params[param]
                for i in range(weight.shape[0]):
                    for j in range(weight.shape[1]):
                        rnd = random.random()
                        if rnd < 0.47:
                            weight[i][j] = model1.params[param][i][j]
                        elif rnd < 0.94:
                            weight[i][j] = model2.params[param][i][j]
                        else:
                            weight[i][j] = random.uniform(-5, 5)
            next_gen.append(Individual(new_model))
        return next_gen