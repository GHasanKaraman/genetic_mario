from copy import deepcopy
import random

class Individual:
    def __init__(self, model):
        self.model = model
        self.fitness = 0

class Genetic:
    def __init__(self):
        pass

    def crossover(self, population):
        pop = sorted(population, key = lambda i:i.fitness, reverse = True)
        next_gen = []
        next_gen.append(Individual(deepcopy(pop[0].model)))
        next_gen.append(Individual(deepcopy(pop[1].model)))
        next_gen.append(Individual(deepcopy(pop[2].model)))

        while not len(next_gen) == len(pop):
            brain1 = random.choice(next_gen).model
            brain2 = random.choice(next_gen).model
            new_model = deepcopy(brain1)

            for param in new_model.params:
                weight = new_model.params[param]
                for i in range(weight.shape[0]):
                    for j in range(weight.shape[1]):
                        rnd = random.random()
                        if rnd < 0.40:
                            weight[i][j] = brain1.params[param][i][j]
                        elif rnd < 0.80:
                            weight[i][j] = brain2.params[param][i][j]
                        else:
                            weight[i][j] = random.uniform(-5, 5)
            next_gen.append(Individual(new_model))
        return next_gen