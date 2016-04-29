#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import imp
ds = imp.load_source("dataset", "./development/dataset.py")
scores, type_array, acc = ds.load_data()

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
    return vertices, values

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

with PdfPages('cap_graphs.pdf') as pdf:
    x = range(0,125)
    fig = plt.figure()
    for j in range(len(type_array)):
        vertices, values = local_max_min(scores[j])
        plt.plot(x,scores[j],'r-',vertices, values, "b-")
        plt.axis([0,130,0,1.2])
        plt.title("Entry # " + str(j) + ": " + acc[j] +  ' -> ' + type_array[j])
        pdf.savefig(fig)
        fig.clf()
