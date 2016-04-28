#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import imp
ds = imp.load_source("dataset", "./development/dataset.py")
scores, type_array = ds.load_data()

def local_max_min(array):
    slopes = []
    vertices, values = [0],[]
    for i in range(1, len(array)):
        slopes.append(array[i] - array[i-1])
    for i in range(1, len(slopes)):
        if (slopes[i] > 0 and slopes[i - 1] < 0) or (slopes[i] < 0 and slopes[i - 1] > 0):
            vertices.append(i)
    vertices.append(124)

    for i in range(len(vertices)):
        values.append(array[vertices[i]])

    return vertices, values

with PdfPages('cap_graphs.pdf') as pdf:
    x = range(0,125)
    for j in range(len(type_array)):
        vertices, values = local_max_min(scores[j])
        fig = plt.figure()
        plt.plot(x,scores[j],'r-',vertices, values, "b-")
        plt.axis([0,130,0,1.2])
        plt.title("Entry #" + str(j) +  ' -> ' + type_array[j])
        pdf.savefig(fig)
