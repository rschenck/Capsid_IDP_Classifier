#!/usr/bin/env python3
import numpy as np

def find_max(group):
    x = 0.0
    for val in group:
        if val > x:
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
def main(scores):
    new_set = []
    #create rows in new dataset
    for i in range(len(scores)):
        row = list(scores[i])
        new_row = []
        max_val = find_max(row)
        # index 0 - is the max_val > 0.5 ?
        if max_val > 0.53:
            new_row.append(1)
        else:
            new_row.append(0)

        diffs = get_diffs(local_max_min(row))
        # index 1-5 - diffs or None
        for diff in diffs:
            new_row.append(diff)
        new_set.append(new_row)


    predictions = []
    for row in new_set:
        prediction = "Neither"

    # Based on additional diffs
        if row[0] > 0:
            # decisions made from sifting through dataset
            if (row[1] > 0.1219871) or ((row[1] + row[2] if row[2] else row[1]) > 0):
                prediction = "Type B"
            else:
                prediction = "Type A"
                condition = (row[1] + row[2] if row[2] else row[1])
                if row[3]:
                    condition += row[3]
                if condition > 0:
                    prediction = "Type B"
        predictions.append(prediction)
    return np.asarray(predictions)
