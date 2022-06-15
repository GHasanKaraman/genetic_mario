import numpy as np

class Layer:
    def __init__(self):
        self.layer_name = None
    def __repr__(self):
        return self.layer_name

class Conv2D(Layer):
    def __init__(self, input_shape):
        self.layer_name = "Conv2D"
        self.use_bias = False

        self.filters = np.array([
        
        [[9, 2, -9],
        [3, -5, 1],
        [-9, 2, 7]],
        
        [[9, -2, -9],
        [1, 0, 1],
        [-9, 2, 9]],
        
        [[-1, -1, -1],
        [-1, 9, -1],
        [-1, -1, -1]]])

        self.flatten_parameter = (input_shape[0]-2)*(input_shape[1]-2)*self.filters.shape[0]

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

    def function(self, X):
        return X

class ReLu(Activation):
    def __init__(self):
        self.layer_name = "ReLu"

    def function(self, X):
        return np.maximum(0, X)

class Sigmoid(Activation):
    def __init__(self):
        self.layer_name = "Sigmoid"

    def function(self, X):
        return 1/(1+np.exp(-X))

class Softmax(Activation):
    def __init__(self):
        self.layer_name = "Sigmoid"

    def function(self, X):
        e = np.exp(X - np.max(X))
        A = e/e.sum(axis = 0)
        return A

class Tanh(Activation):
    def __init__(self):
        self.layer_name = "Tanh"

    def function(self, X):
        return (np.exp(X)-np.exp(-X))/(np.exp(X)+np.exp(-X))
        

class LeakyReLu(Activation):
    def __init__(self):
        self.layer_name = "LeakyReLu"

    def function(self, X):
        return np.maximum(0.01*X, X)

class Sequential:
    def __init__(self):
        self.layers = []
        self.params = {}

    def add(self, layer):
        self.layers.append(layer)

    def initialize_weights(self):
        trainable_layers = list(filter(lambda layer: issubclass(type(layer), Dense) == True, self.layers))
        for i in range(len(trainable_layers) - 1):
            self.params["w"+str(i+1)] = np.random.uniform(-5, 5, (trainable_layers[i+1].units, trainable_layers[i].units))
            if trainable_layers[i+1].use_bias == True:
                self.params["b"+str(i+1)] = np.random.uniform(-5, 5, (trainable_layers[i+1].units, 1))

        self.params["w0"] = np.random.uniform(-5, 5, (trainable_layers[0].units, self.layers[0].flatten_parameter))
        self.params["b0"] = np.random.uniform(-5, 5, (trainable_layers[0].units, 1))

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

    def iterate_slices(self, image):
        h, w = image.shape

        for r in range(h - 2):
            for c in range(w - 2):
                yield image[r:r+3, c:c+3], r, c

    def convolve(self, input, filters):
        h, w = input.shape

        output = np.zeros((h - 2, w - 2, filters.shape[0]))

        for slice, r, c in self.iterate_slices(input):
            output[r, c] = np.sum(slice*filters, axis = (1, 2))
        return output

    def forward(self, X):
        Z = X.copy()
        A = Z.copy()
        d = -1
        for layer in self.layers:
            if layer.layer_name == "Conv2D":
                Z = self.convolve(Z, layer.filters)
                Z = Z.reshape(layer.flatten_parameter, -1)
            elif layer.layer_name == "Dense":
                d+=1
                Z = np.dot(self.params["w"+str(d)], A)
                if layer.use_bias == True:
                    Z = Z + self.params["b"+str(d)]
            elif issubclass(type(layer), Activation) == True:
                A = layer.function(Z)

        return A