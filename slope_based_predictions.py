#!/usr/bin/env python3
import imp
ds = imp.load_source("dataset", './development/dataset.py')
import csv
import pprint
new_set = []
# new_set.append(["accession","above 0.5","max_index", "to max", "to min", "type"])

scores, type_array, acc = ds.load_data()
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

def local_max_min(array):
    slopes = []
    vertices, values = [0],[]
    for i in range(1, len(array)):
        slopes.append(array[i] - array[i-1])
    for i in range(1, len(slopes)):
        if (slopes[i] > 0 and slopes[i - 1] <= 0) or (slopes[i] < 0 and slopes[i - 1] >= 0):
            vertices.append(i)
    vertices.append(124)
    vertices = curate_vertices(vertices)
    for i in range(len(vertices)):
        values.append(array[vertices[i]])
    vertices, values = further_curation(vertices, values)
    return values

def curate_vertices(vertices):
    to_delete = []
    for i in range(1,len(vertices)):
        if (vertices[i] - vertices[i-1] < 10):
            to_delete.append(i)
    to_delete.reverse()
    for x in to_delete:
        del vertices[x]
    return vertices

def further_curation(vertices,values):
    to_delete = []
    for i in range(1,len(vertices)):
        if abs(values[i] - values[i -1]) < 0.05:
            to_delete.append(i)
    to_delete.reverse()
    for x in to_delete:
        del vertices[x]
        del values[x]
    return vertices, values

def get_diffs(values):
    diffs = []
    for i in range(1,len(values)):
        diffs.append(values[i] - values[i-1])
    for i in range(5 - len(diffs)):
        diffs.append(None)
    return diffs
#create rows in new dataset
for i in range(len(type_array)):
    row = list(scores[i])
    new_row = []
    # index 0 -
    new_row.append(type_array[i])
    max_val = find_max(row)
    min_val = find_min(row)
    # index 1 - is the max_val > 0.5 ?
    if max_val > 0.53:
        new_row.append(1)
    else:
        new_row.append(0)

    max_index = row.index(max_val)
    min_index = row.index(min_val)
    # index 2 - the index of the max_val
    new_row.append(max_index)
    # index 3 - diff between point 1 and max
    new_row.append((max_val - row[0]))
    # index 4 - slope between max and min
    new_row.append((min_val - max_val)/ (min_index - max_index))
    #  index 5 - max_val
    new_row.append(max_val)
    if max_index > 0: new_row.append((max_val - row[0])/max_index)
    if max_index == 0: new_row.append(0)
    new_row.append((min_index))
    diffs = get_diffs(local_max_min(row))
    for diff in diffs:
        new_row.append(diff)
    new_row.append(i)
    new_set.append(new_row)


pp = pprint.PrettyPrinter(width=250)
# pp.pprint(new_set)

correct = 0
indexes = []
incorrect = []
predictions = []
index = 0
for row in new_set:
    prediction = "Neither"
# Based on the diff to max and max_index
    # if (row[1] > 0) and (row[2] < 100):
    #     if row[3] > 0.06539:
    #         prediction = "Type B"
    #     else:
    #         prediction = "Type A"
    #         if row[8] > 0.121987:
    #             prediction = "Type B"

# Based on additional diffs
    if row[1] > 0:
        # decisions made from sifting through dataset
        if (row[8] > 0.1219871) or ((row[8] + row[9] if row[9] else row[8]) > 0):
            prediction = "Type B"
        else:
            prediction = "Type A"
            condition = row[8] + row[9] if row[9] else row[8]
            condition += row[10] if row[10] else 0
            if condition > 0:
                prediction = "Type B"
    predictions.append(prediction)
    if prediction == row[0]:
        correct += 1
    else:
        incorrect.append([prediction] + row + [index])
        indexes.append(index)

    index += 1

# with open("slope_dataset_2.csv", "wb") as f:
#     writer = csv.writer(f)
#     writer.writerow(["type","bool > 0.5", "max index", "diff max and 1", "slope to min", "max val", "slope to max", "min index","diff 1","diff 2","diff 3","diff 4","diff 5", "entry #"])
#     writer.writerows(new_set)
#     writer.writerow(["incorrect predictions"])
#     writer.writerow(["prediction","type","bool > 0.5", "max index", "diff max and 1", "slope to min", "max val", "slope to max", "min index","diff 1","diff 2","diff 3","diff 4","diff 5","entry #"])
#     writer.writerows(incorrect)

# print float((correct  / float(len(acc))) * 100)
# print indexes
# pp.pprint(["prediction","type","bool > 0.5", "max index", "diff max and 1", "slope to min", "max val", "slope to max", "min index","diff 1","diff 2","diff 3","diff 4","diff 5","index"])
# pp.pprint(incorrect)
