# Cancer Wisconsin (Diagnostic) Data Set
Predict whether the cancer is benign or malignant

## Description of Data Set
Attribute Information:
* ID number 
* Diagnosis (M = malignant, B = benign)

Ten real-valued features are computed for each cell nucleus:

* radius (mean of distances from center to points on the perimeter) 
* texture (standard deviation of gray-scale values) 
* perimeter 
* area 
* smoothness (local variation in radius lengths)
* compactness
* concavity (severity of concave portions of the contour) 
* concave points (number of concave portions of the contour) 
* symmetry 
* fractal dimension ("coastline approximation" - 1)

The mean, standard error and "worst" or largest (mean of the three largest values) of these features were computed for each image, resulting in 30 features. For instance, field 3 is Mean Radius, field 13 is Radius SE, field 23 is Worst Radius.

All feature values are recoded with four significant digits.

Missing attribute values: none

Class distribution: 357 benign, 212 malignant

## Normalization of Data

Data normalization means transforming all variables in the data to a specific range. In our case it's [0, 1].

![MathEquation](http://i.imgur.com/IgWw5eX.png)

## Code

* Parse CSV Data into a text file 
```python
import csv

with open('data.csv') as csvfile:
    spamreader = csv.reader(csvfile)
    for row in spamreader:
        for col in row:
            print col, 
        print ""
```

* Organise data

1. Randomly shuffle data and assign 60% of data into training_data, remaining into validation_data and test_data

```python
import numpy as np
import random

def vectorized_result(j):
    e = np.zeros((2, 1))
    e[j] = 1
    return e

def load_data():
	x = []
	y = []
	data = []
	training_data = []
	test_data = []
	validation_data = []

	with open('inp', 'r') as f:
		data = []
		for line in f:
			arr = line.split()
			if arr[1] == 'B':
				y.append(int(0))
			else:
				y.append(int(1))
			arr.pop(0)
			arr.pop(0)
			for x_ in xrange(len(arr)):
				arr[x_] = float(arr[x_])
			x.append(arr)

		minx = []
		maxx = []
		for x__ in xrange(30):
			minx.append(10000)

		for x__ in xrange(30):
			maxx.append(-10000)

		for i in x:
			for j in xrange(30):
				minx[j] = min(minx[j], i[j])
				maxx[j] = max(maxx[j], i[j])

		for i in x:
			for j in xrange(30):
				i[j] = float(i[j] - minx[j]) / float(maxx[j] - minx[j])

		# print x		

		dx = [np.reshape(ix, (30, 1)) for ix in x]
		dy = np.asarray(y)

		data = zip(dx, dy)

		random.shuffle(data)

		training_data = []
		test_data = []
		validation_data = []

		for i in xrange(400):
			training_data.append(data[0])
			data.pop()

		for i in xrange(100):
			validation_data.append(data[0])
			data.pop()

		while len(data):
			test_data.append(data[0])
			data.pop()

		print len(training_data), len(test_data), len(validation_data)

		return (training_data, validation_data, test_data

```

* Neural Networks

```python

import random
import numpy as np

class Network(object):

    def __init__(self, sizes):
        self.num_layers = len(sizes)
        self.sizes = sizes
        self.biases = [np.random.randn(y, 1) for y in sizes[1:]]
        self.weights = [np.random.randn(y, x)
                        for x, y in zip(sizes[:-1], sizes[1:])]

    def feedforward(self, a):
        for b, w in zip(self.biases, self.weights):
            a = sigmoid(np.dot(w, a)+b)
        return a

    def SGD(self, training_data, epochs, mini_batch_size, eta,
            test_data=None):
        if test_data: n_test = len(test_data)
        n = len(training_data)
        for j in xrange(epochs):
            random.shuffle(training_data)
            mini_batches = [
                training_data[k:k+mini_batch_size]
                for k in xrange(0, n, mini_batch_size)]
            for mini_batch in mini_batches:
                self.update_mini_batch(mini_batch, eta)
            if test_data:
                print "Epoch {0}, {1}%".format(
                    j + 1, calc(self.evaluate(test_data), n_test))
            else:
                print "Epoch {0} complete".format(j)

    def update_mini_batch(self, mini_batch, eta):
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        for x, y in mini_batch:
            delta_nabla_b, delta_nabla_w = self.backprop(x, y)
            nabla_b = [nb+dnb for nb, dnb in zip(nabla_b, delta_nabla_b)]
            nabla_w = [nw+dnw for nw, dnw in zip(nabla_w, delta_nabla_w)]
        self.weights = [w-(eta/len(mini_batch))*nw
                        for w, nw in zip(self.weights, nabla_w)]
        self.biases = [b-(eta/len(mini_batch))*nb
                       for b, nb in zip(self.biases, nabla_b)]

    def backprop(self, x, y):
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        activation = x
        activations = [x]
        zs = []
        for b, w in zip(self.biases, self.weights):
            z = np.dot(w, activation)+b
            zs.append(z)
            activation = sigmoid(z)
            activations.append(activation)
        delta = self.cost_derivative(activations[-1], y) * sigmoid_prime(zs[-1])
        nabla_b[-1] = delta
        nabla_w[-1] = np.dot(delta, activations[-2].transpose())
        for l in xrange(2, self.num_layers):
            z = zs[-l]
            sp = sigmoid_prime(z)
            delta = np.dot(self.weights[-l+1].transpose(), delta) * sp
            nabla_b[-l] = delta
            nabla_w[-l] = np.dot(delta, activations[-l-1].transpose())
        return (nabla_b, nabla_w)

    def evaluate(self, test_data):
        test_results = [(np.argmax(self.feedforward(x)), y)
                        for (x, y) in test_data]
        return sum(int(x == y) for (x, y) in test_results)

    def cost_derivative(self, output_activations, y):
        return (output_activations-y)

def sigmoid(z):
    return 1.0/(1.0+np.exp(-z))

def calc(x, y):
    percnt = float(x * 1.0)
    percnt = float(percnt) / float(y * 1.0)
    percnt = float(percnt) * 100.0
    return float(percnt)

def sigmoid_prime(z):
    return sigmoid(z)*(1-sigmoid(z))


```
