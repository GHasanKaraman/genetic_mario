import numpy as np

class Layer:
    def __init__(self):
        self.layer_name = None
    def __repr__(self):
        return self.layer_name

class Conv2D(Layer):
    def __init__(self, filters, kernel_size, activation=None, **kwargs):
        self.layer_name = "Conv2D"
        self.filters = filters
        self.kernel_size = kernel_size
        self.activation = activation
        for key, value in kwargs.items():
            if key == "input_shape":
                self.input_shape = value

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
        self.use_bias = True

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
        trainable_layers = list(filter(lambda layer: issubclass(type(layer), Dense) == True, self.layers)) 
        if hasattr(trainable_layers[0], "input_dim"):
            trainable_layers.insert(0, Input(trainable_layers[0].input_dim))
            delattr(trainable_layers[1], "input_dim")
        for i in range(len(trainable_layers) - 1):
            if hasattr(trainable_layers[i+1], "input_dim"):
                raise RuntimeError("You cannot add multiple input dimensions. It is only for the first layer!")
            self.params["w"+str(i+1)] = np.random.rand(trainable_layers[i+1].units, trainable_layers[i].units)
            if trainable_layers[i+1].use_bias == True:
                self.params["b"+str(i+1)] = np.random.rand(trainable_layers[i+1].units, 1)

        trainable_conv_layers = list(filter(lambda layer: issubclass(type(layer), Conv2D) == True, self.layers))
        for i in range(len(trainable_conv_layers)):
            filters = trainable_conv_layers[i].filters
            kernel_size = trainable_conv_layers[i].kernel_size
            for j in range(filters):
                self.params["conv"+str(i)+"w"+str(j)] = np.random.random(filters)

    def summary(self):
        for i in self.layers:
            print(i)
        pass

    def forward(self):
        pass


model = Sequential()
model.add(Conv2D(256, (3,3)))
model.add(Input(4))
model.add(Dense(128))
model.add(LeakyReLu())
model.add(Dense(25))
model.add(Tanh())
model.add(Dense(13))
model.add(Sigmoid())
model.initialize_weights()

for i in model.params:
    print(i)

#model.summary()
