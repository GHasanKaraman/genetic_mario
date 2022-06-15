from copy import deepcopy
import random

class Individual:
    def __init__(self, model):
        self.model = model
        self.fitness = 0

class Genetic:
    def __init__(self):
        pass

    def crossover(self, brain1, brain2):
        new_model = deepcopy(brain1)

        for param in new_model.params:
            weight = new_model.params[param]
            for i in range(weight.shape[0]):
                for j in range(weight.shape[1]):
                    rnd = random.random()
                    if rnd < 0.47:
                        weight[i][j] = brain1.params[param][i][j]
                    elif rnd < 0.94:
                        weight[i][j] = brain2.params[param][i][j]
                    else:
                        weight[i][j] = random.uniform(-5, 5)
        return new_model