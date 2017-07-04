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

		return (training_data, validation_data, test_data)