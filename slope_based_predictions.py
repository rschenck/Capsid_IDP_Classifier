#!/usr/bin/env python3

import csv
from cap_classifier_data import VL3_ARRAY as vl3
import pprint
new_set = []
# new_set.append(["accession","above 0.5","max_index", "to max", "to min", "type"])
def find_max(group):
    x = 0.0
    for val in group:
        if val > x:
            x = val
    return x

def find_min(group):
    x = 1.0
    for val in group:
        if val < x:
            x = val
    return x
for row in vl3:
    new_row = []
    # index 0 - accesion number
    new_row.append(row[0])
    max_val = find_max(row[1:-2])
    min_val = find_min(row[1:-2])
    # index 1 - is the max_val > 0.5 ?
    if max_val > 0.5:
        new_row.append(1)
    else:
        new_row.append(0)

    max_index = row.index(max_val)
    min_index = row.index(min_val)
    # index 2 - the index of the max_val
    new_row.append(max_index)
    # index 3 - diff between point 1 and max
    new_row.append((max_val - row[1]))
    # index 4 - slope between max and min
    new_row.append((min_val - max_val)/ (min_index - max_index))
    #  index 5 - max_val
    new_row.append(max_val)
    new_row.append((max_val - row[1])/max_index)
    new_row.append((min_index))
    new_row.append(row[-1])
    new_set.append(new_row)


pp = pprint.PrettyPrinter(width=150)
# pp.pprint(new_set)

correct = 0
accessions = []
incorrect = []
for row in new_set:
    prediction = "Neither"
    # first branch -> it's either neither or not
    if (row[1] > 0) and (row[2] < 100):
        if row[3] >= 0.1:
            prediction = "Type B"
            if row[2] < 26:
                prediction = "Type A"
        else:
            prediction = "Type A"
    if prediction == row[-1]:
        correct += 1
    else:
        incorrect.append(row + [prediction])
        accessions.append(row[0])

# with open("troubling.csv", "wb") as f:
#     writer = csv.writer(f)
#     writer.writerows(sorted(incorrect))
print float((correct / 261.0) * 100)
print accessions
pp.pprint(["accession","bool > 0.5", "max index", "diff max and 1", "slope to min", "max val", "slope to max", "min index", "type", "prediction"])
pp.pprint(sorted(incorrect))
