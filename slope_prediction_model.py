#!/usr/bin/env python3
import numpy as np


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
# this is a long, function enjoy
def main(scores)
    new_set = []
    #create rows in new dataset
    for i in range(len(scores)):
        row = list(scores[i])
        new_row = []

        max_val = find_max(row)
        min_val = find_min(row)
        # index 0 - is the max_val > 0.5 ?
        if max_val > 0.53:
            new_row.append(1)
        else:
            new_row.append(0)

        max_index = row.index(max_val)
        min_index = row.index(min_val)
        # index 1 - the index of the max_val
        new_row.append(max_index)
        # index 2 - diff between point 1 and max
        new_row.append((max_val - row[0]))
        # index 3 - slope between max and min
        new_row.append((min_val - max_val)/ (min_index - max_index))
        #  index 4 - max_val
        new_row.append(max_val)
        # index 5 - slope to max
        if max_index > 0: new_row.append((max_val - row[0])/max_index)
        if max_index == 0: new_row.append(0)
        # index 6 - index of the min_val
        new_row.append((min_index))
        diffs = get_diffs(local_max_min(row))
        # index 7-11 - diffs or None
        for diff in diffs:
            new_row.append(diff)
        new_set.append(new_row)


    predictions = []
    for row in new_set:
        prediction = "Neither"

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
    return np.asarray(predictions)
