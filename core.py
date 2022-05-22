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
        self.use_bias = False
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
                self.params["conv"+str(i)+"w"+str(j)] = np.random.random(kernel_size)

    def summary(self):
        w_list = []
        act_list = ['Relu',"Sigmoid", "Linear", 'Tanh', "LeakyReLu" ]
        for i in self.params:
            if 'w' in i:
                w_list.append(i)
        print('-'*68) 
        print(7*' ' +"Layer (type)" + 15*' ' + "Output Shape" + ' '*15 + "Param #")
        print('=' * 68)
        k = 0
        total_param = 0
        
        for i in range(1, len(self.layers)):
            x = 16 - len(str(self.layers[i]))
            s1 = "{} {}-{}".format(x*' ', self.layers[i], (i))
            if any(j == str(self.layers[i])  for j in act_list):  
                s3 = "{} {}".format(19*' ', 0)
            elif str(self.layers[i]) == "Conv2D":
                if len(self.x.shape) == 2:
                    x1 = self.x.shape[0] - self.layers[i].kernel_size[0] + 1
                    x2 = self.x.shape[1] - self.layers[i].kernel_size[1] + 1
                    x = 25 - len("[{},{},{},{}]".format(self.layers[i].filters, x1, x2, 1))
                    s2 = "{} [{},{},{},{}]".format(x*' ', self.layers[i].filters, x1, x2, 1)
                    x = 20 - len(str(self.layers[i].filters*self.layers[i].kernel_size[0]*self.layers[i].kernel_size[1]))
                    s3 = "{} {}".format(' '*x, self.layers[i].filters*self.layers[i].kernel_size[0]*self.layers[i].kernel_size[1])
                    total_param = total_param + self.layers[i].filters*self.layers[i].kernel_size[0]*self.layers[i].kernel_size[1]
                elif self.x.shape[2] == 3:
                    x1 = self.x.shape[0] - self.layers[i].kernel_size[0] + 1
                    x2 = self.x.shape[1] - self.layers[i].kernel_size[1] + 1
                    x = 22 - len(str(self.params[w_list[k]].shape[0])) - len(str(self.x.shape[1]))
                    s2 = "{} [{},{},{},{}]".format(x*' ', self.layers[i].filters, x1, x2, 3)
                    x = 20 - len(str(self.layers[i].filters*self.layers[i].kernel_size[0]*self.layers[i].kernel_size[1]))
                    s3 = "{} {}".format(' '*x, self.layers[i].filters*self.layers[i].kernel_size[0]*self.layers[i].kernel_size[1])
                    total_param = total_param + self.layers[i].filters*self.layers[i].kernel_size[0]*self.layers[i].kernel_size[1]
            else:
                x = 22 - len(str(self.params[w_list[k]].shape[0])) - len(str(self.x.shape[1]))
                s2 = "{} [{},{}]".format(x*' ', self.params[w_list[k]].shape[0], self.x.shape[1])
                if k == 0:
                    if self.layers[i].use_bias == True:
                        x = 20 - len(str(self.x.shape[0]*self.params[w_list[k]].shape[0] + self.params[w_list[k]].shape[0]))
                        s3 = "{} {}".format(x*' ', self.x.shape[0]*self.params[w_list[k]].shape[0] + self.params[w_list[k]].shape[0])
                        total_param = total_param + self.x.shape[0]*self.params[w_list[k]].shape[0] + self.params[w_list[k]].shape[0]
                    else:
                        x = 20 - len(str(self.x.shape[0]*self.params[w_list[k]].shape[0]))
                        s3 = "{} {}".format(x*' ', self.x.shape[0]*self.params[w_list[k]].shape[0])
                        total_param = total_param + self.x.shape[0]*self.params[w_list[k]].shape[0]
                else:
                    if self.layers[i].use_bias == True:
                        x = 20 - len(str(self.params[w_list[k - 1]].shape[0]*self.params[w_list[k]].shape[0] + self.params[w_list[k]].shape[0]))
                        s3 = "{} {}".format(x*' ', self.params[w_list[k - 1]].shape[0]*self.params[w_list[k]].shape[0] + self.params[w_list[k]].shape[0])
                        total_param = total_param + self.params[w_list[k - 1]].shape[0]*self.params[w_list[k]].shape[0] + self.params[w_list[k]].shape[0]
                    else:
                        x = 20 - len(str(self.params[w_list[k - 1]].shape[0]*self.params[w_list[k]].shape[0]))
                        s3 = "{} {}".format(x*' ', self.params[w_list[k - 1]].shape[0]*self.params[w_list[k]].shape[0])
                        total_param = total_param + self.params[w_list[k - 1]].shape[0]*self.params[w_list[k]].shape[0]
            k = k+1
            print(s1, s2, s3)
        print('='*68 + "\n" + "Total Params: "+str(total_param))


        
                
            
    def forward(self, x):
        self.x  = x

x = np.random.rand(128, 256)
model = Sequential()
model.add(Input(4))
model.add(Conv2D(256, (3,3)))
model.add(Dense(128))
model.add(LeakyReLu())
model.add(Dense(25, use_bias=(False)))
model.add(Tanh())
model.add(Dense(13))
model.add(Sigmoid())
model.initialize_weights()
model.forward(x)

model.summary()

