import numpy as np

class Layer:
    def __init__(self):
        self.layer_name = None
    def __repr__(self):
        return self.layer_name

class Dense(Layer):
    def __init__(self, units, activation = None, use_bias = True, **kwargs):
        self.layer_name = "Dense"
        self.units = units
        self.activation = activation
        self.use_bias = use_bias
        for key, value in kwargs.items():
            if key == "input_dim":
                self.input_dim = value

class Input(Dense):
    def __init__(self, input_dim):
        self.layer_name = "Input"
        self.units = input_dim
        self.use_bias = False

class Activation(Layer):
    pass

class Linear(Activation):
    def __init__(self):
        self.layer_name = "Linear"

class ReLu(Activation):
    def __init__(self):
        self.layer_name = "ReLu"

class Sigmoid(Activation):
    def __init__(self):
        self.layer_name = "Sigmoid"

class Tanh(Activation):
    def __init__(self):
        self.layer_name = "Tanh"

class LeakyReLu(Activation):
    def __init__(self):
        self.layer_name = "LeakyReLu"

class Sequential:
    def __init__(self):
        self.layers = []
        self.params = {}

    def add(self, layer):
        self.layers.append(layer)

    def initialize_weights(self):
        pass

    def summary(self):
        for i in self.layers:
            print(i)
        pass

    def forward(self):
        pass


model = Sequential()
model.add(Dense(128))
model.add(LeakyReLu())
model.add(Dense(25))
model.add(Tanh())
model.add(Dense(13))
model.add(Sigmoid())

model.summary()
