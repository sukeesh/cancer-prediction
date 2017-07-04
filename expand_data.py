import csv
import random
import numpy as np

x = []
y = []
arr = []
newarr = []
data = []

# def load_data():
with open('data.csv') as csvfile:
    spamreader = csv.reader(csvfile)
    for row in spamreader:
        for col in row:
            print col, 
        print ""
        
    # for i in xrange(1, len(arr)):
    #     newarr.append(arr[i])

    # for i in newarr:
    #     cnt = 0
    #     tx = []
    #     for j in i:
    #         cnt = cnt + 1
    #         if cnt == 1:
    #             fc = 0
    #         elif cnt == 2:
    #             if j == 'M':
    #                 y.append(int(1))
    #             else:
    #                 y.append(int(0))
    #         else:
    #             tx.append(float(j))
    #     x.append(tx)

    # for i in xrange(len(x)):
    #     data.append((x[i], y[i]))

    # random.shuffle(data)

    # training_data = []
    # test_data = []
    # validation_data = []

    # for i in xrange(int(0.6 * 570.0)):
    #     training_data.append(data[i])

    # while i < 470:
    #     test_data.append(data[i])
    #     i = i + 1

    # while i < 576:
    #     validation_data.append(data[i])
    #     i = i + 1

    # return (training_data, validation_data, test_data)

