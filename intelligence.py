from genetic import Individual, Genetic
import core
from core import Sequential
from core import Conv2D, Dense, ReLu, Sigmoid, Softmax

from PIL import Image

import numpy as np
X = np.random.rand(64, 56)

brain1 = Sequential()
brain1.add(Conv2D(input_shape = X.shape))
brain1.add(Sigmoid())
brain1.add(Dense(32))
brain1.add(Sigmoid())
brain1.add(Dense(8))
brain1.add(Sigmoid())
brain1.add(Dense(4))
brain1.add(Softmax())

brain1.initialize_weights()

print("====== BIR =====")
y = brain1.forward(X)
for i in y:
    for j in i:
        print(j)

brain2 = Sequential()
brain2.add(Conv2D(input_shape = X.shape))
brain2.add(Sigmoid())
brain2.add(Dense(32))
brain2.add(Sigmoid())
brain2.add(Dense(8))
brain2.add(Sigmoid())
brain2.add(Dense(4))
brain2.add(Softmax())

brain2.initialize_weights()

print("====== IKI =====")
y = brain2.forward(X)
for i in y:
    for j in i:
        print(j)

new_brain = Genetic().crossover(brain1, brain2)

print("====== NEW =====")
y = new_brain.forward(X)
for i in y:
    for j in i:
        print(j)

img = Image.open(r"C:\Users\hasan\Desktop\genetic_mario\game\Screenshots\mario000.png").convert("L")
img = img.resize((128, 112))

out = Sequential().convolve(np.array(img), Conv2D((64, 56)).filters)

for i in range(10):
    Image.fromarray(out[:, :, i]).show()