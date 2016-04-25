#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from cap_classifier_data import VL3_ARRAY as vl3

entry = 0
for i in range(len(vl3) / 10):
    with PdfPages('cap_graphs_'+ str(i + 1) +'.pdf') as pdf:
        x = range(0,125)
        for j in range(10):
            if entry < len(vl3):
                accession = vl3[entry][0]
                scores = np.array(vl3[entry][1:-1])
                classification = vl3[entry][-1]
                fig = plt.figure()
                plt.plot(x,scores,'r-')
                plt.axis([0,130,0,1.2])
                plt.title(accession + ' -> ' + classification)
                pdf.savefig(fig)
                entry += 1
