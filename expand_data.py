import csv

with open('data.csv') as csvfile:
    spamreader = csv.reader(csvfile)
    for row in spamreader:
        for col in row:
            print col, 
        print ""